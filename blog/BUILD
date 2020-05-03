load("//server:server.bzl", "simple_server")
load("@web_compiler//:compiler.bzl", "document", "site")

document(
    name = "about",
    main = "about.xml",
)

document(
    name = "home",
    main = "home.xml",
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
