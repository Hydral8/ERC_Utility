from ast import arg
import os
import argparse
from pathlib import Path

print("HI")

def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Pull ortholog names from ortholog protein set"
    )
    parser.add_argument(
        "-d", "--directory"
    )
    parser.add_argument(
        "-o", "--output_file"
    )
    return parser

def main():
    parser = init_argparse()
    args = parser.parse_args()
    cur_dir = args.directory
    output_file = args.output_file

    n = 0
    entries = Path(cur_dir)
    with open(output_file, "w") as f:
        for entry in entries.iterdir():
            if('.fa' in entry.name):
                n += 1
                # name = entry.name.split('.fa')[0]
                # f.write(name + "\n")
    print(n)
                
main()