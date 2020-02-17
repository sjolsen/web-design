load("//render:render.bzl", "blog_document")
load("//server:server.bzl", "simple_server")

blog_document(
    name = "example",
    main = "example.xml",
    srcs = [
        "example.xml",
        "fib.c",
        "fib.dis",
    ],
)

simple_server(
    name = "server",
    data = ":example",
)
