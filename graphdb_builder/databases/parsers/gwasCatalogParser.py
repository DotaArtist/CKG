import os.path
from collections import defaultdict
import ckg_utils
from graphdb_builder import builder_utils

#########################
#   GWAS Catalog EBI    #
#########################
def parser(databases_directory, download= True):
    config = ckg_utils.get_configuration('../databases/config/gwasCatalogConfig.yml')
    url = config['GWASCat_url']
    entities_header = config['entities_header']
    relationships_header = config['relationships_header']
    entities = set()
    relationships = defaultdict(set)
    directory = os.path.join(databases_directory,"GWAScatalog")
    builder_utils.checkDirectory(directory)
    fileName = os.path.join(directory, url.split('/')[-1])
    if download:
        builder_utils.downloadDB(url, directory)
    with open(fileName, 'r') as catalog:
        for line in catalog:
            data = line.rstrip("\r\n").split("\t")
            pubmedid = data[1]
            date = data[3]
            title = data[6]
            sample_size = data[8]
            replication_size = data[9]
            chromosome = data[11]
            position = data[12]
            genes_mapped = data[14].split(" - ")
            snp_id = data[20]
            freq = data[26]
            pval = data[27]
            odds_ratio = data[30]
            trait = data[34]
            study = data[36]
            
            entities.add((study, "GWAS_study", title, date, sample_size, replication_size, trait))
            if pubmedid != "":
                relationships["published_in_publication"].add((study, pubmedid, "PUBLISHED_IN", "GWAS Catalog"))
    
    return (entities, relationships, entities_header, relationships_header)