from cl_dir_defines import *
import argparse

CURRENT = Path(__file__).resolve().parent
wrapper = CURRENT.joinpath("cl_wrapper.py")
wrapper_path = str(wrapper)


def write_shim_config(vs_version: str):
    cl_dir = get_cl_dir(vs_version=vs_version)
    shim_file = cl_dir.joinpath("cl.shim")
    shim_file.write_text(
        f"""path = python.exe
args = {wrapper_path} {vs_version}"""
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--vs-version", "-V", required=True)
    args = parser.parse_args()
    write_shim_config(args.vs_version)
