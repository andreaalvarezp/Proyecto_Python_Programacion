#usr/bin/env python3
# -*- coding: UTF-8 -*-
# MODULO 4: MUSCLE

import sys
import os
import subprocess
import shutil

def input_muscle(query, file):

    cwd = os.getcwd()
    origin_path = os.path.join(query, file)
    final_path = os.path.join(cwd, file)
    # Aseguro que se copia en el archivo correcto
    pos = file.find("_")
    name = file[:pos]
    shutil.copy(origin_path, final_path)
    with open(final_path, "r") as f:
        lines = f.read()
        for filename in os.listdir(cwd):
            if filename.endswith(name+"_filtrado.fasta"):
                with open(filename, "a") as outfile:
                    outfile.write(lines)

    os.remove(final_path)

    return()


def funcion_muscle(file):

    pos = file.find("_filtrado") #Cambio el nombre del archivo output
    name = file[:pos]
    out_file = name+"_muscle.fa"
    print("Alignment in progress...")

    try:
        alignment = subprocess.run(["muscle", "-in", file, "-out", out_file])

    except:
        print("Error: alignment error")

    output_tree = name+"_muscle_tree.nw"

    try:
        muscle_tree = subprocess.run(["muscle", "-maketree", "-in", out_file, 
                                      "-out", output_tree, "-cluster", "neighborjoining"])

    except:
        print("Error in -maketree statement")

    os.remove(file)
    
    return(alignment, muscle_tree)






