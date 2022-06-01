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
    parser.add_argument("-f", "--file", help="the input fasta file")
    parser.add_argument("-d", "--input_dir", help="input directory with fasta files")
    parser.add_argument("-o", "--order_schema", help="the file schema giving the orders of the taxas. Used as reference for sorting fasta file")
    parser.add_argument("-w", "--output_dir", help="the output dir of the new fasta file (reordered)")
    parser.add_argument("-s", "--suffix", help="suffix to add to newly ordered files")
    return parser

def find_closest_organism(organism, ordering):
    for key in ordering:
        if key.find(organism) != -1:
            return key
    ordering[organism] = []
    return organism

pattern = r'\(\d\)$'
pattern_space = r'\b \b'

def order_file_helper(input_file, ordering, output_dir, suffix):
    
    # copy dict containing ordering/seqs for each taxa (with initial values so its not overwritten every single time we run this function). No side effects
    data = copy.deepcopy(ordering)
    
    organism = ""
    sequence = ""
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
                        sequence += line
                else:
                    data[organism].append(sequence)
                    organism = line[1:]
                    organism = re.sub(pattern, "", organism)
                    organism = re.sub(pattern_space, "_", organism)
                    organism = find_closest_organism(organism, data)
                    sequence = ""   
            except:
                data[organism].append(sequence)
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

def order_file(input_file, input_dir, order_schema, output_dir, suffix):
    ordered_taxa = ["ORNITHORHYNCHUS_ANATINUS","MONODELPHIS_DOMESTICA","PHASCOLARCTOS_CINEREUS","SARCOPHILUS_HARRISII","DASYPUS_NOVEMCINCTUS","LOXODONTA_AFRICANA","TRICHECHUS_MANATUS","ORYCTEROPUS_AFER","ELEPHANTULUS_EDWARDII","CHRYSOCHLORIS_ASIATICA","ECHINOPS_TELFAIRI","OCHOTONA_PRINCEPS","ORYCTOLAGUS_CUNICULUS","FUKOMYS_DAMARENSIS","HETEROCEPHALUS_GLABER","CAVIA_PORCELLUS","CHINCHILLA_LANIGERA","OCTODON_DEGUS","ICTIDOMYS_TRIDECEMLINEATUS","MARMOTA_MARMOTA","CASTOR_CANADENSIS","DIPODOMYS_ORDII","JACULUS_JACULUS","NANNOSPALAX_GALILI","PEROMYSCUS_MANICULATUS","MICROTUS_OCHROGASTER","CRICETULUS_GRISEUS","MESOCRICETUS_AURATUS","MERIONES_UNGUICULATUS","RATTUS_NORVEGICUS","MUS_PAHARI","MUS_CAROLI","MUS_MUSCULUS","GALEOPTERUS_VARIEGATUS","OTOLEMUR_GARNETTII","MICROCEBUS_MURINUS","PROPITHECUS_COQUERELI","CARLITO_SYRICHTA","AOTUS_NANCYMAAE","CALLITHRIX_JACCHUS","CEBUS_CAPUCINUS","SAIMIRI_BOLIVIENSIS","NOMASCUS_LEUCOGENYS","PONGO_ABELII","GORILLA_GORILLA","HOMO_SAPIENS","PAN_PANISCUS","PAN_TROGLODYTES","RHINOPITHECUS_BIETI","RHINOPITHECUS_ROXELLANA","COLOBUS_ANGOLENSIS","PILIOCOLOBUS_TEPHROSCELES","CHLOROCEBUS_SABAEUS","PAPIO_ANUBIS","CERCOCEBUS_ATYS","MANDRILLUS_LEUCOPHAEUS","MACACA_NEMESTRINA","MACACA_FASCICULARIS","MACACA_MULATTA","CONDYLURA_CRISTATA","ERINACEUS_EUROPAEUS","SOREX_ARANEUS","HIPPOSIDEROS_ARMIGER","RHINOLOPHUS_SINICUS","ROUSETTUS_AEGYPTIACUS","PTEROPUS_ALECTO","PTEROPUS_VAMPYRUS","MINIOPTERUS_NATALENSIS","EPTESICUS_FUSCUS","MYOTIS_BRANDTII","MYOTIS_LUCIFUGUS","MYOTIS_DAVIDII","CERATOTHERIUM_SIMUM","EQUUS_ASINUS","EQUUS_PRZEWALSKII","EQUUS_CABALLUS","MANIS_JAVANICA","PANTHERA_PARDUS","PANTHERA_TIGRIS","ACINONYX_JUBATUS","FELIS_CATUS","CANIS_LUPUS","URSUS_MARITIMUS","AILUROPODA_MELANOLEUCA","ENHYDRA_LUTRIS","MUSTELA_PUTORIUS","LEPTONYCHOTES_WEDDELLII","ODOBENUS_ROSMARUS","VICUGNA_PACOS","CAMELUS_DROMEDARIUS","CAMELUS_BACTRIANUS","CAMELUS_FERUS","SUS_SCROFA","BALAENOPTERA_ACUTOROSTRATA","PHYSETER_CATODON","LIPOTES_VEXILLIFER","DELPHINAPTERUS_LEUCAS","TURSIOPS_TRUNCATUS","ORCINUS_ORCA","ODOCOILEUS_VIRGINIANUS","PANTHOLOPS_HODGSONII","CAPRA_HIRCUS","OVIS_ARIES","BUBALUS_BUBALIS","BISON_BISON","BOS_GRUNNIENS","BOS_INDICUS","BOS_TAURUS"]
    fasta_pattern = r'(?<!etetoolkit)(\.fa|\.fasta)$'
    
    if(order_schema is not None):
        with open(order_schema, "r") as f: 
            ordered_taxa = f.read().splitlines()
            
    data = {key : [] for key in ordered_taxa}
    
    files = []
    if(input_dir is None):
        files = [input_file]
    else:
        entries = Path(input_dir)
        for entry in entries.iterdir():
            if re.search(fasta_pattern, entry.name) is not None:
                files.append(f"{input_dir}/{entry.name}")
            
    for file in files:
        order_file_helper(file, data, output_dir, suffix=("_" + suffix) if suffix is not None else "")
                
        
if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()
    input_file = args.file
    input_dir = args.input_dir
    order_schema = args.order_schema
    output_dir = args.output_dir
    suffix = args.suffix
    order_file(input_file, input_dir, order_schema, output_dir, suffix)