
#usr/bin/env python3
# -*- coding: UTF-8 -*-
# MODULO 5: script para parsear la base de datos prosite presentes            .
# archivosvos prosite.doc y prosite.dat utilizando el modulo Biopython

from Bio.ExPASy import Prosite, Prodoc
import re
import os
import shutil

def prosite_db():
# con este script podeis parsear el archivo .dat
    handle = open("prosite.dat","r")
    records = Prosite.parse(handle)
    with open("prosite_db", "a") as outfile:
        for record in records:
            outfile.write(record.name+"\t"+record.accession+
		    "\t"+record.description+"\t"+record.pattern+"\n")

    handle.close()
    outfile.close()

    return()

def dictionary():

	dictionary_pattern = dict()
	file = open("prosite_db", "r")

	for line in file:
		columns = line.split("\t")
		name = columns[0]
		accession = columns[1]
		description = columns[2]
		pattern = columns[3]
		pattern = pattern.replace("-", "" )
		pattern = pattern.replace("x", ".")
		pattern = pattern.replace("(", "{")
		pattern = pattern.replace(")", "}")
		pattern = pattern.strip()
		if pattern == "":
			pass
		else:
			dictionary_pattern[accession] = [pattern, name, description]

	file.close()

	return(dictionary_pattern)

def domain_search(dictionary_pattern, file, path):

	ini_file = os.path.join(path, file)
	with open(ini_file, "r") as f:
		path2 = "RESULTS/Prosite_results"
		pos = file.find("_filtrado")
		name = file[:pos]
		out_file = name+"_domains.txt"
		new_filename = os.path.join(path2, out_file)
		with open(new_filename, "w") as final_file:
			count = 0
			for linea in f:
				if linea.startswith(">"): 
					subject = linea
					count += 1
					final_file.write(str(count)+". PROTEIN: "+subject[1:])
					final_file.write("---------------------------------------"
					                 +"--"+"\n")
				elif linea.startswith("\n") == False:
					seq = linea.strip() # Las meto en una variable donde voy a
					                    # buscar patrones en el diccionario
					hits = 0
					for key in dictionary_pattern.keys():
						pattern = dictionary_pattern[key][0]
						rgx = re.compile(pattern)
						results = rgx.search(seq)
						if results == None:
							pass
						else:
							hits += 1
							result_pattern = results.group()
							final_file.write(str(hits)+"º Domain"+"\n"+
							"Domain name: "+dictionary_pattern[key][1]+
							"\n"+"Accession: "+key+"\n"+"Pattern: "+
							str(result_pattern)+"\n"+"Description: "+
							dictionary_pattern[key][2]+"\n\n")
				else:
					pass

	f.close()
	final_file.close()

	return()
