# OpenMDAO_class_generator

@Author Arthur Ammeux

Generates code to make OpenMDAO components and groups

## How to use the program ?

- Launch Ipyvuetify GUI in the src folder with jupyter notebook

- Run the first block of code

- Write your equations in the __Equations__ text area with the following synthax:

  - If you want to create a series of om.Component: use a hashtag followed by a space as a prefix to your component's names, you should write your component's names and then your equations after at least one line break (*Example: # Component_1*)

  - If you want to create one or more om.Group with some om.Component: use double hashtags followed by a space as a prefix to your group's names (prefix for components is stated above), you should write your group's name and then break the line at least once and write your components as stated above (*Example: ## Group_1*)

- The equations syntax has to be understandable by python (* to multiply, / to divide ...), variables do not need to be declared, you should only write one equation per line and your equations should be in logical order. Functions are supported by the program and this means that a variable containing parentheses will not be recognised

- Examples of correct syntax are available in Ipyvuetify GUI in the second and third blocks of code

- When you have typed all your equations you can press the __Analyse__ button, it will generate a sheet with all the variables found. You can modify this sheet and change variable names, units and default values (there cannot be any default values for outputs)

- Once you are done modifying the sheet, you can press either the __Print code__ button which will print your code in a markdown style or the __Generate File__ button which will generate one file with all your components if you chose to write om.Component only or one file per group if you have written multiple om.Group, all the files are generated in the current directory and their names is either the name of the first om.Component or the name of the om.Group
