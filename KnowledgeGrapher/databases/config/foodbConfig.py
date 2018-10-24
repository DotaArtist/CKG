    ###### FOODB Database ########
database_url = "http://www.foodb.ca/system/foodb_2017_06_29_csv.tar.gz"
files = ["contents.csv", "foods.csv", "compounds.csv"]
entities_header = ['ID', 'name', 'scientific_name', 'description', 'group', 'subgroup', 'source']
relationships_headers = {"food":['START_ID', 'END_ID', 'TYPE', 'min', 'max','average', 'units', 'source']}
