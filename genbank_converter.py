#usr/bin/env python3
# -*- coding: UTF-8 -*-
# MODULO 1: CONVERTIR LA BASE DE DATOS .GBFF A UN ARCHIVO FASTA PARA EL BLASTP

import sys
from Bio import GenBank
from Bio import SeqIO
import os
import shutil

def convertidor_fasta(genbank):

    if os.path.isdir(genbank): # Compruebo que el directorio existe
        for file in os.listdir(genbank):
            dir = os.path.join(genbank, file)
            if os.path.isfile(dir) == True:
                input_file = open(dir, "r")

                for seq_record in SeqIO.parse(input_file, "genbank"):
                    output_file = open("multifasta.fa", "a")

                    for seq_feature in seq_record.features:
                        try:
                            if seq_feature.type == "CDS":
                                output_file.write("> %s@%s\n%s\n" % (
                                    seq_feature.qualifiers["locus_tag"][0],
                                    seq_record.name,
                                    seq_feature.qualifiers["translation"][0])
                                )

                        except:
                            pass

        output_file.close()
        input_file.close()
    print("Done!")

    return()
