from defines import CL_DIR
import os, contextlib
import subprocess


@contextlib.contextmanager
def CD(dir: str):
    old_dir = os.getcwd()
    os.chdir(dir)
    yield
    os.chdir(old_dir)


def vs2008_set_env():
    with CD(CL_DIR):
        output = subprocess.getoutput('cmd /c "vcvars32.bat&set"')
        for line in output.split("\n"):
            if "=" in line:
                key, val = line.split("=")
                os.putenv(key, val)
