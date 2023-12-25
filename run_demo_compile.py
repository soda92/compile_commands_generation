import subprocess
import contextlib
from cl_dir_defines import CL_DIR

from init_shim_config import write_shim_config, wrapper_path
from tools import CD, vs2008_set_env, vs2019_set_env
import argparse


@contextlib.contextmanager
def CreateDebuggingConfig(port: int, vs_version: str):
    _CL_DIR = CL_DIR
    if vs_version == "2019_64":
        _CL_DIR = "C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Tools/MSVC/14.29.30133/bin/Hostx64/x64"
    with CD(_CL_DIR):
        with open("cl.shim", mode="w") as file:
            file.write(
                f"""path = python.exe
args = -m debugpy --listen 56799 --wait-for-client {wrapper_path} {vs_version}"""
            )
    yield

    write_shim_config(vs_version=vs_version)


def run_vcbuild(proj: str):
    subprocess.run(
        f"vcbuild {proj} /nologo /platform:Win32 Debug /rebuild".split(),
        check=True,
    )


def run_msbuild(proj: str):
    subprocess.run(
        f"msbuild {proj} -t:Rebuild -p:Configuration=Debug".split(),
        check=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", default=False)
    parser.add_argument("--port", type=int, default=5678)
    parser.add_argument("--vs-version", type=str, default="2008")
    args = parser.parse_args()

    if args.vs_version == "2008":
        vs2008_set_env()
        with CD("qt_demo_vs2008"):
            if args.debug:
                with CreateDebuggingConfig(port=args.port, vs_version=args.vs_version):
                    run_vcbuild("demo.vcproj")
            else:
                run_vcbuild("demo.vcproj")

    elif args.vs_version == "2019_64":
        vs2019_set_env()
        with CD("demo_project/build"):
            if args.debug:
                with CreateDebuggingConfig(port=args.port, vs_version=args.vs_version):
                    run_msbuild("ALL_BUILD.vcxproj")
            else:
                run_msbuild("ALL_BUILD.vcxproj")
