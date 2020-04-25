from http import server
import subprocess
import tempfile

from absl import app


PORT = 8000


def main(argv):
  [_, tarball] = argv
  with tempfile.TemporaryDirectory() as d:
    subprocess.check_call(['tar', '-xzf', tarball, '-C', d])
    def handler(*args, **kwargs):
      return server.SimpleHTTPRequestHandler(*args, directory=d, **kwargs)
    with server.HTTPServer(('', PORT), handler) as httpd:
      httpd.serve_forever()


if __name__ == '__main__':
  app.run(main)
