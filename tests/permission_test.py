file = "C:/Program Files/Microsoft Visual Studio/2022/Community/VC/Tools/MSVC/14.38.33130/bin/Hostx64/x64/cl.shim"

import win32security
import ntsecuritycon as con
from pyuac import main_requires_admin

userx, domain, type = win32security.LookupAccountName("", "Users")

sd = win32security.GetFileSecurity(file, win32security.DACL_SECURITY_INFORMATION)
dacl = sd.GetSecurityDescriptorDacl()  # instead of dacl = win32security.ACL()

dacl.AddAccessAllowedAce(
    win32security.ACL_REVISION, con.FILE_GENERIC_READ | con.FILE_GENERIC_WRITE, userx
)

sd.SetSecurityDescriptorDacl(1, dacl, 0)  # may not be necessary


@main_requires_admin
def main():
    win32security.SetFileSecurity(file, win32security.DACL_SECURITY_INFORMATION, sd)


if __name__ == "__main__":
    main()
