import subprocess
from pathlib import Path


def exec_pwsh(command: str) -> str:
    output = subprocess.getoutput(f"powershell -c {command}")
    return output


if __name__ == "__main__":
    user_path = exec_pwsh("[Environment]::GetEnvironmentVariable('PATH', 'User')")
    user_path = user_path.strip()
    bin_dir = Path(__file__).resolve().parent.joinpath("bin")
    bin_dir = str(bin_dir).replace("\\", "/")
    if bin_dir not in user_path:
        user_path += ";" + bin_dir
    exec_pwsh(f"[Environment]::SetEnvironmentVariable('PATH', '{user_path}', 'User')")
    user_path = exec_pwsh("[Environment]::GetEnvironmentVariable('PATH', 'User')")
    user_path = user_path.strip()
    print(user_path)
