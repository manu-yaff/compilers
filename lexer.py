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
    if (not table):
        write_file('<div>Grammar is not LL(1)!</div>', append=False)
    else:
        formatted_table = format_table(table, terminals)
        write_file(formatted_table, append=False)
        number_strings = int(lines[0].split()[0])
        strings_to_read = lines[number_strings+1:]
        strings_result = evaluate_strings(strings_to_read, table, rules[0], terminals)
        write_file(strings_result, append=True)

    print('Archivo output.html generado')




main()

