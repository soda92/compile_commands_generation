# Write-Host $PSScriptRoot
# Write-Host $PWD
python $PSScriptRoot\..\generate_compile_commands.py --path $PWD
