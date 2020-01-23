import sys
from xml.etree import ElementTree as ET


def Tag(ns, name):
  return f'{{{ns}}}{name}'

def Blog(name):
  return Tag('http://sj-olsen.com/blog', name)

def Html(name):
  return Tag('http://www.w3.org/1999/xhtml', name)


class Render(object):

  def __init__(self):
    self._handlers = {}

  def tag(self, tag):
    def decorator(f):
      self._handlers[tag] = f
    return decorator

  def __call__(self, node, *args, **kwargs):
    return self._handlers[node.tag](node, *args, **kwargs)

render = Render()


@render.tag(Blog('document'))
def render_document(doc):
  return 'EXAMPLE'


def main(argv):
  [_, input_filename] = argv
  tree = ET.parse(input_filename)
  root = tree.getroot()
  print(render(root))


if __name__ == '__main__':
  rv = main(sys.argv)
  sys.exit(rv or 0)
