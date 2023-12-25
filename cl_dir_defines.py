from pathlib import Path
from enum import Enum, auto


class VisualStudioVersion(Enum):
    VS2008 = 0
    VS2019_64 = auto()
    VS2022_64 = auto()


def get_cl_dir(vs_version: VisualStudioVersion):
    if vs_version == VisualStudioVersion.VS2008:
        return Path(
            "C:/Program Files (x86)/Microsoft Visual Studio 9.0/VC/bin/"
        ).resolve()
    elif vs_version == VisualStudioVersion.VS2019_64:
        CL_DIR_2019_64 = Path(
            "C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Tools/MSVC/14.29.30133/bin/Hostx64/x64"
        )
        if not CL_DIR_2019_64.exists():
            CL_DIR_2019_64 = Path(
                "C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Tools/MSVC/14.29.30133/bin/Hostx64/x64"
            )
        if not CL_DIR_2019_64.exists():
            raise SystemError("Cannot find VS2019 directory, check paths")

        return CL_DIR_2019_64
    elif vs_version == VisualStudioVersion.VS2022_64:
        return Path(
            "C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC/14.38.33130/bin/Hostx64/x64"
        )


def get_cl_origin(vs_version: VisualStudioVersion):
    cl_dir = get_cl_dir(vs_version=vs_version)
    return cl_dir.joinpath("cl2.exe")
