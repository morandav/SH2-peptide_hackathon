from Bio.PDB import MMCIFIO
from Bio.PDB.PDBExceptions import PDBConstructionWarning
from Bio.PDB.PDBList import PDBList
from Bio.PDB.PDBParser import PDBParser
from Bio.PDB.Superimposer import Superimposer
import warnings
import subprocess as sp
import os
import sys
import shutil

# os.chdir("/cs/usr/rotemmintz/Desktop/all_pdbs")
# for i in os.listdir("Xray"):
#     sp.run(f"rm -rf NMR/{i}", shell=True)
#
# exit()


# ********* NEED TO CHANGE ACCORDING TO LOCATION !!!! ********* #
# path to the SH2 pdb reference
SH2_REF_PATH = "/cs/usr/rotemmintz/Desktop/all_pdbs/pdb6pxc.A.pdb"
# path to the peptide pdb reference
PEPTIDE_REF = "/cs/usr/rotemmintz/Desktop/all_pdbs/pdb6pxc.U.pdb"
# path to the proteinHack program
PROTEINHACK_PATH = "/cs/usr/rotemmintz/Desktop/proteinHack"

# ********* DO NOT CHANGE !!!! ********* #
ACTUAL_DATA_DIR_NAME = "actual_data"
WHOLE_ALIGN_FILE_NAME = "whole_align"
GET_FRAG_CHAIN = "/cs/staff/dina/utils/get_frag_chain.Linux"
TRANS = "/cs/staff/dina/utils/pdb_trans"
ALIGN_SCRIPT = "../alignMPtrans.pl"
NAME_CHAIN = "~dina/scripts/namechain.pl"
SH2_CHAIN = "A"
P_CHAIN = "B"
PEPTIDE_LENGTH = 20
MATCH_INDEX = 0
CHAIN_INDEX = -5
ALIGNMENT_THRESHOLD = 70
EPSILON = 3
WEIRD = [0]


# ********* FUNCTIONS ********* #

def get_data():
    """
    returns a list [match_num, transition, RMSD] taken from "2_sol.res" in the current dir
    """
    if not os.path.exists("2_sol.res"):
        return [-1, "", 10000]
    output_file = open("2_sol.res")
    content = output_file.readlines()
    transition = " ".join(content[11].split()[2:])
    RMSD = float((content[12].split()[-1]))
    match_num = int(content[14].split()[-1])
    return [match_num, transition, RMSD]


def check_alignment_in_dir(dir_path, match_num_threshold, ref_path):
    """
    gets a dir path, returns a dictionary with key filename.pdb, and value- [match_num, transition, RMSD]
    In the dir- a file for every chain in a larger pdb file
    """
    data_dict = dict()
    os.chdir(dir_path)
    for f in os.listdir():
        if f[:-4] == os.path.basename(dir_path):
            continue
        if f.endswith(".pdb"):
            sp.run([ALIGN_SCRIPT, ref_path, f, "out"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
            data_list = get_data()  # get relevant data from 2_sol.res
            if data_list[0] > match_num_threshold:
                data_dict[f] = data_list

    os.chdir("..")
    return data_dict


def filter_pdbs(path_to_all_pdbs, threshold_for_align, ref_path):
    """
    filters only pdbs that are good for network's train and test
    :param path_to_all_pdbs: path to directory with pdb_dir files
    :param threshold_for_align: threshold of amount of atoms that were part of the alignment to decide if 2 chains are fit
    return: a dictionary of {pdb_file_name: (SH2 SH2_chain name, peptide SH2_chain name) of the pdbs that are good for the net
    """
    os.chdir(path_to_all_pdbs)
    os.mkdir(ACTUAL_DATA_DIR_NAME)
    for type_dir in os.listdir(path_to_all_pdbs): # NMR and Xray directory
        cur_pdb_dir = os.path.join(path_to_all_pdbs, type_dir)
        if os.path.isfile(cur_pdb_dir):
            continue
        if type_dir == ACTUAL_DATA_DIR_NAME:
            continue
        for pdb_dir in os.listdir(cur_pdb_dir):
            pdb_dir = os.path.join(cur_pdb_dir, pdb_dir)
            # checking if it is a file
            if os.path.isfile(pdb_dir):
                continue

            # check if we have a SH2_chain that is similar to our reference SH2_chain
            all_relevant_chains_dict = check_alignment_in_dir(pdb_dir, threshold_for_align, ref_path)
            find_best_sh2(path_to_all_pdbs, all_relevant_chains_dict, pdb_dir, ref_path)


def find_best_sh2(path_to_all_pdbs, all_relevant_chains_dict, pdb_dir, ref_path):
    """
    this function finds the best SH2 to align to and saves its pdb and its peptide pdb
    """
    max_val = 0
    max_file = None
    trans = ""
    for file, val in all_relevant_chains_dict.items():
        if val[MATCH_INDEX] > max_val:
            max_val = val[MATCH_INDEX]
            max_file = file
            trans = val[1]

    if max_file == None:
        return

    path_to_copy_to = f"{path_to_all_pdbs}/{ACTUAL_DATA_DIR_NAME}/{os.path.basename(pdb_dir)}"

    # the path of the whole pdb
    whole_file = f"{pdb_dir}/{os.path.basename(pdb_dir)}.pdb"
    # the path of the whole pdb to transpose
    new_path = f"{pdb_dir}/{WHOLE_ALIGN_FILE_NAME}.pdb"
    sp.run(f"{TRANS} {trans} < {whole_file} > {new_path}", shell=True, stdout=sp.DEVNULL,
           stderr=sp.DEVNULL)

    chain_peptide, start_peptide, end_peptide = sp.run(f"{PROTEINHACK_PATH } {EPSILON} {PEPTIDE_REF} {new_path}",
                                                       shell=True,
                                                       capture_output=True).stdout.strip().decode("utf-8").split()
    chain_sh2, start_sh2, end_sh2 = sp.run(f"{PROTEINHACK_PATH} {EPSILON} {ref_path} {new_path}",
                                           shell=True,
                                           capture_output=True).stdout.strip().decode("utf-8").split()

    if chain_peptide == '@' or chain_sh2 == '@':
        return

    if chain_peptide == chain_sh2:
        return

    if int(end_peptide) - int(start_peptide) <= 4 or int(end_peptide) - int(start_peptide) > 25:
        return

    if int(end_sh2) - int(start_sh2) > 140:
        WEIRD[0] += 1
        return

    if int(start_peptide) < 0:
        start_peptide = "0"

    os.mkdir(path_to_copy_to)
    to_copy_path_sh = f"{path_to_copy_to}/{os.path.basename(pdb_dir)}_SH2_{SH2_CHAIN}.pdb"
    to_copy_path_P =  f"{path_to_copy_to}/{os.path.basename(pdb_dir)}_peptide_{P_CHAIN}.pdb"

    sp.run(f"{GET_FRAG_CHAIN} {new_path} {chain_sh2} {start_sh2} {end_sh2} > {to_copy_path_sh}", shell=True)
    sp.run(f"{GET_FRAG_CHAIN} {new_path} {chain_peptide} {start_peptide} {end_peptide} > {to_copy_path_P}", shell=True)

    sp.run(f"{NAME_CHAIN} {to_copy_path_sh} {SH2_CHAIN}", shell=True)
    sp.run(f"{NAME_CHAIN} {to_copy_path_P} {P_CHAIN}", shell=True)


if __name__ == '__main__':
    all_pdb_path = sys.argv[1]

    if os.path.exists(f"{all_pdb_path}/{ACTUAL_DATA_DIR_NAME}"):
        sp.run(f"rm -rf {all_pdb_path}/{ACTUAL_DATA_DIR_NAME}", shell=True)
    filter_pdbs(all_pdb_path, ALIGNMENT_THRESHOLD, SH2_REF_PATH)


