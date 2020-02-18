load("//server:server.bzl", "ResourceInfo", "TransitiveResources")

def _blog_document(ctx):
    ctx.actions.run_shell(
        outputs = [ctx.outputs.html],
        inputs = ctx.files.srcs,
        tools = [ctx.executable._render],
        command = "{render} {main} > {output}".format(
            render = ctx.executable._render.path,
            main = ctx.file.main.path,
            output = ctx.outputs.html.path,
        ),
    )
    resource = struct(
        src = ctx.outputs.html,
        path = ctx.outputs.html.short_path,
    )
    resources = TransitiveResources(resource, ctx.attr._default_deps)
    return [ResourceInfo(resource=resource, resources=resources)]


blog_document = rule(
    implementation = _blog_document,
    attrs = {
        "main": attr.label(
            mandatory = True,
            allow_single_file = True,
        ),
        "srcs": attr.label_list(
            mandatory = True,
            allow_files = True,
        ),
        "_default_deps": attr.label_list(
            providers = [ResourceInfo],
            default = [
                "//render:bullet",
                "//render:style",
            ],
        ),
        "_render": attr.label(
            executable = True,
            default = "//render",
            cfg = "exec",
        ),
    },
    outputs = {
        "html": "%{name}.html",
    },
)
