# compile_commands_generation

## Install

1. download https://github.com/71/scoop-better-shimexe and compile shim.exe
1. open VS Directory 
    VS2008/VC9: C:/Program Files (x86)/Microsoft Visual Studio 9.0/VC/bin/
    VS2019 amd64: C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Tools/MSVC/14.29.30133/bin/Hostx64/x64/
1. rename cl.exe to cl2.exe
1. copy shim.exe to VS Directory as cl.exe
1. back to repo directory
1. run `init_shim_config.py`, this will set database location
1. run `pyinstaller --onefile generate_compile_commands.py`
1. add repo_directory/dist to PATH
1. fully rebuild programs to record compile commands
1. in project path, run generate_compile_commands.exe, 
it will select compile commands for current folder and generate "compile_commands.json"

## Debugging

1. Run debug config: "Test VS2019", if replaced shim correctly, it'll stop at compile
1. place breakpoints at "cl_wrapper.py", then parallelly run config: "cl_wrapper: connect"
1. run "dump_database.ps1" to check "db.sqlite3" content

## TODO
1. remove pyinstaller, use bat
1. detect run dir, filter files
1. auto update deleted files
