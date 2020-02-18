load("//render:render.bzl", "blog_document")
load("//server:server.bzl", "simple_server")

blog_document(
    name = "about",
    main = "about.xml",
    srcs = ["about.xml"],
)

simple_server(
    name = "server",
    data = ":about",
)
