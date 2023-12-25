from tools import VisualStudioVersion, get_cl_origin, parse_vs_version
import argparse
from pathlib import Path
from pyuac import main_requires_admin
import shutil

CURRENT = Path(__file__).resolve().parent
wrapper = CURRENT.joinpath("cl_wrapper.py")
wrapper_path = str(wrapper)
SHIM_EXE = CURRENT.joinpath("shim.exe")


@main_requires_admin
def init_shim(cl_dir: Path):
    shutil.copy(cl_dir.joinpath("cl.exe"), cl_dir.joinpath("cl2.exe"))
    shutil.copy(SHIM_EXE, cl_dir.joinpath("cl.exe"))
    shim_config = cl_dir.joinpath("cl.shim")
    shim_config.write_text("---")
    shim_file = str(shim_config)
    add_user_write_permission(file=shim_file)


def add_user_write_permission(file: str):
    import win32security
    import ntsecuritycon as con

    userx, domain, type = win32security.LookupAccountName("", "Users")

    sd = win32security.GetFileSecurity(file, win32security.DACL_SECURITY_INFORMATION)
    dacl = sd.GetSecurityDescriptorDacl()  # instead of dacl = win32security.ACL()

    dacl.AddAccessAllowedAce(
        win32security.ACL_REVISION,
        con.FILE_GENERIC_READ | con.FILE_GENERIC_WRITE,
        userx,
    )

    sd.SetSecurityDescriptorDacl(1, dacl, 0)  # may not be necessary
    win32security.SetFileSecurity(file, win32security.DACL_SECURITY_INFORMATION, sd)


def write_shim_config(vs_version: VisualStudioVersion):
    origin_cl = get_cl_origin(vs_version=vs_version)
    if not origin_cl.exists():
        init_shim(cl_dir=origin_cl.parent)
    shim_config = origin_cl.parent.joinpath("cl.shim")

    shim_config.write_text(
        f"""path = python.exe
args = {wrapper_path} {vs_version}"""
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--vs-version", "-V", required=True)
    args = parser.parse_args()

    vs_version = parse_vs_version(args.vs_version)
    write_shim_config(vs_version=vs_version)
