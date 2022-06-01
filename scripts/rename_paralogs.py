import os
import argparse
from pathlib import Path
import shutil
import re
import shutil


def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Rename paralog split files"
    )
    parser.add_argument("-f", "--file", help="the input fasta file")
    parser.add_argument("-d", "--input_dir", help="input directory with fasta files to be renamed accordingly")
    parser.add_argument("-w", "--output_dir", help="the output dir of the renamed fasta files")
    parser.add_argument("-s", "--suffix", help="the suffix to add on the newly generated files")
    return parser

pattern = r'(\.fa|\.fasta)$'
fasta_pattern = r'(?<!etetoolkit)(\.fa|\.fasta)$'

def rename(input_file, input_dir, output_dir, suffix):
    suffix=("_" + suffix) if suffix is not None else ""
    copy = True
    file_paths = []
    if(input_dir is None):
        file_paths = [input_file]
    else:
        entries = Path(input_dir)
        for entry in entries.iterdir():
            if re.search(fasta_pattern, entry.name) is not None:
                file_paths.append(f"{input_dir}/{entry.name}")
            
    for file_path in file_paths:
        file_path_trimmed = re.sub(pattern, "", file_path)
        file_path_data = list(map(lambda x: x.strip(), file_path_trimmed.split("/")))
        if output_dir is None:
            copy = False
            output_dir = "."
            if(len(file_path_data) > 1):
                output_dir = "/".join(file_path_data[0:-1])
        filename = file_path_data[-1]
        filename_data = list(map(lambda x: x.strip(), filename.split("_")))
        protein_id = ""
        gene_id = ""
        
        if len(filename_data) > 1:
            if re.search(r'\dat\d', filename_data[1]) is not None:
                protein_id = filename_data[1]
                gene_id = filename_data[0]
            else:
                protein_id = filename_data[0]
                gene_id = filename_data[1]
        else:
            protein_id = filename_data[0]
            
        new_file_path = output_dir + "/" + protein_id + (("_" + gene_id) if gene_id != "" else "") + suffix + ".fa"
        if copy:
            shutil.copyfile(file_path, new_file_path)
        else:
            os.rename(file_path, new_file_path)
                
        
if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()
    input_file = args.file
    input_dir = args.input_dir
    output_dir = args.output_dir
    suffix = args.suffix
    
    rename(input_file, input_dir, output_dir, suffix)