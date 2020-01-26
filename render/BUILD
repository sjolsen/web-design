py_library(
  name = "document",
  srcs = ["document.py"],
)

py_library(
  name = "parser",
  srcs = ["parser.py"],
  deps = [":document"],
)

py_binary(
  name = "render",
  srcs = ["render.py"],
  deps = [":parser"],
  visibility = ["//visibility:public"],
)
