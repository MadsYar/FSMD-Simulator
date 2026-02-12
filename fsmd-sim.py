#!/usr/bin/env python3

import sys
import xmltodict

print("Welcome to the FSMD simulator!")

if len(sys.argv) < 3:
    print('Too few arguments.')
    sys.exit(-1)
elif (len(sys.argv) >4):
    print('Too many arguments.')
    sys.exit(-1)

iterations = int(sys.argv[1])

#Parsing the FSMD description file
with open(sys.argv[2]) as fd:
    fsmd_des = xmltodict.parse(fd.read())

#Parsing the stimuli file
fsmd_stim = {}
if len(sys.argv) == 4:
    with open(sys.argv[3]) as fd:
        fsmd_stim = xmltodict.parse(fd.read())

print("\n--FSMD description--")

#
# Description:
# The 'states' variable of type 'list' contains the list of all states names.
#
states = fsmd_des['fsmddescription']['statelist']['state']
print("States:")
for state in states:
    print('  ' + state)
#
# Description:
# The 'initial_state' variable of type 'string' contains the initial_state name.
#
initial_state = fsmd_des['fsmddescription']['initialstate']
print("Initial state:")
print('  ' + initial_state)

#
# Description:
# The 'inputs' variable of type 'dictionary' contains the list of all inputs
# names and value. The default value is 0.
#
inputs = {}
if(fsmd_des['fsmddescription']['inputlist'] is None):
    inputs = {}
    #No elements
else:
    if type(fsmd_des['fsmddescription']['inputlist']['input']) is str:
        # One element
        inputs[fsmd_des['fsmddescription']['inputlist']['input']] = 0
    else:
        # More elements
        for input_i in fsmd_des['fsmddescription']['inputlist']['input']:
            inputs[input_i] = 0
print("Inputs:")
for input_i in inputs:
    print('  ' + input_i)

#
# Description:
# The 'variables' variable of type 'dictionary' contains the list of all variables
# names and value. The default value is 0.
#
variables = {}
if(fsmd_des['fsmddescription']['variablelist'] is None):
    variables = {}
    #No elements
else:
    if type(fsmd_des['fsmddescription']['variablelist']['variable']) is str:
        # One element
        variables[fsmd_des['fsmddescription']['variablelist']['variable']] = 0
    else:
        # More elements
        for variable in fsmd_des['fsmddescription']['variablelist']['variable']:
            variables[variable] = 0
print("Variables:")
for variable in variables:
    print('  ' + variable)

#
# Description:
# The 'operations' variable of type 'dictionary' contains the list of all the
# defined operations names and expressions.
#
operations = {}
if(fsmd_des['fsmddescription']['operationlist'] is None):
    operations = {}
    #No elements
else:
    for operation in fsmd_des['fsmddescription']['operationlist']['operation']:
        if type(operation) is str:
            # Only one element
            operations[fsmd_des['fsmddescription']['operationlist']['operation']['name']] = \
                fsmd_des['fsmddescription']['operationlist']['operation']['expression']
            break
        else:
            # More than 1 element
            operations[operation['name']] = operation['expression']
print("Operations:")
for operation in operations:
    print('  ' + operation + ' : ' + operations[operation])

#
# Description:
# The 'conditions' variable of type 'dictionary' contains the list of all the
# defined conditions names and expressions.
#
conditions = {}
if(fsmd_des['fsmddescription']['conditionlist'] is None):
    conditions = {}
    #No elements
else:
    for condition in fsmd_des['fsmddescription']['conditionlist']['condition']:
        if type(condition) is str:
            #Only one element
            conditions[fsmd_des['fsmddescription']['conditionlist']['condition']['name']] = fsmd_des['fsmddescription']['conditionlist']['condition']['expression']
            break
        else:
            #More than 1 element
            conditions[condition['name']] = condition['expression']
print("Conditions:")
for condition in conditions:
    print('  ' + condition + ' : ' + conditions[condition])

#
# Description:
# The 'fsmd' variable of type 'dictionary' contains the list of dictionaries,
# one per state, with the fields 'condition', 'instruction', and 'nextstate'
# describing the FSMD transition table.
#
fsmd = {}
for state in states:
    fsmd[state] = []
    for transition in fsmd_des['fsmddescription']['fsmd'][state]['transition']:
        if type(transition) is str:
            #Only one element
            fsmd[state].append({'condition': fsmd_des['fsmddescription']['fsmd'][state]['transition']['condition'],
                                'instruction': fsmd_des['fsmddescription']['fsmd'][state]['transition']['instruction'],
                                'nextstate': fsmd_des['fsmddescription']['fsmd'][state]['transition']['nextstate']})
            break
        else:
            #More than 1 element
            fsmd[state].append({'condition' : transition['condition'],
                                'instruction' : transition['instruction'],
                                'nextstate' : transition['nextstate']})
print("FSMD transitions table:")
for state in fsmd:
    print('  ' + state)
    for transition in fsmd[state]:
        print('    ' + 'nextstate: ' + transition['nextstate'] + ', condition: ' + transition['condition'] + ', instruction: ' + transition['instruction'])


#
# Description:
# This function executes a Python compatible operation passed as string
# on the operands stored in the dictionary 'inputs'
#
def execute_setinput(operation):
    operation_clean = operation.replace(' ', '')
    operation_split = operation_clean.split('=')
    target = operation_split[0]
    expression = operation_split[1]
    inputs[target] = eval(expression, {'__builtins__': None}, inputs)
    return


#
# Description:
# This function executes a Python compatible operation passed as string
# on the operands stored in the dictionaries 'variables' and 'inputs'
#
def execute_operation(operation):
    operation_clean = operation.replace(' ', '')
    operation_split = operation_clean.split('=')
    target = operation_split[0]
    expression = operation_split[1]
    variables[target] = eval(expression, {'__builtins__': None}, merge_dicts(variables, inputs))
    return


#
# Description:
# This function executes a list of operations passed as string and spaced by
# a single space using the expression defined in the dictionary 'operations'
#
def execute_instruction(instruction):
    if instruction == 'NOP' or instruction == 'nop':
        return
    instruction_split = instruction.split(' ')
    for operation in instruction_split:
        execute_operation(operations[operation])
    return


#
# Description:
# This function evaluates a Python compatible boolean expressions of
# conditions passed as string using the conditions defined in the variable 'conditions'
# and using the operands stored in the dictionaries 'variables' and 'inputs
# It returns True or False
#
def evaluate_condition(condition):
    if condition == 'True' or condition=='true' or condition == 1:
        return True
    if condition == 'False' or condition=='false' or condition == 0:
        return False
    condition_explicit = condition
    for element in conditions:
        condition_explicit = condition_explicit.replace(element, conditions[element])
    #print('----' + condition_explicit)
    return eval(condition_explicit, {'__builtins__': None}, merge_dicts(variables, inputs))


#
# Description:
# Support function to merge two dictionaries.
#
def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

#######################################
# Start to simulate
cycle = 0
state = initial_state

# The next 8 lines of codes prints the start variables
print('\n---Start simulation---')
print("At the start of the simulation, we have the following variables:")

for variable in variables:
    print("  " + str(variable) + " = " + str(variables[variable]))

print("Status: " + str(state))    
print("-------------------------------------------------------------------")

# Creating a var for the repeats of the simulation
if (iterations > 0):
    simulation = True

# Next 3 lines starts the simulation and prints the cycle number and current state
while(simulation):
    print("Cycle = " + str(cycle))
    print("Current state = " + str(state))
    
    # Next 14 lines is a code snip given from the assignment to update input
    try:
        if (not(fsmd_stim['fsmdstimulus']['setinput'] is None)):
            for setinput in fsmd_stim['fsmdstimulus']['setinput']:
                if type(setinput) is str:
                    #Only one element
                    if int(fsmd_stim['fsmdstimulus']['setinput']['cycle']) == cycle:
                        execute_setinput(fsmd_stim['fsmdstimulus']['setinput']['expression'])
                    break
                else:
                    #More than 1 element
                    if int(setinput['cycle']) == cycle:
                        execute_setinput(setinput['expression'])
    except:
        pass
    
    # Next 4 lines prints the input
    if inputs:
        print("Inputs: ")
        for input in inputs:
            print("  " + str(input) + " = " + str(inputs[input]))
    
    # This for loop checks the conditions and executes the correct instructions from the XML-file
    for transition in fsmd[state]:
        # Next 6 lines checks if condition = true then it executes the instruction from the XML-file
        if (evaluate_condition(transition["condition"])):
            print("The condition (" + str(transition["condition"] + ") is true."))
            print("Executing instruction = " + str(transition["instruction"]))
            print("Next state = " + str(transition["nextstate"]))
            
            execute_instruction(transition["instruction"])
            # Next 7 lines is a code snip given from the assignment to terminate if the state is equal to the end state
            try:
                if (not(fsmd_stim['fsmdstimulus']['endstate'] is None)):
                    if state == fsmd_stim['fsmdstimulus']['endstate']:
                        print('End-state reached.')
                        simulation = False
            except:
                pass
            
            # Transitioning into the next state
            state = transition["nextstate"] 

    # Next 4 lines prints the variables
    print("At the end of the cycle " + str(cycle) + " execution, the status is: ")
    print("Variables: ")
    for variable in variables:
        print("  " + str(variable) + " = " + str(variables[variable]))
    
    # Cycle counter
    cycle += 1
    if (cycle == iterations):
        simulation = False

    print("-------------------------------------------------------------------")
print("End-state reached.")
print('End of simulation.')


#
# Description:
# This is a code snippet used to update the inputs values according to the
# stimuli file content. You can see here how the 'fsmd_stim' variable is used.
#
'''
try:
    if (not(fsmd_stim['fsmdstimulus']['setinput'] is None)):
        for setinput in fsmd_stim['fsmdstimulus']['setinput']:
            if type(setinput) is str:
                #Only one element
                if int(fsmd_stim['fsmdstimulus']['setinput']['cycle']) == cycle:
                    execute_setinput(fsmd_stim['fsmdstimulus']['setinput']['expression'])
                break
            else:
                #More than 1 element
                if int(setinput['cycle']) == cycle:
                    execute_setinput(setinput['expression'])
except:
    pass
'''

#
# Description:
# This is a code snipppet used to check the endstate value according to the
# stimuli file content. You can see here how the 'fsmd_stim' variable is used.
#
'''
try:
    if (not(fsmd_stim['fsmdstimulus']['endstate'] is None)):
        if state == fsmd_stim['fsmdstimulus']['endstate']:
            print('End-state reached.')
            repeat = False
except:
    pass
'''
