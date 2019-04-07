#!/usr/bin/python3
import argparse

parser = argparse.ArgumentParser(description='Generate a template for ECSC write-ups')
parser.add_argument('-n', '--name', type=str, help='Challenge name')
parser.add_argument('-p', '--points', type=str, help='Points awarded for challenge')
parser.add_argument('-c', '--category', type=str, help='Category')
parser.add_argument('-f', '--flag', type=str, help='Flag')

args = parser.parse_args()

if args.name is None or args.points is None or args.category is None:
    parser.print_help()
    exit()

template = f'''
# ECSC 2019
**Author: Moga Tudor - alexmoga69@yahoo.com - SoulTaku**

## {args.name} ({args.points}): {args.category}

### Proof of flag
>* {args.flag}

### Summary
>* <explanation>

### Proof of solving
>* <detailed explanation>
'''

open(args.name + '.md', 'w').write(template)
