import functools
import html
import sys
import typing
from xml.etree import ElementTree as ET

from web_design.render import document
from web_design.render import parser


@functools.singledispatch
def Render(obj):
  raise TypeError(f'No Render instance found for {type(obj)}')


@Render.register(typing.Text)
def RenderText(text):
  return html.escape(text, quote=False)


@Render.register(document.MixedContent)
def RenderMixedContent(mc):
  return ''.join(map(Render, mc.parts))


@Render.register(document.Document)
def RenderDocument(doc):
  title = Render(doc.title)
  subtitle = Render(doc.subtitle)
  copyright = Render(doc.copyright)
  sections = '\n\n'.join(map(Render, doc.sections))
  return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{title}</title>
    <link rel="stylesheet" href="/style.css" type="text/css" />
  </head>
  <body>
    <header>
      <div class="hcenter">
        <h1 class="title">{title}</h1>
        <hr class="title" />
        <h2 class="subtitle">{subtitle}</h2>
      </div>
    </header>
    <div class="main-content">
      <div class="hcenter">
        <div class="body-copy">

          {sections}

        </div>
      </div>
    </div>
    <footer>
      <div class="hcenter">{copyright}</div>
    </footer>
  </body>
</html>
"""


@Render.register(document.Document.Section)
def RenderDocumentSection(section):
  title = Render(section.title)
  body = Render(section.body)
  return f"""<h2 class="section">{title}</h2>{body}"""


@Render.register(document.HTMLNode)
def RenderHTMLNode(node):
  parts = [node.tag]
  for key, value in node.attrs:
    parts.append(f'{key}="{html.escape(value)}"')
  opentag = ' '.join(parts)
  content = Render(node.content)
  return f'<{opentag}>{content}</{node.tag}>'


@Render.register(document.Code)
def RenderCode(code):
  content = Render(code.content)
  return f'<span class="code">{content}</span>'


@Render.register(document.CodeBlock)
def RenderCodeBlock(block):
  if block.header is not None:
    header = Render(block.header)
    body = Render(block.body)
    return f"""<div class="code">
  <div class="code-header">{header}</div>
  <div class="code-body">
    <pre>{body}</pre>
  </div>
 </div>"""
  else:
    body = Render(block.body)
    return f"""<div class="code">
  <div class="code-body">
    <pre>{body}</pre>
  </div>
 </div>"""


def main(argv):
  [_, input_filename] = argv
  tree = ET.parse(input_filename)
  root = tree.getroot()
  doc = parser.ParseDocument(root)
  print(RenderDocument(doc))


if __name__ == '__main__':
  rv = main(sys.argv)
  sys.exit(rv or 0)
