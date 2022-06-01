import os
import argparse
from pathlib import Path
import shutil
import copy
import re

def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Pull ortholog names from ortholog protein set"
    )
    parser.add_argument("-f", "--files", nargs="+", help="input files of fasta files")
    parser.add_argument("-d", "--input_dir", help="input directory with fasta files")
    parser.add_argument("-o", "--output_file", help="the output, concatenated file")
    return parser

def find_closest_organism(organism, data):
    for key in data:
        if key.find(organism) != -1:
            return key
    data[organism] = ""
    return organism

pattern = r'\(\d\)$'
pattern_space = r'\b \b'

def concat_files_helper(input_file, data):
    # note this will only work in cases where there is only ever 1 ortholog per specie. If there is more than one, it will concatenate everything into one.
    organism = ""
    with open(input_file, 'rb') as f:
        iterator = iter(f)
        line = next(iterator).decode(errors='replace').strip()
        if(line[0] == ">"):
            organism = line[1:]
            organism = re.sub(pattern, "", organism)
            organism = re.sub(pattern_space, "_", organism)
            organism = find_closest_organism(organism, data)
        
        while(True):
            try:
                line = next(iterator).decode(errors='replace').strip()
                if line[0] != ">":
                    data[organism] += line
                else:
                    organism = line[1:]
                    organism = re.sub(pattern, "", organism)
                    organism = re.sub(pattern_space, "_", organism)
                    organism = find_closest_organism(organism, data)  
            except:
                break

def concat(input_files, input_dir, output_file):
    fasta_pattern = r'(?<!etetoolkit)(\.fa|\.fasta)$'
            
    data = {}
    
    files = []
    if(input_dir is None):
        files = input_files
    else:
        entries = Path(input_dir)
        for entry in entries.iterdir():
            if re.search(fasta_pattern, entry.name) is not None:
                files.append(f"{input_dir}/{entry.name}")
            
    for file in files:
        concat_files_helper(file, data)
    
    n = 60 #chunk size
    with open(output_file, 'w') as f:
        for (key,value) in data.items():
            f.write(f">{key}\n")
            chunks = [value[i:i+n] for i in range(0, len(value), n)]
            for chunk in chunks:
                f.write(f"{chunk}\n")
                
        
if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()
    input_files = args.files
    input_dir = args.input_dir
    output_file = args.output_file
    concat(input_files, input_dir, output_file)