load("//compiler:compiler.bzl", "document", "site")
load("//server:server.bzl", "simple_server")

document(
    name = "example",
    main = "example.xml",
    srcs = [
        "example.xml",
        "fib.c",
        "fib.dis",
    ],
)

site(
    name = "example_site",
    srcs = [
        ":example",
        # TODO: Make this implicit
        "//compiler/backend/swiss:nav_buttons",
        "//compiler/backend/swiss:style",
    ],
    index = ":example",
    output_root = "example",
)

simple_server(
    name = "server",
    site = ":example_site",
)
