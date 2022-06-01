# from openpyxl import load_workbook, Workbook
import xlsxwriter
import argparse
from pathlib import Path
from count import count_file
import re
import pandas as pd
import numpy as np
import os

def init_argparse():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Pull ortholog names from ortholog protein set"
    )
    parser.add_argument("-d", "--input_dir", help="input directory with fasta files")
    parser.add_argument("-o", "--output_path", help="path for output taxa stats sheet")
    parser.add_argument("-f", "--id2name", help="path to id2name file")
    parser.add_argument("-mito", "--mito_path", help="path to file containing mito ids", default="../assets/mitoproteins.txt")
    parser.add_argument("-thirty", "--thirty_path", help="path to file containing 30MY ids", default="../assets/30myproteins.txt")
    return parser

fasta_pattern = r'(?<!etetoolkit)(\.fa|\.fasta)$'

def main(input_dir, output_path, id2name_path, mito_path, thirty_path):
    output_path_splits = output_path.split("/")
    dir = "/".join(output_path_splits[:-1])
    if not os.path.isdir(dir):
        os.mkdir(dir)
    name = output_path_splits[-1]
    mito_file = open(mito_path)
    thirty_file = open(thirty_path)
    
    #all taxa and mito proteins (probably move this into a separate file)
    mito_proteins = set(map(lambda v: v.strip("\n"), mito_file.readlines()))
    thirty_proteins = set(map(lambda v: v.strip("\n"), thirty_file.readlines()))
    full_taxa = ["ORNITHORHYNCHUS_ANATINUS","MONODELPHIS_DOMESTICA","PHASCOLARCTOS_CINEREUS","SARCOPHILUS_HARRISII","DASYPUS_NOVEMCINCTUS","LOXODONTA_AFRICANA","TRICHECHUS_MANATUS","ORYCTEROPUS_AFER","ELEPHANTULUS_EDWARDII","CHRYSOCHLORIS_ASIATICA","ECHINOPS_TELFAIRI","OCHOTONA_PRINCEPS","ORYCTOLAGUS_CUNICULUS","FUKOMYS_DAMARENSIS","HETEROCEPHALUS_GLABER","CAVIA_PORCELLUS","CHINCHILLA_LANIGERA","OCTODON_DEGUS","ICTIDOMYS_TRIDECEMLINEATUS","MARMOTA_MARMOTA","CASTOR_CANADENSIS","DIPODOMYS_ORDII","JACULUS_JACULUS","NANNOSPALAX_GALILI","PEROMYSCUS_MANICULATUS","MICROTUS_OCHROGASTER","CRICETULUS_GRISEUS","MESOCRICETUS_AURATUS","MERIONES_UNGUICULATUS","RATTUS_NORVEGICUS","MUS_PAHARI","MUS_CAROLI","MUS_MUSCULUS","GALEOPTERUS_VARIEGATUS","OTOLEMUR_GARNETTII","MICROCEBUS_MURINUS","PROPITHECUS_COQUERELI","CARLITO_SYRICHTA","AOTUS_NANCYMAAE","CALLITHRIX_JACCHUS","CEBUS_CAPUCINUS","SAIMIRI_BOLIVIENSIS","NOMASCUS_LEUCOGENYS","PONGO_ABELII","GORILLA_GORILLA","HOMO_SAPIENS","PAN_PANISCUS","PAN_TROGLODYTES","RHINOPITHECUS_BIETI","RHINOPITHECUS_ROXELLANA","COLOBUS_ANGOLENSIS","PILIOCOLOBUS_TEPHROSCELES","CHLOROCEBUS_SABAEUS","PAPIO_ANUBIS","CERCOCEBUS_ATYS","MANDRILLUS_LEUCOPHAEUS","MACACA_NEMESTRINA","MACACA_FASCICULARIS","MACACA_MULATTA","CONDYLURA_CRISTATA","ERINACEUS_EUROPAEUS","SOREX_ARANEUS","HIPPOSIDEROS_ARMIGER","RHINOLOPHUS_SINICUS","ROUSETTUS_AEGYPTIACUS","PTEROPUS_ALECTO","PTEROPUS_VAMPYRUS","MINIOPTERUS_NATALENSIS","EPTESICUS_FUSCUS","MYOTIS_BRANDTII","MYOTIS_LUCIFUGUS","MYOTIS_DAVIDII","CERATOTHERIUM_SIMUM","EQUUS_ASINUS","EQUUS_PRZEWALSKII","EQUUS_CABALLUS","MANIS_JAVANICA","PANTHERA_PARDUS","PANTHERA_TIGRIS","ACINONYX_JUBATUS","FELIS_CATUS","CANIS_LUPUS","URSUS_MARITIMUS","AILUROPODA_MELANOLEUCA","ENHYDRA_LUTRIS","MUSTELA_PUTORIUS","LEPTONYCHOTES_WEDDELLII","ODOBENUS_ROSMARUS","VICUGNA_PACOS","CAMELUS_DROMEDARIUS","CAMELUS_BACTRIANUS","CAMELUS_FERUS","SUS_SCROFA","BALAENOPTERA_ACUTOROSTRATA","PHYSETER_CATODON","LIPOTES_VEXILLIFER","DELPHINAPTERUS_LEUCAS","TURSIOPS_TRUNCATUS","ORCINUS_ORCA","ODOCOILEUS_VIRGINIANUS","PANTHOLOPS_HODGSONII","CAPRA_HIRCUS","OVIS_ARIES","BUBALUS_BUBALIS","BISON_BISON","BOS_GRUNNIENS","BOS_INDICUS","BOS_TAURUS"]
    thirty_taxa = ["ORNITHORHYNCHUS_ANATINUS","MONODELPHIS_DOMESTICA","PHASCOLARCTOS_CINEREUS","SARCOPHILUS_HARRISII","DASYPUS_NOVEMCINCTUS","LOXODONTA_AFRICANA","TRICHECHUS_MANATUS","ORYCTEROPUS_AFER","ELEPHANTULUS_EDWARDII","CHRYSOCHLORIS_ASIATICA","ECHINOPS_TELFAIRI","OCHOTONA_PRINCEPS","ORYCTOLAGUS_CUNICULUS","FUKOMYS_DAMARENSIS","HETEROCEPHALUS_GLABER","CAVIA_PORCELLUS","CHINCHILLA_LANIGERA","OCTODON_DEGUS","MARMOTA_MARMOTA","CASTOR_CANADENSIS","DIPODOMYS_ORDII","JACULUS_JACULUS","NANNOSPALAX_GALILI","PEROMYSCUS_MANICULATUS","MESOCRICETUS_AURATUS","MERIONES_UNGUICULATUS","MUS_MUSCULUS","GALEOPTERUS_VARIEGATUS","OTOLEMUR_GARNETTII","MICROCEBUS_MURINUS","PROPITHECUS_COQUERELI","CARLITO_SYRICHTA","CALLITHRIX_JACCHUS","HOMO_SAPIENS","MACACA_MULATTA","CONDYLURA_CRISTATA","ERINACEUS_EUROPAEUS","SOREX_ARANEUS","HIPPOSIDEROS_ARMIGER","RHINOLOPHUS_SINICUS","ROUSETTUS_AEGYPTIACUS","PTEROPUS_VAMPYRUS","MINIOPTERUS_NATALENSIS","EPTESICUS_FUSCUS","MYOTIS_DAVIDII","CERATOTHERIUM_SIMUM","EQUUS_CABALLUS","MANIS_JAVANICA","FELIS_CATUS","CANIS_LUPUS","AILUROPODA_MELANOLEUCA","MUSTELA_PUTORIUS","ODOBENUS_ROSMARUS","CAMELUS_FERUS","SUS_SCROFA","BALAENOPTERA_ACUTOROSTRATA","PHYSETER_CATODON", "ORCINUS_ORCA","ODOCOILEUS_VIRGINIANUS","BOS_GRUNNIENS"]
    thirty_taxa_set = set(thirty_taxa)
    non_thirty_taxa = list(set(full_taxa) - thirty_taxa_set)
    
    # set up excel sheet
    wb = xlsxwriter.Workbook(output_path)
    taxa_stats_sheet = wb.add_worksheet("taxa_stats")
    
    # excel headers
    basic_protein_info_headers = ["Annotation", "Protein_ID","is_mito","is_in_dataset"]
    protein_aggregated_stats_headers = ["total_unique_taxa_count", "total_sequence_count", "total_min_sequence_count","total_max_sequence_count","total_average_sequence_count", "total_median_sequence_count", "30my_unique_taxa_count", "30my_sequence_count", "30my_min_sequence_count", "30my_max_sequence_count", "30my_average_sequence_count", "30my_median_sequence_count", "deep_paralog_split", "num_0s", "num_1s", "num_2s", "num_3s", "num_4s", "num_5s", "potential_num_paralogs", "num_taxa_for_paralogs"]
    headers = [*basic_protein_info_headers, *protein_aggregated_stats_headers, *full_taxa]
    bold = wb.add_format({
        'bold': True
    })
    highlight = wb.add_format({'bg_color': '#32E3CB'})
    taxa_stats_sheet.write_row(0, 0, headers, cell_format=bold)
    row_idx = 1
    
    id2name = {}
    # load tsv 
    with open(id2name_path, "r") as f:
        for l in f:
            # print(l.split("\t"))
            key,value = l.split("\t")
            value.strip()
            id2name[key] = value
    
    # create data in full_taxa order
    data = {key: 0 for key in full_taxa}
    
    files = []
    entries = Path(input_dir)
    for entry in entries.iterdir():
        if re.search(fasta_pattern, entry.name) is not None:
            files.append(f"{input_dir}/{entry.name}")
            
    output_data = []
            
    for file in files:
        returned_data = count_file(file, data, dir, False, True)
        file_name = file.split("/")[-1]
        id = re.sub(fasta_pattern, "", file_name) #retrieve protein id
        gene = None
        if "_" in id:
            gene = id.split("_")[-1]
        try:
            id2name[id]
        except:
            print(id)
            continue
        basic_info = [id2name[id], id, "yes" if id in mito_proteins else "no", "30MY" if id in thirty_proteins else "no"]
        
        seq_counts = []
        thirty_seq_counts = []
        
        for taxa in full_taxa:
            cnt = 0
            if taxa in returned_data:
                cnt = returned_data[taxa]
                
            # append counts to thirty and full
            seq_counts.append(cnt)
            if taxa in thirty_taxa_set:
                thirty_seq_counts.append(cnt)
                
        seq_counts = np.array(seq_counts)
        thirty_seq_counts = np.array(thirty_seq_counts)
        
        unique, counts = np.unique(thirty_seq_counts, return_counts=True)
        
        potential_paralogs = -1
        num_taxa_for_paralogs = -1
        unique_counts = np.asarray((unique, counts)).T
        counts_above_50 = unique_counts[unique_counts[:, 1] >= 50]
        if len(counts_above_50) != 0:
            potential_paralogs = counts_above_50[0, 0]
            num_taxa_for_paralogs = counts_above_50[0, 1]
            
        protein_agg_stats = [np.count_nonzero(seq_counts), np.sum(seq_counts), np.min(seq_counts), np.max(seq_counts), np.average(seq_counts), np.median(seq_counts), np.count_nonzero(thirty_seq_counts), np.sum(thirty_seq_counts), np.min(thirty_seq_counts), np.max(thirty_seq_counts), np.average(thirty_seq_counts), np.median(thirty_seq_counts), gene if gene else "no", np.count_nonzero(thirty_seq_counts == 0), np.count_nonzero(thirty_seq_counts == 1), np.count_nonzero(thirty_seq_counts == 2), np.count_nonzero(thirty_seq_counts == 3), np.count_nonzero(thirty_seq_counts == 4), np.count_nonzero(thirty_seq_counts == 5), potential_paralogs, num_taxa_for_paralogs] # "total_unique taxa_count", "total_sequence count", "total_min sequence_count", "total_max sequence_count", "total_average sequence_count", "total_median sequence_count", "30my_unique taxa_count", "30my_sequence count", "30my_min sequence_count", "30my_maxsequence_count", "30my_average sequence_count", "30my_median sequence_count", "deep_paralog_split", "num_0s", "num_1s", "num_2s", "num_3s", "num_4s", "num_5s", "potential_num_paralogs", "num_taxa_for_paralogs"
        full_taxa_stats = seq_counts
        
        full_data = [*basic_info, *protein_agg_stats, *full_taxa_stats]
        output_data.append(full_data)
    
    df = pd.DataFrame(output_data, columns=headers)
    df_sorted = df.sort_values(["30my_sequence_count"], ascending=False)
    for row in df_sorted.itertuples(index=False, name='Pandas'):
        if (row.potential_num_paralogs > 1):
            taxa_stats_sheet.set_row(row_idx, cell_format=highlight)
        taxa_stats_sheet.write_row(row_idx, 0, list(row))
        row_idx += 1
        
    wb.close()
    

        
        
                
        
        
                
        
if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()
    input_dir = args.input_dir
    output_path = args.output_path
    id2name = args.id2name
    mito_path = args.mito_path
    thirty_path = args.thirty_path
        
    main(input_dir, output_path, id2name, mito_path, thirty_path)