# FSMD Simulator - README

## What is this?

This is a simulator for FSMD (Finite State Machine with Datapath). An FSMD is a type of state machine that can also perform calculations and store data in variables.

## What does it do?

The simulator reads an FSMD description from an XML file and runs it step by step. It shows you:
- What state the machine is in
- What the inputs are
- What the variables contain
- Which transitions happen and why

## How to run it
For test 2:
python3 fsmd-sim.py 100 ./test_2/gcd_desc.xml ./test_2/gcd_stim.xml

For test 3:
python3 fsmd-sim.py 300 ./test_3/test3_desc.xml ./test_3/test3_stim.xml

### Parameters:
- **number_of_cycles**: How many cycles to run the simulation
- **description_file**: XML file that describes your FSMD (states, transitions, operations, etc.)
- **stimuli_file**: (Optional) XML file that provides input values at specific cycles

### Examples:

Run for 10 cycles with just a description file:
```
python3 fsmd-sim.py 10 test_1/test_desc.xml
```

Run for 20 cycles with both description and stimuli files:
```
python3 fsmd-sim.py 20 test_2/gcd_desc.xml test_2/gcd_stim.xml
```

## What's in the XML files?

### Description File
Contains:
- **States**: All possible states of the machine
- **Initial State**: Where the machine starts
- **Inputs**: External values that can be read
- **Variables**: Internal storage for calculations
- **Operations**: Calculations that can be performed (like `a = a + b`)
- **Conditions**: Tests that determine which transition to take (like `a > b`)
- **Transitions**: Rules for moving between states

### Stimuli File (Optional)
Contains:
- **setinput**: Changes input values at specific cycles
- **endstate**: Tells the simulator to stop when reaching a certain state

## What you'll see

When you run the simulator, it will show:
1. A summary of your FSMD (all states, inputs, variables, operations, conditions, transitions)
2. For each cycle:
   - Current cycle number
   - Current state
   - Input values (if any)
   - Which condition was true
   - Which instruction was executed
   - What the next state is
   - Variable values at the end of the cycle
3. When the simulation ends

## Stopping the simulation

The simulation stops when:
- It reaches the specified number of cycles, OR
- It reaches the end state (if specified in the stimuli file)

## Example Output

```
Cycle = 0
Current state = Start
Inputs: 
  x = 5
The condition (x > 0) is true.
Executing instruction = decrement
Next state = Loop
At the end of the cycle 0 execution, the status is: 
Variables: 
  counter = 4
-------------------------------------------------------------------
```

## Need help?

Make sure your XML files are properly formatted and all required elements are present in the description file.
