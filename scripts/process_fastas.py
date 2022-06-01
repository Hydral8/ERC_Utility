# process fastas for adding into master fasta folder

import os
import argparse
from pathlib import Path
import shutil
import re
from rename_paralogs import rename
from order_fasta import order_file
from dealign import dealign
from remove_original_paralogs import remove_original

def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Rename paralog split files"
    )
    parser.add_argument("-f", "--file", help="the input fasta file")
    parser.add_argument("-d", "--input_dir", help="input directory with fasta files")
    parser.add_argument("-o", "--order_schema", help="the file schema giving the orders of the taxas. Used as reference for sorting fasta file")
    parser.add_argument("-w", "--output_dir", help="the output dir of the new processed fastas")
    parser.add_argument("-s", "--suffix", help="suffix to add to newly processed files")
    return parser
                
        
if __name__ == "__main__":
    ordered_taxa = ["ORNITHORHYNCHUS_ANATINUS","MONODELPHIS_DOMESTICA","PHASCOLARCTOS_CINEREUS","SARCOPHILUS_HARRISII","DASYPUS_NOVEMCINCTUS","LOXODONTA_AFRICANA","TRICHECHUS_MANATUS","ORYCTEROPUS_AFER","ELEPHANTULUS_EDWARDII","CHRYSOCHLORIS_ASIATICA","ECHINOPS_TELFAIRI","OCHOTONA_PRINCEPS","ORYCTOLAGUS_CUNICULUS","FUKOMYS_DAMARENSIS","HETEROCEPHALUS_GLABER","CAVIA_PORCELLUS","CHINCHILLA_LANIGERA","OCTODON_DEGUS","ICTIDOMYS_TRIDECEMLINEATUS","MARMOTA_MARMOTA","CASTOR_CANADENSIS","DIPODOMYS_ORDII","JACULUS_JACULUS","NANNOSPALAX_GALILI","PEROMYSCUS_MANICULATUS","MICROTUS_OCHROGASTER","CRICETULUS_GRISEUS","MESOCRICETUS_AURATUS","MERIONES_UNGUICULATUS","RATTUS_NORVEGICUS","MUS_PAHARI","MUS_CAROLI","MUS_MUSCULUS","GALEOPTERUS_VARIEGATUS","OTOLEMUR_GARNETTII","MICROCEBUS_MURINUS","PROPITHECUS_COQUERELI","CARLITO_SYRICHTA","AOTUS_NANCYMAAE","CALLITHRIX_JACCHUS","CEBUS_CAPUCINUS","SAIMIRI_BOLIVIENSIS","NOMASCUS_LEUCOGENYS","PONGO_ABELII","GORILLA_GORILLA","HOMO_SAPIENS","PAN_PANISCUS","PAN_TROGLODYTES","RHINOPITHECUS_BIETI","RHINOPITHECUS_ROXELLANA","COLOBUS_ANGOLENSIS","PILIOCOLOBUS_TEPHROSCELES","CHLOROCEBUS_SABAEUS","PAPIO_ANUBIS","CERCOCEBUS_ATYS","MANDRILLUS_LEUCOPHAEUS","MACACA_NEMESTRINA","MACACA_FASCICULARIS","MACACA_MULATTA","CONDYLURA_CRISTATA","ERINACEUS_EUROPAEUS","SOREX_ARANEUS","HIPPOSIDEROS_ARMIGER","RHINOLOPHUS_SINICUS","ROUSETTUS_AEGYPTIACUS","PTEROPUS_ALECTO","PTEROPUS_VAMPYRUS","MINIOPTERUS_NATALENSIS","EPTESICUS_FUSCUS","MYOTIS_BRANDTII","MYOTIS_LUCIFUGUS","MYOTIS_DAVIDII","CERATOTHERIUM_SIMUM","EQUUS_ASINUS","EQUUS_PRZEWALSKII","EQUUS_CABALLUS","MANIS_JAVANICA","PANTHERA_PARDUS","PANTHERA_TIGRIS","ACINONYX_JUBATUS","FELIS_CATUS","CANIS_LUPUS","URSUS_MARITIMUS","AILUROPODA_MELANOLEUCA","ENHYDRA_LUTRIS","MUSTELA_PUTORIUS","LEPTONYCHOTES_WEDDELLII","ODOBENUS_ROSMARUS","VICUGNA_PACOS","CAMELUS_DROMEDARIUS","CAMELUS_BACTRIANUS","CAMELUS_FERUS","SUS_SCROFA","BALAENOPTERA_ACUTOROSTRATA","PHYSETER_CATODON","LIPOTES_VEXILLIFER","DELPHINAPTERUS_LEUCAS","TURSIOPS_TRUNCATUS","ORCINUS_ORCA","ODOCOILEUS_VIRGINIANUS","PANTHOLOPS_HODGSONII","CAPRA_HIRCUS","OVIS_ARIES","BUBALUS_BUBALIS","BISON_BISON","BOS_GRUNNIENS","BOS_INDICUS","BOS_TAURUS"]
    parser = init_argparse()
    args = parser.parse_args()
    input_file = args.file
    input_dir = args.input_dir
    order_schema = args.order_schema
    output_dir = args.output_dir
    suffix = args.suffix
    
    if output_dir:
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        
    
    rename(input_file, input_dir, output_dir, suffix)
    if output_dir:
        input_dir = output_dir
    dealign(input_file, input_dir, output_dir, suffix)
    order_file(input_file, input_dir, order_schema, output_dir, suffix)
    remove_original(input_file, input_dir)
    