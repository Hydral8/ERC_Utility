from ast import arg
import os
import argparse
from pathlib import Path
import shutil

def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Pull ortholog names from ortholog protein set"
    )
    parser.add_argument("-f", "--file", help="the input ortholog id file")
    parser.add_argument(
        "-d", "--directory"
    )
    parser.add_argument(
        "-o", "--output_dir"
    )
    parser.add_argument("-m", "--method", default="copy")
    return parser

def main():
    parser = init_argparse()
    args = parser.parse_args()
    input_file = args.file
    cur_dir = args.directory
    output_dir = args.output_dir
    method = args.method
    
    with open(input_file, "r") as f: 
        orthoIDS = f.read().splitlines()
    

    for id in orthoIDS:
        if(os.path.exists(f"{cur_dir}/{id}.fa")):
            if(method == "move"):
                shutil.move(f"{cur_dir}/{id}.fa", f"{output_dir}/{id}.fa")
            else:
                shutil.copy(f"{cur_dir}/{id}.fa", f"{output_dir}/{id}.fa")
        else:
            print(f"{id} was not found in directory")  
    
    movement = "moved" if method == "move" else "copied"
    print("{movement} all possible files!")
        
main()