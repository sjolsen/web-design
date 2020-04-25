load(
    "//compiler:compiler.bzl",
    "document",
    "site",
)
# load("//server:server.bzl", "simple_server")

document(
    name = "about",
    src = "about.xml",
)

site(
    name = "blog",
    srcs = [":about"],
    index = ":about",
    output_root = "blog",
)

# simple_server(
#     name = "server",
#     data = ":about",
# )
