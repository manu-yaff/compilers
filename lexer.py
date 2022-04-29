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
from turtle import right


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
    if (productions[counter]['right_side'][0] in terminals):
      # print('es un terminal')
      first.append(productions[counter]['right_side'][0])
      return generate_first_set(non_terminal, productions, terminals, counter + 1, first)
    else:
      return generate_first_set(productions[counter]['right_side'][0], productions, terminals, counter + 1, first)
  else:
    return generate_first_set(non_terminal, productions, terminals, counter + 1, first)
  


def generate_follow_set(non_terminal, productions, counter, follow):
  if (counter > (len(productions)-1)):
    print('follow:', set(follow))
    return set(follow)
  
  right_side = productions[counter]['right_side']
  right_side_size = len(right_side)
  if (productions[0]['left_side'] == non_terminal):
    follow.append('$')
  for index, symbol in enumerate(right_side):
    # print(symbol)
    if (symbol == non_terminal):
      # check it has something in front
      if (index == right_side_size - 1 and non_terminal != productions[counter]['left_side']):
        # print('no tiene algo enfrente', non_terminal)
        # print(productions[counter]['left_side'])
        generate_follow_set(productions[counter]['left_side'], productions, 0, follow)
      elif ((index < right_side_size - 1)):
        if (right_side[index + 1] in terminals):
          # print('terminal al frente', right_side[index+1])
          follow.append(right_side[index+1])
        else:
          # print('tiene el siguiente no terminal', right_side[index+1])
          result = generate_first_set(right_side[index+1], productions, terminals, 0, [])
          # print('this is result: ',result)
          follow.extend(result)
          if ('epsilon' in result):
           follow.remove('epsilon')
      #   # print('tiene un epsilon')
      #   # elimnar el que esta a la derecha
      #   # llamar el follow del que esta a index + 1
          if (index + 2 > right_side_size - 1):
            generate_follow_set(productions[counter]['left_side'], productions, 0, follow)
    # else:
      # return generate_follow_set(non_terminal, productions, counter + 1, follow)
  generate_follow_set(non_terminal, productions, counter + 1, follow)
        

  # for index_production, production in enumerate(productions):
  #   right_side = production['right_side']
  #   right_side_size = len(right_side)
  #   if (index_production == 0):
  #     follow.append('$')
  #   for index, symbol in enumerate(right_side):
  #     # print(symbol)
  #     if (symbol == non_terminal):
  #       # print('this is index: ', index, symbol)
  #       # check it has something in front
  #       if (index == right_side_size - 1 and non_terminal != production['left_side']):
  #         # print('no tiene nada en frente', non_terminal)
  #         generate_follow_set(production['left_side'], productions, follow, first)

  #       # check if the one in front is terminal
  #       elif (index < right_side_size and (right_side[index + 1] in terminals)):
  #         # print('tiene un terminal en frente', right_side[index+1])
  #         follow.append(right_side[index+1])
  #       else:
  #         # print('tiene un no terminal')
  #         result =  generate_first_set(right_side[index+1], productions, terminals, index + 1, first)
  #         follow.extend(result)
  #         if ('epsilon' in result):
  #           follow.remove('epsilon')
  #           # print('tiene un epsilon')
  #           # elimnar el que esta a la derecha
  #           # llamar el follow del que esta a index + 1
  #           if (index + 2 > right_side_size - 1):
  #             return generate_follow_set(production['left_side'], productions, follow, first)

  # return set(follow)


print_menu()
lines = read_file()
rules = read_rules(lines)
non_terminals = read_non_terminals(lines)
terminals = read_terminals(lines, non_terminals)
# print(terminals)
# # print(rules)


# generate_first_set(rules[6]['left_side'], rules, terminals, 0, [])

# for non_terminal in non_terminals:
  # print(non_terminal, generate_first_set(non_terminal, rules, terminals, 0, []))
  # generate_follow_set(non_terminal, rules, [], [])


# print('\nFOLLOW: ')

# print(generate_follow_set('E', rules, 0, []))
# print(generate_follow_set('EPrime', rules, 0, []))
# print(generate_follow_set('T', rules, 0, []))
# print(generate_follow_set('TPrime', rules, 0, []))
# print(generate_follow_set('F', rules, 0, []))

# print(generate_follow_set('E', rules, 0, []))
# print(generate_follow_set('T', rules, 0, []))
# print(generate_follow_set('F', rules, 0, []))


# print(generate_follow_set('A', rules, 0, []))
# print(generate_follow_set('B', rules, 0, []))
# print(generate_follow_set('C', rules, 0, []))
# print(generate_follow_set('D', rules, 0, []))

# print(generate_follow_set('bexpr', rules, 0, []))
# print(generate_follow_set('bterm', rules, 0, []))
# print(generate_follow_set('bfactor', rules, 0, []))

print(generate_follow_set('S', rules, 0, []))
print(generate_follow_set('A', rules, 0, []))
print(generate_follow_set('APrime', rules, 0, []))