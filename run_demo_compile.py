import subprocess
import contextlib
import os
from defines import CL_DIR

from init_shim_config import write_shim_config, wrapper_path
from tools import CD, vs2008_set_env
import argparse


@contextlib.contextmanager
def CreateDebuggingConfig(port: int):
    with CD(CL_DIR):
        with open("cl.shim", mode="w") as file:
            file.write(
                f"""path = python.exe
args = -m debugpy --listen 56799 --wait-for-client {wrapper_path}"""
            )
    yield

    write_shim_config()


def run_build():
    subprocess.run(
        "vcbuild piapprox.vcproj /nologo /platform:Win32 Debug /rebuild".split(),
        check=True,
    )


if __name__ == "__main__":
    vs2008_set_env()

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", default=False)
    parser.add_argument("--port", type=int, default=5678)
    args = parser.parse_args()

    with CD("E:/src/testCffi"):
        if args.debug:
            with CreateDebuggingConfig(port=args.port):
                run_build()
        else:
            run_build()
