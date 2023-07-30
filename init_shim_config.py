from tools import CL_DIR, CURRENT

if __name__ == "__main__":
    wrapper = CURRENT.joinpath("cl_wrapper.py")
    wrapper_path = str(wrapper)
    shim_file = CL_DIR.joinpath("cl.shim")
    shim_file.write_text(
        f"""path = python.exe
args = {wrapper_path}"""
    )
