# compile_commands_generation

Install:

1. download https://github.com/71/scoop-better-shimexe and compile shim.exe
1. open VS Directory (VS2008/VC9: C:/Program Files (x86)/Microsoft Visual Studio 9.0/VC/bin/)
1. rename cl.exe to cl2.exe
1. copy shim.exe to VS Directory as cl.exe
1. back to repo directory
1. run init_wrapper_config.py, this will set database location
1. run build_exe.py
1. add repo_directory/dist to PATH
1. fully rebuild programs to record compile commands
1. in project path, run generate_compile_commands.exe, 
it will select compile commands for current folder and generate "compile_commands.json"
