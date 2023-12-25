from cl_dir_defines import *
import os, contextlib
import subprocess


def parse_vs_version(vs_version: str) -> VisualStudioVersion:
    if vs_version == "2008":
        return VisualStudioVersion.VS2008
    elif vs_version == "2019_64":
        return VisualStudioVersion.VS2019_64
    else:
        return VisualStudioVersion.VS2022_64


@contextlib.contextmanager
def CD(dir: str):
    old_dir = os.getcwd()
    os.chdir(dir)
    yield
    os.chdir(old_dir)


def vs2008_set_env():
    with CD("C:/Program Files (x86)/Microsoft Visual Studio 9.0/Common7/Tools/"):
        output = subprocess.getoutput('cmd /c "vsvars32.bat&set"')
        for line in output.split("\n"):
            if "=" in line:
                key, val = line.split("=", maxsplit=1)
                os.putenv(key, val)


def vs2019_set_env():
    VS_community_path = "C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Auxiliary/Build"
    VS_professional_path = "C:/Program Files (x86)/Microsoft Visual Studio/2019/Community/VC/Auxiliary/Build"
    VS_path = VS_community_path
    if not Path(VS_path).exists():
        VS_path = VS_professional_path
    if not Path(VS_path).exists():
        raise SystemError("cannot find Visual Studio 2019 instance.")
    with CD(VS_path):
        output = subprocess.getoutput('cmd /c "vcvars64.bat&set"')
        for line in output.split("\n"):
            if "=" in line:
                key, val = line.split("=", maxsplit=1)
                os.putenv(key, val)


def vs2022_set_env():
    VS_community_path = (
        "C:/Program Files/Microsoft Visual Studio/2022/Professional/VC/Auxiliary/Build"
    )
    VS_professional_path = (
        "C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Auxiliary/Build"
    )
    VS_path = VS_community_path
    if not Path(VS_path).exists():
        VS_path = VS_professional_path
    if not Path(VS_path).exists():
        raise SystemError("cannot find Visual Studio 2022 instance.")
    with CD(VS_path):
        output = subprocess.getoutput('cmd /c "vcvars64.bat&set"')
        for line in output.split("\n"):
            if "=" in line:
                key, val = line.split("=", maxsplit=1)
                os.putenv(key, val)


def vs_set_env(vs_version: VisualStudioVersion):
    if vs_version == VisualStudioVersion.VS2008:
        vs2008_set_env()
    elif vs_version == VisualStudioVersion.VS2019_64:
        vs2019_set_env()
    else:
        vs2022_set_env()


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


def run_build(
    vs_version: VisualStudioVersion,
    project_dir: str,
    project_file: str,
    port: int,
    is_debug: bool = False,
):
    from run_demo_compile import CreateDebuggingConfig

    if vs_version == VisualStudioVersion.VS2008:
        build = run_vcbuild
    else:
        build = run_msbuild
    with CD(project_dir):
        if is_debug:
            with CreateDebuggingConfig(port=port, vs_version=vs_version):
                build(project_file)
        else:
            build(project_file)
