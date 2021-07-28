# Analytic derivatives adding function for OpenMDAO

@Author Arthur Ammeux (ISAE-SUPAERO DCAS)

## How to use the function

- Place the __deriv__ folder in your current directory

- open a terminal

- type: python deriv/add_derivative.py [-h] [-dir DIR] [-outfile OUTFILE] [-outdir OUTDIR] [-check CHECK] file

- [-h] will show you help, file is the path to the .py file that you want to ass dereivatives to (.py has to be included), [-dir] is a boolean and if true you can apply the function to a directory, the function will therefore be applied to all files in the directory (the file argument is now the path to the chosen directory), [-outfile] and [-outdir] allow you to choose names for the output file or directory [-outfile] is written without exention

- This function only works on om.ExplicitComponent with at least a setup function and a compute function 
