# function to print menu
def print_menu():
    """
    This function prints the menu to select the file
    """
    # print('Ingresa el nombre del archivo que contiene el input:')
    # print("['input1.txt', 'input2.txt', 'input3.txt', 'input4.txt', 'input5.txt']")


# function to read files
def read_file():
    """
    This function reads the test case file according to the name specified
    """
    # file_name = input()
    # input_file = open('test_cases/' + file_name, 'r')
    input_file = open('test_cases/input1.txt', 'r')
    return input_file.readlines()


# read non-terminals
def read_non_terminals(lines):
    """This function determines the non-terminals symbols of the grammar"""
    non_terminals = []
    rules_number = int(lines[0][0]) + 1
    for index, line in enumerate(lines):
        if (index != 0 and index < rules_number):
            terminal = line.split('->')[0].strip()
            non_terminals.append(terminal)
    return set(non_terminals)

def read_terminals(lines, non_terminals_set):
    """This function determines the terminals symbols of the grammar"""
    terminals = []
    rules_number = int(lines[0][0]) + 1
    for index, line in enumerate(lines):
        if (index != 0 and index < rules_number):
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
    rules_number = int(lines[0][0]) + 1
    for index, line in enumerate(lines):
        if (index != 0 and index < rules_number):
            left_side = line.split('->')[0].strip()
            right_side = line.split('->')[1].strip()
            if (right_side == "' '"):
                lines_formatted.append({ "left_side": left_side, "right_side": ["epsilon"] })
            else:
                lines_formatted.append({ "left_side": left_side,  "right_side": right_side.split() })
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
def generate_follow_set(non_terminal, productions, counter, follow, terminals):
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
                generate_follow_set(
                    productions[counter]['left_side'], productions, 0, follow, terminals)
            elif ((index < right_side_size - 1)):
                if (right_side[index + 1] in terminals):
                    # print('terminal al frente', right_side[index+1])
                    follow.append(right_side[index+1])
                else:
                    # print('tiene el siguiente no terminal', right_side[index+1])
                    result = generate_first_set(
                        right_side[index+1], productions, terminals, 0, [])
                    # print('this is result: ',result)
                    follow.extend(result)
                    if ('epsilon' in result):
                        follow.remove('epsilon')
            #   # elimnar el que esta a la derecha
            #   # llamar el follow del que esta a index + 1
                    if (index + 2 > right_side_size - 1):
                        generate_follow_set(
                            productions[counter]['left_side'], productions, 0, follow, terminals)
        # else:
            # return generate_follow_set(non_terminal, productions, counter + 1, follow)
    return generate_follow_set(non_terminal, productions, counter + 1, follow, terminals)

def fill_table_row(non_terminal, rule, cols, table):
    formatted_rule = rule['left_side'] + ' -> ' + ' '.join(rule['right_side'])
    for col in cols:
        table[non_terminal][col] = formatted_rule

def format_table(table, terminals):
    for index, non_terminal in enumerate(table):
        row = "<tr>\n"
        for terminal in table[non_terminal]:
            row += f"\t<td>{table[non_terminal][terminal]}</td>\n"
            # print(table[non_terminal][terminal], end = "|")
        row += "</tr>\n"
        print('\n', row)
        row = ""


def write_file(content):
    f = open("output.html", "w")
    f.write(content)
    f.close()

def generate_parsing_table(terminals, non_terminals, rules):
    table = {}
    temp = {}
    counter = 0
    print(non_terminals)
    for non_terminal in non_terminals:
        for terminal in terminals:
            if terminal != 'epsilon':
                temp[terminal] = 'x'
            counter += 1
        temp['$'] = 'x'
        table[non_terminal] = temp
        temp = {}

    counter = 0
    for item in table:
        for x in table[item]:
            counter += 1
            print(f"{counter} - table[{item}][{x}] = {table[item][x]}")
    print('--------------------')

    for rule in rules:
        non_terminal = rule['left_side']
        first_set = generate_first_set(non_terminal, rules, terminals, 0, [])
        if ('epsilon' in first_set):
            first_set.remove('epsilon')
            epsilon_rule = { "left_side": non_terminal, "right_side": 'epsilon' }
            follow_set = generate_follow_set(non_terminal, rules, 0, [], terminals)
            if (rule['right_side'][0] == 'epsilon'):
                fill_table_row(non_terminal, epsilon_rule, follow_set, table)
            else:
                fill_table_row(non_terminal, rule, first_set, table)
        else:
            if(rule['right_side'][0] in terminals):
                # print('aqui: ', rule['right_side'])
                if(len(rule['right_side']) > 1):
                    new_rule = rule['right_side'][0]
                else:
                    new_rule = rule['right_side']
                fill_table_row(non_terminal, rule, set(new_rule), table)
            else:
                fill_table_row(non_terminal, rule, first_set, table)

    counter = 0
    for item in table:
        for x in table[item]:
            counter += 1
            print(f"{counter} - table[{item}][{x}] = {table[item][x]}")
    return table


# print_menu()
# lines = read_file()
# rules = read_rules(lines)
# non_terminals = read_non_terminals(lines)
# terminals = read_terminals(lines, non_terminals)
# table = generate_parsing_table(terminals, non_terminals, rules)
# print(table)
# for non_terminal in non_terminals:
#   print(non_terminal, end=" => ")
#   print('FIRST =', generate_first_set(non_terminal, rules, terminals, 0, []), end=",")
#   print(" FOLLOW = ", end="")
#   print(generate_follow_set(non_terminal, rules, 0, []))

# filtered_non_terminals = filter_non_terminals(non_terminals, rules)
# print('LL(1)?', end=" ")
# print('Yes') if check_ll1(rules, filtered_non_terminals, terminals) else print('No')
