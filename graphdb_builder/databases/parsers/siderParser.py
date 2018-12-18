import os.path
import gzip
import re
import ckg_utils
from graphdb_builder import mapping as mp, builder_utils

#############################################
#              SIDER database               # 
#############################################
def parser(databases_directory, drug_source, download=True):
    config = ckg_utils.get_configuration('../databases/config/siderConfig.yml')
    url = config['SIDER_url']
    header = config['header']
    outputfileName = config['outputfileName']
    
    drugmapping = mp.getSTRINGMapping(config['SIDER_mapping'], source = drug_source, download = False, db = "STITCH")
    phenotypemapping = mp.getMappingFromOntology(ontology="Phenotype", source = config['SIDER_source'])
    
    relationships = set()
    directory = os.path.join(databases_directory,"SIDER")
    builder_utils.checkDirectory(directory)
    fileName = os.path.join(directory, url.split('/')[-1])
    if download:
        builder_utils.downloadDB(url, directory)
    associations = gzip.open(fileName, 'r')
    for line in associations:
        data = line.decode('utf-8').rstrip("\r\n").split("\t")
        drug = re.sub(r'CID\d', 'CIDm', data[1])
        se = data[3]
        if se.lower() in phenotypemapping and drug in drugmapping:
            for d in drugmapping[drug]:
                p = phenotypemapping[se.lower()]
                relationships.add((d, p, "HAS_SIDE_EFFECT", "SIDER", se))
    associations.close()

    return (relationships, header, outputfileName, drugmapping, phenotypemapping)


def parserIndications(databases_directory, drugMapping, phenotypeMapping, download=True):
    config = ckg_utils.get_configuration('../databases/config/siderConfig.yml')
    url = config['SIDER_indications']
    header = config['indications_header']
    outputfileName = config['indications_outputfileName']

    relationships = set()
    directory = os.path.join(databases_directory,"SIDER")
    builder_utils.checkDirectory(directory)
    fileName = os.path.join(directory, url.split('/')[-1])
    if download:
        builder_utils.downloadDB(url, directory)
    associations = gzip.open(fileName, 'r')
    for line in associations:
        data = line.decode('utf-8').rstrip("\r\n").split("\t")
        drug = re.sub(r'CID\d', 'CIDm', data[0])
        se = data[1]
        evidence = data[2]
        if se.lower() in phenotypeMapping and drug in drugMapping:
            for d in drugMapping[drug]:
                p = phenotypeMapping[se.lower()]
                relationships.add((d, p, "IS_INDICATED_FOR", evidence, "SIDER", se))
    
    associations.close()
    
    return (relationships, header, outputfileName)