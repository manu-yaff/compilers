"""
Program that takes a grammar as input and produce the terminal and non terminal
symbols

Input example:
Output example:


Author: Manuel Yafté
"""
from utils import *

def main():
    print_menu()
    lines = read_file()
    rules = read_rules(lines)
    non_terminals = read_non_terminals(lines)
    terminals = read_terminals(lines, non_terminals)

    # for non_terminal in non_terminals:
    #     print(non_terminal, end=" => ")
    #     print('FIRST =', generate_first_set(non_terminal, rules, terminals, 0, []), end=",")
    #     print(" FOLLOW = ", end="")
    #     print(generate_follow_set(non_terminal, rules, 0, [], terminals))

    table = generate_parsing_table(terminals, non_terminals, rules)
    # print(table)
    formatted_table = format_table(table, terminals)
    write_file(formatted_table)





main()

