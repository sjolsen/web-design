load("@pip_deps//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "server",
    srcs = ["server.py"],
    visibility = ["//visibility:public"],
    deps = [requirement("absl-py")],
)
