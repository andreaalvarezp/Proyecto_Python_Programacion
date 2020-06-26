#usr/bin/env python3
# -*- coding: UTF-8 -*-
# MODULO 3: BLASTP y filtro por identity y coverage

import sys
import os
import subprocess
import shutil

def funcion_blast(file):

    pos = file.find(".")
    name = file[:pos]

    # Blastp como subprocess
    blastp = subprocess.run(["blastp", "-query", file, "-db", "multifasta.fa", 
                             "-evalue", "0.00001", "-outfmt", 
                             "6 sseqid sseq qseqid qseq pident qcovs evalue", 
                             "-out", str(name)+"_result.fasta"])

    os.remove(file) # Elimino archivo original

    return()

def filtro_blastp(file, identity, coverage, path):

    pos = file.find("_blastp")
    name = file[:pos]
    new_filename = name+"_filtrado.fasta"

    with open(new_filename, "a") as outfile:
        with open(file, "r") as f:
            lineas = f.readlines()
            for linea in lineas:
                b = linea.split("\t") # Hago una lista con cada linea
                ident = b[4] # Cojo los valores de id y cov
                cov = b[5]
                if ident > identity and cov > coverage: # Filtro
                    # Reescribo en un nuevo archivo las lineas filtradas
                    outfile.write(">"+b[0]+"\n"+b[1]+"\n")

    f.close()
    outfile.close()
    os.remove(file) # Elimino blastp sin filtrar

    cwd = os.getcwd()
    ini_path = os.path.join(cwd, new_filename)
    shutil.copy(ini_path, path)

    return()




