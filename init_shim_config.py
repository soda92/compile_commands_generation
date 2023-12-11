from defines import *
import argparse

wrapper = CURRENT.joinpath("cl_wrapper.py")
wrapper_path = str(wrapper)


def get_cl_dir(vs_version: str):
    if vs_version == "2008":
        return CL_DIR
    elif vs_version == "2019_64":
        return CL_DIR_2019_64


def write_shim_config(vs_version: str):
    cl_dir = get_cl_dir(vs_version=vs_version)
    shim_file = cl_dir.joinpath("cl.shim")
    shim_file.write_text(
        f"""path = python.exe
args = {wrapper_path}"""
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--vs-version", "-V", required=True)
    args = parser.parse_args()
    write_shim_config(args.vs_version)
