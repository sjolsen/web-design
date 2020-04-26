load("//server:server.bzl", "simple_server")
load("@web_compiler//:compiler.bzl", "document", "site")

document(
    name = "about",
    main = "about.xml",
    srcs = [
        # TODO: Make this implicit
        "@web_compiler//backend/swiss:nav_buttons",
        "@web_compiler//backend/swiss:style",
    ],
)

document(
    name = "home",
    main = "home.xml",
    srcs = [
        # TODO: Make this implicit
        "@web_compiler//backend/swiss:nav_buttons",
        "@web_compiler//backend/swiss:style",
    ],
)

site(
    name = "blog",
    srcs = [
        ":about",
        ":home",
    ],
    build_info = "//bazel:build_info",
    index = ":home",
    nav = "nav.xml",
    output_root = "blog",
)

simple_server(
    name = "server",
    site = ":blog",
)
