"""
Program that takes a grammar as input and produce the terminal and non terminal
symbols

Input example:
8
E -> T EPrime
EPrime -> + T EPrime
EPrime -> ' '
T -> F TPrime
TPrime -> * F TPrime
TPrime -> ' '
F -> ( E )
F -> id

Output example:
Terminal: +, *, (, ), id
Non terminal: E, EPrime T, TPrime, F


Author: Manuel Yafté
"""

# read input filename
print('Ingresa el nombre del archivo que contiene el input:')
print("['input1.txt', 'input2.txt', 'input3.txt', 'input4.txt', 'input5.txt']")
file = input()
input_file = open('test_cases/' + file, 'r')
lines = input_file.readlines()

# list to store the initial terminals and non_terminals
non_terminals = []
temp_terminal = []

# read lines from file
for index, line in enumerate(lines):
  if (index != 0):
    line = line
    splitted = line.split('->')
    non_terminals.append(splitted[0].strip())
    temp_terminal.append(splitted[1].strip())

# split terminals and added them to a list
terminals = []
for item in temp_terminal:
  if (item != "' '"):
    for element in item.split():
      terminals.append(element)

# remove duplicates from both lists
non_terminals = list(dict.fromkeys(non_terminals))
terminals = list(dict.fromkeys(terminals))

# remove 'false' terminals
items_to_delete = []
for item in terminals:
  if(non_terminals.count(item)):
    items_to_delete.append(item)

for item in items_to_delete:
  terminals.remove(item)

# format the output
formatted_terminals = ", ".join(map(str, terminals))
print('Terminal:', formatted_terminals)

formatted_non_terminals = ", ".join(map(str, non_terminals))
print('Non terminal:', formatted_non_terminals)
