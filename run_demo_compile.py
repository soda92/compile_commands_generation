import subprocess
import contextlib

from init_shim_config import write_shim_config, wrapper_path
from tools import (
    vs_set_env,
    get_cl_dir,
    CD,
    parse_vs_version,
    run_build,
    VisualStudioVersion,
)

import argparse


@contextlib.contextmanager
def CreateDebuggingConfig(port: int, vs_version: VisualStudioVersion):
    _CL_DIR = get_cl_dir(vs_version=vs_version)
    with CD(_CL_DIR):
        with open("cl.shim", mode="w") as file:
            file.write(
                f"""path = python.exe
args = -m debugpy --listen 56799 --wait-for-client {wrapper_path} {vs_version}"""
            )
    yield

    write_shim_config(vs_version=vs_version)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", default=False)
    parser.add_argument("--port", type=int, default=5678)
    parser.add_argument("--vs-version", type=str, default="2008")
    args = parser.parse_args()

    vs_version = parse_vs_version(args.vs_version)
    vs_set_env(vs_version=vs_version)

    if vs_version == VisualStudioVersion.VS2008:
        run_build(
            vs_version=vs_version,
            project_dir="qt_demo_vs2008",
            project_file="demo.vcproj",
            port=args.port,
            is_debug=args.debug,
        )
    else:
        run_build(
            vs_version=vs_version,
            project_dir="demo_project/build",
            project_file="ALL_BUILD.vcxproj",
            port=args.port,
            is_debug=args.debug,
        )
