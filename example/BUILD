genrule(
  name = "example",
  srcs = [
      "fib.c",
      "fib.dis",
      "lorem-ipsum.xml",
  ],
  outs = ["example.html"],
  tools = ["//render"],
  cmd = "$(location //render) $(location :lorem-ipsum.xml) > $@",
)

py_binary(
    name = "server",
    srcs = ["server.py"],
    data = [
        ":example",
        "//:style.css",
    ],
)
