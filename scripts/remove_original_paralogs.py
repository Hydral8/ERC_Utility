import os
import argparse
from pathlib import Path
import shutil
import re

def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Rename paralog split files"
    )
    parser.add_argument("-f", "--file", help="the input fasta file")
    parser.add_argument("-d", "--input_dir", help="input directory with fasta files to be renamed accordingly")
    return parser

pattern = r'(\.fa|\.fasta)$'
fasta_pattern = r'(?<!etetoolkit)(\.fa|\.fasta)$'

def remove_original(input_file, input_dir):
    file_paths = []
    if(input_dir is None):
        file_paths = [input_file]
    else:
        entries = Path(input_dir)
        for entry in entries.iterdir():
            if re.search(fasta_pattern, entry.name) is not None:
                file_paths.append(f"{input_dir}/{entry.name}")
            
    paralog_ids = set()
            
    for file_path in file_paths:
        # file_path_trimmed = re.sub(pattern, "", file_path)
        file_path_data = file_path.split("/")
        filename = file_path_data[-1]
        filename_data = list(map(lambda x: x.strip(), filename.split("_")))
        protein_id = ""
        gene_id = ""
        
        if len(filename_data) > 1:
            if "at" in filename_data[0]:
                protein_id = filename_data[0]
                gene_id = filename_data[1]
            else:
                protein_id = filename_data[1]
                gene_id = filename_data[0]
        else:
            protein_id = filename_data[0]
            
        if gene_id != "" and protein_id not in paralog_ids:
            paralog_ids.add(protein_id)
            
    for file_path in file_paths:
        file_path_trimmed = re.sub(pattern, "", file_path)
        file_path_data = file_path_trimmed.split("/")
        protein_id = file_path_data[-1]
        if protein_id in paralog_ids:
            os.remove(file_path)
        
        
                
        
if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()
    input_file = args.file
    input_dir = args.input_dir
    
    remove_original(input_file, input_dir)