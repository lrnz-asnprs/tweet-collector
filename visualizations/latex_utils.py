import json
from drivers.configs.directories import Directories
dir = Directories()
from random import randint

def read_json(path, filename):
    with open(path+filename, "r") as fp:
        return json.load(fp)

def create_variables(variables, to_latex=True):
    """Takes a json object of variables and transforms them into the format necessary in latex for variables to be accessible 
    Args:
        variables (dictionary): Should contain the variable's ref-name as key. and value of variable as value. 
        Can also contain a description which will be put in as a comment in Latex
    """ 
    
    lst = []   
    for key, value in variables.items(): 
        variable_statement = "\\newcommand{" + "\\" + key + "}{" + str(value["value"]) + "}"
        
        if 'description' in value:
            description = " % " + value['description']
        else:
            description = ""

        lst.append(variable_statement + description)
    
    if to_latex:
        with open(str(dir.LATEX_VARIABLES_PATH) + "/" + "variables_" + str(randint(0,9999)) + ".tex", "w") as fp:
            for i in lst:
                fp.write(i + "\n")
    
    return lst

