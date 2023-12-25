from cl_dir_defines import *
import os, contextlib
import subprocess


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
    with CD("C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Auxiliary/Build"):
        output = subprocess.getoutput('cmd /c "vcvars64.bat&set"')
        for line in output.split("\n"):
            if "=" in line:
                key, val = line.split("=", maxsplit=1)
                os.putenv(key, val)
