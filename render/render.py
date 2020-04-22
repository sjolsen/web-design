import functools
import html
import os
import sys
from typing import Any, Dict, Iterable, Iterator, List, NamedTuple, Optional, Set, Text, Union
from xml.etree import ElementInclude
from xml.etree import ElementTree as ET

from web_design.render import document
from web_design.render import parser
from web_design.render import resource


def intersperse(sep: Any, l: Iterable[Any]) -> Iterator[Any]:
  try:
    i = iter(l)
    yield next(i)
    for item in i:
      yield sep
      yield item
  except StopIteration:
    return


class MixedContent(NamedTuple):
  parts: List['PageFragment']


class HTMLNode(NamedTuple):
  tag: Text
  attrs: Dict[Text, Union[Text, resource.Reference]]
  content: MixedContent


PageFragment = Union[Text, MixedContent, HTMLNode, resource.Reference]


@functools.singledispatch
def Render(obj) -> PageFragment:
  raise TypeError(f'No Render instance found for {type(obj)}')


@Render.register(Text)
def RenderText(text) -> PageFragment:
  return MixedContent([html.escape(text, quote=False)])


@Render.register(document.MixedContent)
def RenderMixedContent(mc) -> PageFragment:
  return MixedContent([Render(p) for p in mc.parts])


def H(tag: Text, attrs: Optional[Dict[Text, Text]] = None,
      content: Optional[MixedContent] = None) -> HTMLNode:
  return HTMLNode(tag=tag, attrs=attrs or {}, content=content or MixedContent([]))


def TitleBlock(title: PageFragment, subtitle: PageFragment) -> PageFragment:
  return H('div', {'class': 'title-block'}, MixedContent([
    H('h1', {'class': 'title'}, title),
    H('hr', {'class': 'title-rule'}),
    H('h1', {'class': 'subtitle'}, subtitle),
  ]))


def Nav() -> PageFragment:
  links = [
    ('Home', '#', resource.Reference('x.svg')),
    ('Document index', '#', resource.Reference('x.svg')),
    ('Contact', '#', resource.Reference('x.svg')),
  ]
  anchors = [
    H('a', {'class': 'nav-row', 'href': href}, MixedContent([
      H('img', {'class': 'nav-icon', 'src': src}),
      H('li', {}, MixedContent([text])),
    ]))
    for text, href, src in links
  ]
  spacer = H('div', {'class': 'nav-spacer'})
  return H('nav', {}, MixedContent([
    H('ul', {}, MixedContent(list(intersperse(spacer, anchors)))),
  ]))


@Render.register(document.Document)
def RenderDocument(doc) -> PageFragment:
  title = Render(doc.title)
  subtitle = Render(doc.subtitle)
  copyright = Render(doc.copyright)
  sections = MixedContent([Render(s) for s in doc.sections])
  style = resource.Reference('style.css')

  head = H('head', MixedContent([
    H('meta', {'charset': 'utf-8'}),
    H('title', {}, title),
    H('link', {'rel': 'stylesheet', 'href': style, 'type': 'text/css'}),
  ]))
  header = H('header', {},
    H('div', {'class': 'hcenter header-flexbox'}, MixedContent([
      TitleBlock(title, subtitle),
      H('div', {'class': 'header-vr title-rule'}),
      Nav(),
    ])))
  main_content = H('div', {'class': 'main-content'},
    H('div', {'class': 'hcenter'},
      H('div', {'class': 'body-copy'}, sections)))
  footer = H('footer', {}, H('div', {'class': 'hcenter'}, copyright))

  return MixedContent([
    '<!DOCTYPE html>',
    H('html', {'lang': 'en'}, MixedContent([
      head,
      H('body', {}, MixedContent([
        header,
        main_content,
        footer,
      ])),
    ])),
  ])


@Render.register(document.Document.Section)
def RenderDocumentSection(section) -> PageFragment:
  title = Render(section.title)
  body = Render(section.body)
  return MixedContent([
    H('h2', {'class': 'section'}, title),
    body,
  ])


@Render.register(document.HTMLNode)
def RenderHTMLNode(node) -> PageFragment:
  return HTMLNode(tag=node.tag, attrs=node.attrs, content=node.content)


@Render.register(document.Code)
def RenderCode(code) -> PageFragment:
  content = Render(code.content)
  return H('span', {'class': 'code'}, content)


@Render.register(document.CodeBlock)
def RenderCodeBlock(block) -> PageFragment:
  if block.header is not None:
    header = Render(block.header)
    body = Render(block.body)
    return H('div', {'class': 'code'}, MixedContent([
      H('div', {'class': 'code-header'}, header),
      H('div', {'class': 'code-body'},
        H('pre', {}, body)),
    ]))
  else:
    header = Render(block.header)
    return H('div', {'class': 'code'},
      H('div', {'class': 'code-body'},
        H('pre', {}, body)))


class PageResource(resource.Resource):

  def __init__(self, fragment: PageFragment):
    super().__init__()
    self._fragment = fragment

  def get_references(self) -> Set[resource.Reference]:
    refs = set()
    frontier = [self._fragment]
    while frontier:
      new_frontier = []
      for item in frontier:
        if isinstance(item, str):
          pass
        elif isinstance(item, MixedContent):
          new_frontier.extend(item.parts)
        elif isinstance(item, HTMLNode):
          new_frontier.extend(item.attrs.values())
          new_frontier.append(item.content)
        elif isinstance(item, resource.Reference):
          refs.add(item)
        else:
          raise TypeError(item)
      frontier = new_frontier
    return refs

  def _render_fragment(self, item: PageFragment,
                       linker: resource.Linker) -> Text:
    if isinstance(item, str):
      return item
    elif isinstance(item, MixedContent):
      # TODO: Indent HTML tags excluding pre?
      return ''.join(self._render_fragment(p, linker) for p in item.parts)
    elif isinstance(item, HTMLNode):
      parts = [item.tag]
      for key, value in item.attrs.items():
        value = self._render_fragment(value, linker)
        parts.append(f'{key}="{value}"')
      opentag = ' '.join(parts)
      content = self._render_fragment(item.content, linker)
      return f'<{opentag}>{content}</{item.tag}>'
    elif isinstance(item, resource.Reference):
      return linker.resolve(item)
    else:
      raise TypeError(item)

  def populate_fs(self, path: str, linker: resource.Linker):
    with open(path, 'wt') as f:
      f.write(self._render_fragment(self._fragment, linker))


def LinkStrategy(ref: resource.Reference, res: resource.Resource) -> str:
  basename = os.path.basename(ref.src_url)
  if isinstance(res, PageResource):
    base, _ = os.path.splitext(basename)
    return base + '.html'
  else:
    return basename


def main(argv):
  [_, input_filename] = argv
  tree = ET.parse(input_filename)
  root = tree.getroot()
  ElementInclude.include(root)
  doc = parser.ParseDocument(root)
  page = PageResource(RenderDocument(doc))
  linker = resource.Linker(LinkStrategy)
  linker.add_resource()


if __name__ == '__main__':
  rv = main(sys.argv)
  sys.exit(rv or 0)
