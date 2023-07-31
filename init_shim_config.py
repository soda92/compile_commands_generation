from defines import CURRENT, CL_DIR

wrapper = CURRENT.joinpath("cl_wrapper.py")
wrapper_path = str(wrapper)
shim_file = CL_DIR.joinpath("cl.shim")


def write_shim_config():
    shim_file.write_text(
        f"""path = python.exe
    args = {wrapper_path}"""
    )


if __name__ == "__main__":
    write_shim_config()
