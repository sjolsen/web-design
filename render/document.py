from typing import *


class Content(object):
  pass


class MixedContent(NamedTuple):
  parts: List[Union[Text, Content]]


class Document(NamedTuple):
  title: MixedContent
  subtitle: MixedContent
  copyright: MixedContent
  sections: List['Document.Section']

  class Section(NamedTuple):
    title: MixedContent
    body: MixedContent


class HTMLNode(NamedTuple, Content):
  tag: Text
  attrs: Dict[Text, Text]
  content: MixedContent


class CodeBlock(NamedTuple, Content):
  header: MixedContent
  body: MixedContent
