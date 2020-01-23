import sys
import typing
from xml.etree import ElementTree as ET

from renderer import document


def text_and_children(node):
  result = []
  if node.text is not None:
    result.append(node.text)
  for child in node:
    result.append(child)
    if child.tail is not None:
      result.append(child.tail)
  return result


def is_whitespace(s):
  return not s.strip()


def BlogTag(name):
  return '{http://sj-olsen.com/blog}' + name


def ParseDocument(node):
  assert node.tag == BlogTag('document')
  by_tag = {}
  for part in text_and_children(node):
    if isinstance(part, typing.Text):
      assert is_whitespace(part)
      continue
    try:
      assert isinstance(part, ET.Element)
    except Exception:
      print(type(part), file=sys.stderr)
      raise
    by_tag.setdefault(part.tag, []).append(part)
  try:
    [title] = by_tag[BlogTag('title')]
    [subtitle] = by_tag[BlogTag('subtitle')]
    [copyright] = by_tag[BlogTag('copyright')]
    sections = by_tag[BlogTag('section')]
  except Exception:
    print(by_tag, file=sys.stderr)
    raise
  return document.Document(
    title=ParseMixedContent(title),
    subtitle=ParseMixedContent(subtitle),
    copyright=ParseMixedContent(copyright),
    sections=list(map(ParseDocumentSection, sections)))


def ParseDocumentSection(node):
  pass


def ParseMixedContent(node):
  pass
