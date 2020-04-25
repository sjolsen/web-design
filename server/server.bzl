load("//compiler:compiler.bzl", "SiteInfo")

_STUB_TEMPLATE = """#!/bin/sh

exec {server} {tarball}
"""

def _simple_server(ctx):
    tarball = ctx.attr.site[SiteInfo].tarball
    exe = ctx.actions.declare_file(ctx.label.name)
    ctx.actions.write(exe, _STUB_TEMPLATE.format(
        server = ctx.executable._server.short_path,
        tarball = tarball.short_path
    ))
    return [DefaultInfo(
        executable = exe,
        runfiles = ctx.runfiles(
            [tarball],
            transitive_files = ctx.attr._server[DefaultInfo].default_runfiles.files,
        ),
    )]


simple_server = rule(
    implementation = _simple_server,
    attrs = {
        "site": attr.label(
            mandatory = True,
            providers = [SiteInfo],
        ),
        "_server": attr.label(
            executable = True,
            default = "//server",
            cfg = "target",
        ),
    },
    executable = True,
)
