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


    table = generate_parsing_table(terminals, non_terminals, rules)
    for item in table:
        for x in table[item]:
            print(f"table[{item}][{x}] = {table[item][x]}")
    formatted_table = format_table(table, terminals)
    write_file(formatted_table)



main()

