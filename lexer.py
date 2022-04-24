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

# function to print menu
def print_menu():
  print('Ingresa el nombre del archivo que contiene el input:')
  print("['input1.txt', 'input2.txt', 'input3.txt', 'input4.txt', 'input5.txt']")


# function to read files
def read_file():
  file_name = input()
  input_file = open('test_cases/' + file_name, 'r')
  return input_file.readlines()

  
# read non-terminals
def read_non_terminals(lines):
  non_terminals = []
  for index, line in enumerate(lines):
    if (index!= 0):
      terminal = line.split('->')[0].strip()
      non_terminals.append(terminal)


  return set(non_terminals)


print_menu()
lines = read_file()
print(read_non_terminals(lines))


# # read lines from file
# for index, line in enumerate(lines):
#   if (index != 0):
#     line = line
#     splitted = line.split('->')
#     non_terminals.append(splitted[0].strip())
#     temp_terminal.append(splitted[1].strip())

# # split terminals and added them to a list
# terminals = []
# for item in temp_terminal:
#   if (item != "' '"):
#     for element in item.split():
#       terminals.append(element)

# # remove duplicates from both lists
# non_terminals = list(dict.fromkeys(non_terminals))
# terminals = list(dict.fromkeys(terminals))

# # remove 'false' terminals
# items_to_delete = []
# for item in terminals:
#   if(non_terminals.count(item)):
#     items_to_delete.append(item)

# for item in items_to_delete:
#   terminals.remove(item)

# # format the output
# formatted_terminals = ", ".join(map(str, terminals))
# print('Terminal:', formatted_terminals)

# formatted_non_terminals = ", ".join(map(str, non_terminals))
# print('Non terminal:', formatted_non_terminals)
