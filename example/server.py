from http import server
import os
import tempfile


PORT = 8000


RESOURCES = {
  'index.html': 'example/example.html',
  'style.css': 'style.css',
}


with tempfile.TemporaryDirectory() as d:
  for link, origin in RESOURCES.items():
    src = os.path.abspath(origin)
    dst = os.path.join(d, link)
    os.symlink(src, dst)
  def handler(*args, **kwargs):
    return server.SimpleHTTPRequestHandler(*args, directory=d, **kwargs)
  with server.HTTPServer(('', PORT), handler) as httpd:
    httpd.serve_forever()
