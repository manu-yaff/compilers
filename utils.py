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
    header = "<tr style='border: 1px solid black'>\n<td style='border: 1px solid black'></td>\n"
    for non_terminal in table:
        for terminal in table[non_terminal]:
            header += f"<td style='border: 1px solid black'>{terminal}</td>\n"
        break
    header += '</tr>\n'

    html_table = '<table>\n' + header
    row = ""
    for non_terminal in table:
        row += "<tr>\n"
        for index, terminal in enumerate(table[non_terminal]):
            if (index == 0):
                row += f"\t<td style='border: 1px solid black'>{non_terminal}</td>\n"
            row += f"\t<td style='border: 1px solid black'>{table[non_terminal][terminal]}</td>\n"
        row += "</tr>\n"
    html_table += row
    html_table += '\n</table>'
    return html_table


def write_file(content):
    f = open("output.html", "w")
    f.write(content)
    f.close()

def generate_parsing_table(terminals, non_terminals, rules):
    table = {}
    temp = {}
    for non_terminal in non_terminals:
        for terminal in terminals:
            if terminal != 'epsilon':
                temp[terminal] = 'x'
        temp['$'] = 'x'
        table[non_terminal] = temp
        temp = {}

    for rule in rules:
        non_terminal = rule['left_side']
        first_set = generate_first_set(non_terminal, rules, terminals, 0, [])
        if ('epsilon' in first_set):
            first_set.remove('epsilon')
            epsilon_rule = { "left_side": non_terminal, "right_side": "0" }
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

    return table

def process_string(string, parsing_table, first_rule, terminals):
    stack = ['$', first_rule['left_side']]
    current_input = string.split()
    current_input.append('$')
    counter = 0
    while len(current_input) > 0:
        stack_length = len(stack)
        counter += 1
        stack_top = stack[stack_length - 1]
        if (stack_top == current_input[0]):
            current_input.pop(0)
            stack.pop()
        elif (stack_top in terminals and current_input[0] in terminals):
            return False
        else:
            stack.pop()
            # print(stack_top, current_input[0])
            # print(parsing_table[stack_top][current_input[0]])
            temp_output = parsing_table[stack_top][current_input[0]]
            if (temp_output == 'x'):
                return False
            else:
                if (temp_output.split('->')[1].strip() != '0'):
                    output = parsing_table[stack_top][current_input[0]].split('->')[1].strip().split()
                    output.reverse()
                    stack.extend(output)
                # print('this is the output', output)
                # print('al stack', output)
            # if (stack_top != 'x'):
            #     print('this is the last output', parsing_table[stack_top][current_input[0]])
            #     output = parsing_table[stack_top][current_input[0]].split('->')[1].strip().split()
            #     if (output == 'x'):
            #         stack.pop()
            #     else:
            #         output.reverse()
            #         stack.extend(output)
        # print(stack, '->', current_input, '->', output)

    if (len(stack) == 0 and len(current_input) == 0):
        return True
    else:
        return False


def evaluate_strings(strings, parsing_table, first_rule, terminals):
    for string in strings:
        result = process_string(string[:-1], parsing_table, first_rule, terminals)
        print(result)



