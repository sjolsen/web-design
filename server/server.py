import ast
from http import server
import os
import sys
import tempfile


PORT = 8000


def main(argv):
  [_, resources_file] = argv
  with open(resources_file, 'rt') as f:
    resources = ast.literal_eval(f.read())
  with tempfile.TemporaryDirectory() as d:
    for link, origin in resources.items():
      src = os.path.abspath(origin)
      dst = os.path.join(d, link)
      os.makedirs(os.path.dirname(dst), exist_ok=True)
      os.symlink(src, dst)
    def handler(*args, **kwargs):
      return server.SimpleHTTPRequestHandler(*args, directory=d, **kwargs)
    with server.HTTPServer(('', PORT), handler) as httpd:
      httpd.serve_forever()


if __name__ == '__main__':
  rv = main(sys.argv)
  sys.exit(rv or 0)
