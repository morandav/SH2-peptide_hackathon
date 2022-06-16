from Bio.PDB.PDBExceptions import PDBConstructionWarning
from Bio.PDB.PDBParser import PDBParser
import warnings
import os

PEPTIDE_LENGTH = 20


def get_chain_length(pdb_file, wanted_chain):
    """
    Checks the length of a specific chain in the given pdb file
    :param pdb_file:
    :param wanted_chain:
    :return: chain's length
    """
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', PDBConstructionWarning)
        struct = parser.get_structure("pdb", pdb_file)
    chain_length = 0
    for ch in struct.get_chains():
        if ch.get_id() == wanted_chain:
            for r in ch.get_residues():
                if r.id[0] == ' ':
                    chain_length += 1
    print("file: ", pdb_file,", length: ", chain_length)
    return chain_length


def get_maximal_sh2_pep_length(good_pdbs_path):
    """
    gets an absolute path of the good_pdbs directory and checks what is the maximal SH2 and peptide lengths
    :param good_pdbs_path: absolute path of the good_pdbs directory
    :return: [SH2_maximal_length, peptide_maximal_length]
    """
    sh2_max_len = 0
    peptide_max_len = 0
    for pdb_file in os.listdir(good_pdbs_path):
        os.chdir(os.path.join(good_pdbs_path, pdb_file))
        print("### ", pdb_file)
        for file in os.listdir('.'):
            if file.find('SH2') == 0:   # SH2 path : SH2_<chain_id>_.pdb
                wanted_chain = (file.split('_'))[1].split('.')[0]
                chain_len = get_chain_length(file, wanted_chain)
                if chain_len > sh2_max_len:
                    sh2_max_len = chain_len
            elif file.find('peptide') == 0: # peptide path : peptide_<chain_id>.pdb
                wanted_chain = (file.split('_'))[1].split('.')[0]
                chain_len = get_chain_length(file, wanted_chain)
                if chain_len > peptide_max_len:
                    peptide_max_len = chain_len
    return sh2_max_len,peptide_max_len


if __name__ == "__main__":
    parser = PDBParser()
    good_pdbs_path = "/cs/usr/moran_david/Downloads/good_pdbs/" # absolute path
    sh2_max_len, peptide_max_len = get_maximal_sh2_pep_length(good_pdbs_path)
    print("maximal SH2 length: ", sh2_max_len)
    print("maximal peptide length:", peptide_max_len)