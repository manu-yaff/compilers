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

# read terminals
def read_terminals(lines, non_terminals_set):
  terminals = []
  for index, line in enumerate(lines):
    if (index != 0):
      item = line.split('->')[1].strip()
      if (item != "' '"):
        for element in item.split():
          if(element not in non_terminals_set):
            terminals.append(element)
  return set(terminals)


print_menu()
lines = read_file()
non_terminals = read_non_terminals(lines)
print('Terminal: ', read_terminals(lines, non_terminals))
print('Non terminal: ', non_terminals)

