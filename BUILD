genrule(
  name = "output",
  srcs = ["lorem-ipsum.xml"],
  outs = ["output.html"],
  tools = ["//render"],
  cmd = "$(location //render) $(SRCS) > $@",
)
