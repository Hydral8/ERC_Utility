import os
import argparse
from pathlib import Path
import shutil
import copy
import re

fasta_pattern = r'(?<!etetoolkit)(\.fa|\.fasta)$'


def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Pull ortholog names from ortholog protein set"
    )
    parser.add_argument("-f", "--file", help="the input fasta file")
    parser.add_argument("-d", "--input_dir", help="input directory with fasta files")
    parser.add_argument("-o", "--output_dir", help="the output dir of the count file")
    parser.add_argument("-nw", "--no_write", action="store_true", help="to not write outputs")
    parser.add_argument("-s", "--store", action="store_true", help="to store outputs")
    return parser

def find_closest_organism(organism, ordering):
    for key in ordering:
        if key.find(organism) != -1: #check if key exists
            return key #if key exists return it
    ordering[organism] = 0 #if it does not, add key to data
    return organism

digit_pattern = r'\(\d\)$'
space_pattern = r'\b \b'

def count_file(input_file, count_dict, output_dir, write=True, store=False):
    
    # copy dict containing ordering/seqs for each taxa (with initial values so its not overwritten every single time we run this function). No side effects
    data = copy.deepcopy(count_dict)
    organism = ""
    with open(input_file, 'r') as f:
        iterator = iter(f)
        
        while(True):
            try:
                line = next(iterator).strip()
                if line[0] == ">":
                    organism = line[1:]
                    organism = re.sub(digit_pattern, "", organism)
                    organism = re.sub(space_pattern, "_", organism)
                    organism = find_closest_organism(organism, data)
                    data[organism] += 1
                    
                    # if data[organism] > 1:
                    #     print(input_file + ": " + "\n")
                    #     print(organism + " " + str(data[organism]))
                    #     print("-----------------------" + "\n")
            except:
                break

    file_name = input_file.split("/")[-1]
    if output_dir is not None:
        new_file = output_dir + "/" + file_name + "_counts"
    else:
        new_file = input_file + "_counts"
            
    if (write):
        with open(new_file, 'w') as f:
            for (key,count) in data.items():
                f.write(f"{key}: {count}\n")
                
    if (store):
        return data

def main(input_file, input_dir, output_dir, no_write, store):
    if output_dir: #make output dir if it does not already exist
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
    
    global_data = {}
    data = {}
    
    files = []
    if(input_dir is None):
        files = [input_file]
    else:
        entries = Path(input_dir)
        for entry in entries.iterdir():
            files.append(f"{input_dir}/{entry.name}")
            
    for file in files:
        returned_data = count_file(file, data, output_dir, write = False if no_write else True, store=store)
        if (store):
            file_name = file.split("/")[-1]
            id = re.sub(fasta_pattern, file_name) #retrieve protein id
            global_data[id] = returned_data
                
        
if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()
    input_file = args.file
    input_dir = args.input_dir
    output_dir = args.output_dir
    no_write = args.no_write
    store = args.store
    
    main(input_file, input_dir, output_dir, no_write, store)