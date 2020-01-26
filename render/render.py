import html
import sys
from xml.etree import ElementTree as ET

from web_design.render import parser

def make_html_node(name, attrs, contents):
  parts = [name]
  for key, value in attrs:
    parts.append(f'{key}="{html.escape(value)}"')
  return f'<{name}>{contents}</{name}>'


def main(argv):
  [_, input_filename] = argv
  tree = ET.parse(input_filename)
  root = tree.getroot()
  print(parser.ParseDocument(root))


if __name__ == '__main__':
  rv = main(sys.argv)
  sys.exit(rv or 0)
