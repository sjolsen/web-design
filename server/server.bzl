ResourceInfo = provider(fields = ['resource', 'resources'])


def TransitiveResources(root, deps):
    return depset([root], transitive=[d[ResourceInfo].resources for d in deps])


def _simple_resource(ctx):
    resource = struct(
        src = ctx.file.src,
        path = ctx.attr.path,
    )
    resources = TransitiveResources(resource, ctx.attr.deps)
    return [ResourceInfo(resource=resource, resources=resources)]


simple_resource = rule(
    implementation = _simple_resource,
    attrs = {
        "src": attr.label(
            mandatory = True,
            allow_single_file = True,
        ),
        "path": attr.string(
            mandatory = True,
        ),
        "deps": attr.label_list(
            providers = [ResourceInfo],
        ),
    },
)


_STUB_TEMPLATE = """#!/bin/sh

exec {server} {resources_file}
"""


def _simple_server(ctx):
    root = ctx.attr.data[ResourceInfo].resource
    idx = struct(
        src = root.src,
        path = "index." + root.src.extension,
    )
    resources = TransitiveResources(idx, [ctx.attr.data])
    path_map = {r.path: r.src.short_path for r in resources.to_list()}
    resources_file = ctx.actions.declare_file('resources.txt')
    ctx.actions.write(resources_file, str(path_map))
    exe = ctx.actions.declare_file(ctx.label.name)
    ctx.actions.write(exe, _STUB_TEMPLATE.format(
        server = ctx.executable._server.short_path,
        resources_file = resources_file.short_path
    ))
    return [DefaultInfo(
        executable = exe,
        runfiles = ctx.runfiles(
            [resources_file] + [r.src for r in resources.to_list()],
            transitive_files = ctx.attr._server[DefaultInfo].default_runfiles.files,
        ),
    )]


simple_server = rule(
    implementation = _simple_server,
    attrs = {
        "data": attr.label(
            mandatory = True,
            providers = [ResourceInfo],
        ),
        "_server": attr.label(
            executable = True,
            default = "//server",
            cfg = "target",
        ),
    },
    executable = True,
)
