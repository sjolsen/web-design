workspace(name = "web_design")

load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")
git_repository(
    name = "web_compiler",
    remote = "https://github.com/sjolsen/web_compiler.git",
    commit = "fcce888f2b031123cef747c21b66606ac767ea07",
    shallow_since = "1588482642 -0700",
)
# local_repository(name = "web_compiler", path = "../web_compiler")

# Path manipulation
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
http_archive(
    name = "bazel_skylib",
    urls = [
        "https://mirror.bazel.build/github.com/bazelbuild/bazel-skylib/releases/download/1.0.2/bazel-skylib-1.0.2.tar.gz",
        "https://github.com/bazelbuild/bazel-skylib/releases/download/1.0.2/bazel-skylib-1.0.2.tar.gz",
    ],
    sha256 = "97e70364e9249702246c0e9444bccdc4b847bed1eb03c5a3ece4f83dfe6abc44",
)
load("@bazel_skylib//:workspace.bzl", "bazel_skylib_workspace")
bazel_skylib_workspace()

# Python setup
http_archive(
    name = "rules_python",
    sha256 = "98c9b903f6e8fe20b7e56d19c4822c8c49a11b475bd4ec0ca6a564e8bc5d5fa2",
    url = "https://github.com/bazelbuild/rules_python/archive/a0fbf98d4e3a232144df4d0d80b577c7a693b570.zip",
    strip_prefix = "rules_python-a0fbf98d4e3a232144df4d0d80b577c7a693b570",
)

load("@rules_python//python:pip.bzl", "pip3_import", "pip_repositories")
load("@rules_python//python:repositories.bzl", "py_repositories")
pip_repositories()
py_repositories()

# Create a central repo that knows about the dependencies needed for
# requirements.txt.
pip3_import(
    name = "pip_deps",
    requirements = "@web_compiler//:pip_requirements.txt",
)

# Load the central repo's install function from its `//:requirements.bzl` file,
# and call it.
load("@pip_deps//:requirements.bzl", "pip_install")
pip_install()
