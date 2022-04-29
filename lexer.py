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
      else:
        terminals.append("epsilon")
  return set(terminals)

# read grammar rules and replace epsilon ocurrences
def read_rules(lines):
  lines_formatted = []
  for index, line in enumerate(lines):
    if (index != 0):
      left_side = line.split('->')[0].strip()
      right_side = line.split('->')[1].strip()
      if (right_side == "' '"):
        lines_formatted.append({ "left_side": left_side, "right_side": ["epsilon"] })
      else:
        lines_formatted.append({ "left_side": left_side,  "right_side": right_side.split() })
  # need to format the symbols as arrays
  return lines_formatted

# generate FIRST Set
def generate_first_set(non_terminal, productions, terminals, counter, first):
  # print(len(productions))
  if (counter > len(productions)-1):
    # print(first)
    return set(first)
  
  if (productions[counter]['left_side'] == non_terminal):
    # aqui abajo esta el problema
    if (productions[counter]['right_side'][0] in terminals):
      # print('es un terminal')
      first.append(productions[counter]['right_side'][0])
      return generate_first_set(non_terminal, productions, terminals, counter + 1, first)
    else:
      return generate_first_set(productions[counter]['right_side'][0], productions, terminals, counter + 1, first)
  else:
    return generate_first_set(non_terminal, productions, terminals, counter + 1, first)
  
  # if (productions[counter]['left_side'] == symbol):
  #   if (productions[counter]['left_side'] in terminals):
  #     print(symbol)
  #   else:
  #     print('llamada con, ', productions[counter]['right_side'][0], counter + 1)
  # else:
  #   print('llamada con, ', symbol, productions, terminals, counter + 1)





  # first = []
  # symbol = rule["right_side"][0]
  # if (symbol in terminals and ):
  #   first.append(symbol)
  # else:
  #   generate_first_set(productions[i + 1], productions, terminals)

  # print(first)
  



print_menu()
lines = read_file()
rules = read_rules(lines)
non_terminals = read_non_terminals(lines)
terminals = read_terminals(lines, non_terminals)
# print(terminals)
# # print(rules)


# generate_first_set(rules[6]['left_side'], rules, terminals, 0, [])

for non_terminal in non_terminals:
  print(non_terminal, generate_first_set(non_terminal, rules, terminals, 0, []))



# print('Non terminals: ', non_terminals)
# print('Terminals: ', terminals)

# generate_first_set(grammar_rules, terminals, non_terminals)
