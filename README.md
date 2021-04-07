# OpenMDAO_class_generator

@Author Arthur Ammeux

Generates code to make OpenMDAO components and groups

# How to use the program ?

- Launch Ipyvuetify GUI in the src folder 

- Run the first block of code

- Specify if you want to generate only om.Component code or om.Group and om.Component

- If you select om.Component: use a hashtag followed by a space as a prefix to your component's names, you should write your component's names and then your equations after a line break

- If you select om.Group: use double hashtags followed by a space as a prefix to your group's names (prefix for components is stated above), you should write your group's name and then break the line and write your components as stated above

- The equations syntax has to be understandable by python (* to multiply, / to divide ...), variables do not need to be declared, you should only write one equation per line and your equations should be in logical order. Functions are supported by the program and this means that a variable containing parentheses will not be recognised

- Examples of correct syntax are available in Ipyvuetify GUI in the second and third blocks of code

- When you have selected the right type and typed all your equations you can press the 'print code' button, it will print the code for all your om.Components/om.Groups
