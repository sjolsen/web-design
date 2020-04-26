load("//server:server.bzl", "simple_server")
load("@web_compiler//:compiler.bzl", "document", "site")

document(
    name = "about",
    main = "about.xml",
)

site(
    name = "blog",
    srcs = [
        ":about",
        # TODO: Make this implicit
        "@web_compiler//backend/swiss:nav_buttons",
        "@web_compiler//backend/swiss:style",
    ],
    build_info = "//bazel:build_info",
    index = ":about",
    nav = "nav.xml",
    output_root = "blog",
)

simple_server(
    name = "server",
    site = ":blog",
)
