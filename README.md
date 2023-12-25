# compile_commands_generation

## Install
1. run `init_shim_config.py`, this will set database location
1. add `repo_directory/bin` to PATH
1. fully rebuild programs to record compile commands
1. in project path, run `generate_cc.bat`, 
it will select compile commands for current folder and generate "compile_commands.json"

## Debugging

1. Run debug config: "Test VS2019", it'll stop at compile
1. place breakpoints at "cl_wrapper.py", then parallelly run config: "cl_wrapper: connect"
1. use DBeaver to check Database
