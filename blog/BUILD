load(
    "//compiler:compiler.bzl",
    "document",
    "site",
)
load("//server:server.bzl", "simple_server")

document(
    name = "about",
    main = "about.xml",
)

site(
    name = "blog",
    srcs = [
        ":about",
        # TODO: Make this implicit
        "//compiler/backend/swiss:nav_buttons",
        "//compiler/backend/swiss:style",
    ],
    index = ":about",
    output_root = "blog",
)

simple_server(
    name = "server",
    site = ":blog",
)
