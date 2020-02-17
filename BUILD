genrule(
  name = "output",
  srcs = [
      "fib.c",
      "fib.dis",
      "lorem-ipsum.xml",
  ],
  outs = ["output.html"],
  tools = ["//render"],
  cmd = "$(location //render) $(location :lorem-ipsum.xml) > $@",
)
