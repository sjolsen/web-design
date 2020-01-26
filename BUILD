genrule(
  name = "output",
  srcs = ["lorem-ipsum.xml"],
  outs = ["output.xml"],
  tools = ["//render"],
  cmd = "$(location //render) $(SRCS) > $@",
)
