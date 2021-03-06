# OpenMDAO_class_generator

@Author Arthur Ammeux (ISAE-SUPAERO DCAS)

Generates code to make OpenMDAO components and groups (implementing the om.ExplicitComponent and om.Group class)

## How to use the program ?

### Launch the program

- Launch __Ipyvuetify GUI__ in the src folder with jupyter notebook

- Run the first block of code

### Writing your equations

- Write your equations in the __Equations__ text area with the following syntax:

  - If you want to create a series of om.Component: use a hashtag and a percent followed by a space as a prefix to your component's names, you should write your component's names and then your equations after at least one line break (*Example: #% Component_1*)

  - If you want to create one or more om.Group with some om.ExplicitComponent: a hastag and two percent followed by a space as a prefix to your group's names (prefix for components is stated above), you should write your group's name and then break the line at least once and write your components as stated above (*Example: #%% Group_1*)

  - To create higher level groups (groups that will contain other groups) just use a hashtag and as many percent as the level of your group as a decorator (*Example: #%%% Higher_Group*)
the groups following in your text with the next lower level of hashtags will be added to your higher level group.

  - /!\ Your first non empty line should always be either a group or a component

  - /!\ Comments are supported but you should only use # and not begin your comment with % or [

- The equations syntax has to be understandable by python (* to multiply, / to divide ...), variables do not need to be declared, you should only write one equation per line and your equations should be in logical order. Functions are supported by the program and this means that a variable containing parentheses will not be recognised (if you are using functions from a specific package, dont forget to type the name of the package in the __Packages to import__ text area)

- You can add units to output variables by adding a # [your_unit] (the space between # and [ is not necessary) decorator at the end of the line where you define the output variable (*Example: y = x + 1 # [kg]*), this unit will still be modifiable afterwards. Comments following this decorator are supported

- Examples of correct syntax are available in __Ipyvuetify GUI__ in the second and third blocks of code

- You can then specify which packages you want to import in the generated code in the __Packages to import__ text area by simply tping regular python syntax (*import pack1, import pack2 as pk2, from pack3 import func*). To import multiple packages, just add a linebreak between them. By default numpy is imported as np, this can be necessary for the non initialized input variables as they will use "np.nan" as a default value as well as for analytic derivatives so it is strongly advised not to remove this package. Keep in mind that the imported packages will have an impact on what the program detects as constant or a function as opposed to a variable.

- There is another way to write your equations that allows you to test them before generating the code, you can simply add as many cells to the notebook as you like, write your equations in these cells and when you are done, run all your relevant cells in order and then set the __First cell__ and __Last cell__ as the number In[ ] of your first cell and last cell, finally click on the __Copy Cells__ button and all your equations will appear in the text area. To facilitate the procedure, you can use the *# Init* decorator to initialize your variables (the program will take the initial values as default values for those variables), the *# Import* decorator to import packages that will be imported in the final code and the *# Exclude* decorator to specify that the program should ignore a certain cell.

### Equation analysis and code generation

- When you have typed all your equations you can press the __Analyse__ button, it will generate a sheet with all the variables found. You can modify this sheet and change variable names, units and default values (there cannot be any default values for outputs). You can also use the __DELETE__ button on any variable to remove the specified variable from the variables detected by the program. Keep in mind that variables that are in the same group (not higher level group but lowest level group) and that have the same symbol in your equations will be linked together (if you change one's name, the other's will change and so on), the only properties that aren't linked are the deleted status and the default value for output variables

- Once you are done modifying the sheet, you can choose whether you want analytic derivatives or numerical derivatives by ticking the __checkbox__. Then you can press either the __Print code__ button which will print your code in a markdown style or the __Generate File__ button which will generate one file with all your components if you chose to write om.ExplicitComponent only or one file per highest level group if you have written om.Group, all the files are generated in the current directory and their names is either the name of the first om.ExplicitComponent or the name of the highest level group

- After you have clicked on either __Print code__ or __Generated File__, a new button __Generate n2 diagram__ will appear. It will be clickable only if your code contains groups. Once clicked, it will generate one n2 diagram for every highest level group.

- If you want to use the program again, it is necessary to re-run the first cell of __Ipyvuetify GUI__
