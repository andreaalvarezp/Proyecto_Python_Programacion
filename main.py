#usr/bin/env python3
# -*- coding: UTF-8 -*-
#----------------------------------------------------------------------------79
import genbank_converter
import sys
import re
import shutil
import os
import re
from pathlib import Path

def ayuda():
	print("\n"+"SCRIPT HELP PANNEL")
	print("USAGE: python proyecto.py GENBANK QUERY IDENTITY COVERAGE")
	print()
	print("INTRUCTIONS")
	print("- First argument: name of a folder with all the GenBanks you want to "
         +"use for the analysis inside")
	print("- Second argument: name of a folder with a multifasta file with all "
         +"the query sequences you want to use in the analysis")
	print("- Identity and coverage values must be numeric and must be provided "
         +"as arguments when running the script")
	print("IMPORTANT: GenBanks and Query folder must be in the same directory "
         +"as all the modules neede to run the script")
	print("")

longitud = len(sys.argv)

 # Compruebo que se han introducido un minimo numero de argumentos

if longitud < 5:
	print("")
	print("ERROR: Incorrect number of arguments")
	ayuda()
	exit ()

genbank = sys.argv[1]
query = sys.argv[2]
identity = sys.argv[3]
coverage = sys.argv[4]

# Compruebo que el identity y coverage son valores numericos

if (identity.isdigit() == False):
        print("")
        print("ERROR: Identity value must be numeric")
        ayuda()
        exit()
elif (coverage.isdigit() == False):
        print("")
        print("ERROR: Coverage value must be numeric")
        ayuda()
        exit()

# Seleccion de la carpeta donde estan los GenBanks
print("Analyzing GenBanks...")

# En el caso de que ya exista un mismo archivo multifasta, se borra
if os.path.isfile("multifasta.fa"): 
    print("Multifasta.fa alredy exists. It would be rewrited")
    os.remove("multifasta.fa")

if os.path.isdir(genbank): # Compruebo que el directorio seleccionado existe
        # MODULO 1
        resultado = genbank_converter.convertidor_fasta(genbank) 
else:
        print("ERROR: Selected directory do not exist")
        ayuda()
        exit()

# Seleccion de la carpeta donde esta almacenado el multifasta de los query
# Separo el multifasta en archivos fasta independientes

import query_analizer

if os.path.isdir(query):
    for file in os.listdir(query):
        # MODULO 2
        fasta = query_analizer.multifasta_fasta(query, file) 

cwd = os.getcwd()

print("\n"+"Checking query's format...")

if os.path.isdir(query):
    for filename in os.listdir(query):
        if filename.startswith("Query"):
            # MODULO 2
            comprobacion = query_analizer.comprobar_query(query, filename)

print("Done!"+"\n")

# Creo la BD a partir del multifasta: 

print("Creating database...")
os.system("makeblastdb -in multifasta.fa -dbtype prot")
print("Done!")

import blastp

for file in os.listdir(cwd):
    if file.endswith("_blastp.fasta"):
        # MODULO 3
       resultado_blastp = blastp.funcion_blast(file) 

# Creo la carpeta RESULTS donde se iran almacenando todos los resultados

print("\n"+"Creating RESULTS folder")
path = Path("RESULTS/Blastp_results")
if not os.path.isdir("RESULTS"):
    path.mkdir(parents = True)
else:
    shutil.rmtree("RESULTS")
    path.mkdir(parents = True)

# Filtro por identity y converage y guardo los resultados del fitrado en la     
# carpeta RESULTS

print("\n"+"Running Blastp...")
for file in os.listdir(cwd):
    if file.endswith("_blastp_result.fasta"):
        # MODULO 3
        blastp_filtro = blastp.filtro_blastp(file, identity, coverage, path)

print("\n"+"Blastp and sorting proceeded succesfully, you can check the files in "
     +"the RESULTS/Blastp_results folder")

# Añado el query original a los archivos que entraran como input en el MUSCLE

import muscle

# Añado a los archivos input del MUSCLE la secuencia query original
print("\n"+"Preparing MUSCLE input files...")
if os.path.isdir(query): # Itero sobre la carpeta de los querys
    for file in os.listdir(query):
        if file.startswith("Query_"):
            # MODULO 4
            input_muscle = muscle.input_muscle(query, file)

print("\n"+"Input files for MUSCLE are ready!")

# Se realiza alineamiento múltiple con MUSCLE de cada uno de los .fasta 
# que corresponde con los querys

for file in os.listdir(cwd):
    if file.endswith("_filtrado.fasta"):
        # MODULO 4
        multiple_alignment = muscle.funcion_muscle(file)

print("\n"+"Alignment proceeded successfully")
print("\n"+"You can check alignments and trees in RESULTS/Muscle_results folder")

path2 = Path("RESULTS/Muscle_results")
path2.mkdir(parents = True)

for file in os.listdir(cwd):
    if file.endswith("_muscle.fa") or file.endswith("_muscle_tree.nw"):
        ini_path = os.path.join(cwd, file)
        shutil.move(ini_path, path2)

# MODULO 5: Busqueda de dominios en Prosite
import prosite

print("\n"+"Creating Prosite Database and pattern dictionary...")

if os.path.isfile("prosite.dat") == False:
    print("ERROR: El archivo 'prosite.dat' no existe o no se encuentra "
         +"en el directorio correcto. Reviselo y vuelva a intentarlo")
    ayuda()
    exit()

if os.path.isfile("prosite_db") == False:
    domain_search = prosite.prosite_db()
    dictionary_pattern = prosite.dictionary()
else:
    os.remove("prosite_db")
    domain_search = prosite.prosite_db()
    dictionary_pattern = prosite.dictionary()

path3 = Path("RESULTS/Prosite_results")
path3.mkdir(parents = True)

shutil.move("prosite_db", path3)
print("\n"+"Done! You can check the db in file 'prosite_db' in RESULTS/ "          
    +"Prosite_results folder")

print("\n"+"Searching patterns in input sequences...")

for filename in os.listdir(path3): # Si los archivos existen, los elimino
    if filename.endswith("_domains"):
        os.remove(filename)
    else:
        pass

path = "RESULTS/Blastp_results"
for file in os.listdir(path):
    domain_search = prosite.domain_search(dictionary_pattern, file, path)
    
print("\n"+"Done! You can check the results in RESULTS/Prosite_results folder"+"\n")

