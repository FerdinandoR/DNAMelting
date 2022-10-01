#! /usr/bin/env python
'''
Writes a dataset of DNA duplex melting temperatures from the SantaLucia model.

Each line of the database contains in order:
1. the sequence in 3'-5' direction
2. The duplex concentration in micromolar
3. The salt concentration

By default, the database contains every sequence with a number of bases
comprised between 6 and 9. 
'''
import SantaLucia as sl
from tqdm import tqdm
import numpy as np
import pandas as pd
import os

bases_to_i = {'A':1, 'T':2, 'C':3, 'G':4}
bases = list(bases_to_i.keys())

def base_convert(i, b, n):
    '''
    Convert number i in decimal base to base b, then
    pad it with leading zeros until it contains n digits.
    '''
    result = []
    while i > 0:
            result.insert(0, i % b)
            i = i // b
    while len(result) < n:
        result.insert(0, 0)
    return result
def get_Tm_dataframe(n_bases, n_bases_buffer, duplex_umol_conc, salt_mol_conc):
    '''
    Computes the melting temperatures of all the sequences with a given number of bases,
    for the given duplex and salt concentrations.

    The melting temperatures are returned as a dataframe ready to be printed on file.
    '''

    n_seq = 4**n_bases
    data = np.array([['E'*n_bases, -1, -1, -1] + [-1] * n_bases_buffer] * n_seq * len(duplex_umol_conc) * len(salt_mol_conc))
    e_n = 0
    # loop over all the sequences
    for i in tqdm(range(n_seq)):
        # transform the number into a base-4 number
        base_4 = base_convert(i, 4, n_bases)
        # convert the base-4 number to a DNA string
        seq = ''.join([bases[i] for i in base_4])
        # loop over duplex and salt concentrations
        for c in duplex_umol_conc:
            for s in salt_mol_conc:
                # compute the melting temperature - c is rescaled to respect get_TM's convention
                T_m = sl.get_TM(seq, salt_conc=s, duplex_concentration=c * 1e-6)[0]
                # add the sequence and numerical columns to the entry
                entry = [seq, str(s), str(c), str(T_m)]
                # add the columns encoding each nucleotide of the sequence into a number
                entry += [nuc for nuc in seq]
                # add columns encoding nucleotides up until n_bases_buffer
                entry += [0] * (n_bases_buffer-n_bases)
                data[e_n,:] = entry
                e_n += 1
    df = pd.DataFrame(data, columns = ['seq', 's_mol', 'c_umol', 'T_m'] + ['base_'+str(i) for i in range(n_bases_buffer)])
    return df


def write_database(start_n_bases = 6, end_n_bases = 9, duplex_umol_conc = 1, salt_mol_conc = 0.5):
    '''
    Create a database of sequences, duplex concentrations, salt concentrations,
    and their relative melting temperatures.

    Uses the SantaLucia model to compute the temperatures of all the sequences
    with a number of base-pairs between start_n_bases and end_n_bases
    '''
    # transform the concentrations into list, if they are not already
    try:
        duplex_umol_conc[0]
    except:
        duplex_umol_conc = [duplex_umol_conc]
    try:
        salt_mol_conc[0]
    except:
        salt_mol_conc = [salt_mol_conc]
    # create the folder
    database_path = 'melting_database'
    os.makedirs(database_path, exist_ok=True)
    # iterate over all possible sequence lengths:
    for n in range(start_n_bases, end_n_bases + 1):
        # generate the dataframe with all the sequences of length n and save it to file
        df = get_Tm_dataframe(n, end_n_bases, duplex_umol_conc, salt_mol_conc)
        dataframe_path = os.path.join(database_path, str(n) + 'meres.csv')
        df.to_csv(dataframe_path, header=True)
if __name__ == '__main__':
    write_database(2,5,[1, 2], 0.5)

