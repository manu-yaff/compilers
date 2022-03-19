print('Ingresa el nombre del archivo que contiene el input:')
file = input()
input_file = open('test_cases/' + file, 'r')
lines = input_file.readlines()

non_terminals = []
temp_terminal = []

# read lines from file
for index, line in enumerate(lines):
  if (index != 0):
    line = line
    splitted = line.split('->')
    non_terminals.append(splitted[0].strip())
    temp_terminal.append(splitted[1].strip())

# split terminals
terminals = []
for item in temp_terminal:
  if (item != "' '"):
    for element in item.split():
      terminals.append(element)

# delete duplicates
non_terminals = list(dict.fromkeys(non_terminals))
terminals = list(dict.fromkeys(terminals))

# deleting false terminals
items_to_delete = []
for item in terminals:
  if(non_terminals.count(item)):
    items_to_delete.append(item)

for item in items_to_delete:
  terminals.remove(item)

formatted_terminals = ", ".join(map(str, terminals))
print('Terminal:', formatted_terminals)

formatted_non_terminals = ", ".join(map(str, non_terminals))
print('Non terminal:', formatted_non_terminals)
