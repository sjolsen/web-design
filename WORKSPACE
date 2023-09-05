workspace(name = "web_design")

load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")
git_repository(
    name = "web_compiler",
    remote = "https://github.com/sjolsen/web_compiler.git",
    commit = "71fa43abc80122bbbb05e2f57bbd7416c09fa3e2",
    shallow_since = "1693877491 -0500",
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
    sha256 = "5868e73107a8e85d8f323806e60cad7283f34b32163ea6ff1020cf27abef6036",
    strip_prefix = "rules_python-0.25.0",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.25.0/rules_python-0.25.0.tar.gz",
)

load("@rules_python//python:pip.bzl", "pip_parse")
load("@rules_python//python:repositories.bzl", "py_repositories")
py_repositories()

# Create a central repo that knows about the dependencies needed for
# requirements.txt.
pip_parse(
    name = "pip_deps",
    requirements = "@web_compiler//:pip_requirements.txt",
)

# Load the central repo's install function from its `//:requirements.bzl` file,
# and call it.
load("@pip_deps//:requirements.bzl", "install_deps")
install_deps()
