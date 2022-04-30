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
from turtle import left, right


def print_menu():
  """
  This function prints the menu to select the file
  """
  print('Ingresa el nombre del archivo que contiene el input:')
  print("['input1.txt', 'input2.txt', 'input3.txt', 'input4.txt', 'input5.txt']")


# function to read files
def read_file():
  """
  This function reads the test case file according to the name specified
  """
  file_name = input()
  input_file = open('test_cases/' + file_name, 'r')
  return input_file.readlines()

  
# read non-terminals
def read_non_terminals(lines):
  """This function determines the non-terminals symbols of the grammar"""
  non_terminals = []
  for index, line in enumerate(lines):
    if (index!= 0):
      terminal = line.split('->')[0].strip()
      non_terminals.append(terminal)
  return set(non_terminals)

# read terminals
def read_terminals(lines, non_terminals_set):
  """This function determines the terminals symbols of the grammar"""
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
  """This function reads the lines from the file and store the information as an array of objects"""
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
  """This function generates the FIRST set for a non_terminal"""
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
  

# generate FOLLOW Set
def generate_follow_set(non_terminal, productions, counter, follow):
  """This function generates the FOLLOW set for a non_terminal"""
  if (counter > (len(productions)-1)):
    # print('follow:', set(follow))
    return set(follow)
  
  right_side = productions[counter]['right_side']
  right_side_size = len(right_side)
  if (productions[0]['left_side'] == non_terminal):
    follow.append('$')
  for index, symbol in enumerate(right_side):
    if (symbol == non_terminal):
      # check it has something in front
      if (index == right_side_size - 1 and non_terminal != productions[counter]['left_side']):
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
      #   # elimnar el que esta a la derecha
      #   # llamar el follow del que esta a index + 1
          if (index + 2 > right_side_size - 1):
            generate_follow_set(productions[counter]['left_side'], productions, 0, follow)
    # else:
      # return generate_follow_set(non_terminal, productions, counter + 1, follow)
  return generate_follow_set(non_terminal, productions, counter + 1, follow)
        

# get terminals that have more than 1 production
def filter_non_terminals(non_terminals, productions):
  """This function gets the non-terminals with more than one production"""
  filtered = []
  counter = 0
  for non_terminal in non_terminals:
    for production in productions:
      left_side = production['left_side']
      right_side = production['right_side']
      if (left_side == non_terminal):
        counter += 1
        if (counter > 1):
          filtered.append(non_terminal)
    counter = 0
  return set(filtered) 


# check if productions start width different symbol 
def check_start_diff_symbol(non_terminal, productions, terminals):
  """ This function checks if the start symbols are different for all rules of a non_terminal"""
  visited = set()
  counter = 0
  for index, production in enumerate(productions):
    left_side = production['left_side']
    right_side = production['right_side']
    if (left_side == non_terminal):
      counter += 1
      if (right_side[0] in visited):
        return False
      visited.add(right_side[0])
  
    if (right_side[0] == left_side):
      return False
    if(index == 0 and right_side[0] == productions[index + 2]['left_side']):
     return False 
  return True

# check each rule has at most one epsilon
def check_at_most_one_epislon(non_terminal, productions):
  """ This function checks if there's at most one epislon"""
  counter = 0
  for production in productions:
    left_side = production['left_side']
    right_side = production['right_side']
    if (left_side == non_terminal):
      if(right_side[0] == 'epsilon'):
        counter += 1
  return counter <= 1

# check that intersection of FIRST and FOLLOW set is null
def check_sets_intersection_is_null(non_terminal, productions, terminals):
  """ This function checks if the first and follow intersection is null"""
  first = generate_first_set(non_terminal, productions, terminals, 0, [])
  follow = generate_follow_set(non_terminal, productions, 0, [])
  for element in first:
    if (element in follow):
      return False
  return True

# check if three rules are met
def check_ll1(productions, non_terminals, terminals):
  """ This function checks if the grammar is LL(1) based on the 3 rules required"""
  for non_terminal in non_terminals:
    if(not check_start_diff_symbol(non_terminal, productions, terminals)):
      return False
    
    if(not check_at_most_one_epislon(non_terminal, productions)):
      return False

    if(not check_sets_intersection_is_null(non_terminals, productions, terminals)):
      return False
  
  return True
  
print_menu()
lines = read_file()
rules = read_rules(lines)
non_terminals = read_non_terminals(lines)
terminals = read_terminals(lines, non_terminals)

for non_terminal in non_terminals:
  print(non_terminal, end=" => ")
  print('FIRST =', generate_first_set(non_terminal, rules, terminals, 0, []), end=",")
  print(" FOLLOW = ", end="")
  print(generate_follow_set(non_terminal, rules, 0, []))

filtered_non_terminals = filter_non_terminals(non_terminals, rules)
print('LL(1)?', end=" ")
print('Yes') if check_ll1(rules, filtered_non_terminals, terminals) else print('No')