import os
import argparse
from pathlib import Path
import shutil
import re

def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Pull ortholog names from ortholog protein set"
    )
    parser.add_argument("-f", "--file", help="the input fasta file")
    parser.add_argument("-d", "--input_dir", help="input directory with fasta files")
    parser.add_argument("-w", "--output_dir", help="the output dir of the dealigned fasta files")
    parser.add_argument("-s", "--suffix", help="the suffix to add on the newly generated files")
    return parser

def dealign_helper(input_file, output_dir, suffix):
    organism = ""
    sequence = ""
    data = dict()
    
    with open(input_file, 'rb') as f:
        print(input_file)
        iterator = iter(f)
        line = next(iterator).decode(errors='replace').strip()
        if(line[0] == ">"):
            organism = line[1:]
        
        while(True):
            try:
                line = next(iterator).decode(errors='replace').strip().replace("-", "")
                if line=="" or line[0] != ">":
                        sequence += line
                else:
                    if organism in data:
                        data[organism].append(sequence)
                    else: 
                        data[organism] = [sequence]
                    organism = line[1:]
                    sequence = ""   
            except:
                if organism in data:
                    data[organism].append(sequence)
                else:
                    data[organism] = [sequence]
                break

    file_name = input_file.split("/")[-1]
    if output_dir != None:
        new_file = output_dir + "/" + file_name + suffix
    else:
        new_file = input_file + suffix
            
    n = 60 #chunk size
    with open(new_file, 'w') as f:
        for (key,values) in data.items():
            for value in values:
                f.write(f">{key}\n")
                chunks = [value[i:i+n] for i in range(0, len(value), n)]
                for chunk in chunks:
                    f.write(f"{chunk}\n")


def dealign(input_file, input_dir, output_dir, suffix):
    fasta_pattern = r'(?<!etetoolkit)(\.fa|\.fasta)$'
    files = []
    if(input_dir is None):
        files = [input_file]
    else:
        entries = Path(input_dir)
        for entry in entries.iterdir():
            if re.search(fasta_pattern, entry.name) is not None:
                files.append(f"{input_dir}/{entry.name}")
        
    for file in files:
        dealign_helper(file, output_dir, suffix=("_" + suffix) if suffix is not None else "")

if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()
    input_file = args.file
    input_dir = args.input_dir
    output_dir = args.output_dir
    suffix = args.suffix
    dealign(input_file, input_dir, output_dir, suffix)