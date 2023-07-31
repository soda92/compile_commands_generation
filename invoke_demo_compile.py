import subprocess
import contextlib
import os
from defines import CL_DIR

from init_shim_config import write_shim_config, wrapper_path
from tools import CD, vs2008_set_env


@contextlib.contextmanager
def CreateDebuggingConfig():
    with CD(CL_DIR):
        with open("cl.shim", mode="w") as file:
            file.write(
                f"""path = python.exe
args = -m debugpy --listen 5678 --wait-for-client {wrapper_path}"""
            )
    yield

    write_shim_config()


if __name__ == "__main__":
    vs2008_set_env()
    with CD("E:/src/testCffi"):
        with CreateDebuggingConfig():
            subprocess.run("vcbuild piapprox.vcproj /Rebuild".split(), check=True)
