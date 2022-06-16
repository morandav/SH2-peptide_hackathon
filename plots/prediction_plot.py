import os
import subprocess as sp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


BASE_PATH = "/cs/usr/ehassid/Downloads/"
SCRIPT_DIR = "/cs/usr/ehassid/PycharmProjects/proteins_hackathon/"
sh2_ref_path = "pdb6pxc.A.pdb"
sh2_predicted_files = ["/cs/usr/ehassid/Downloads/actual_data/pdb1bmb/pdb1bmb_SH2_A.pdb", "pdb6pxc.A.pdb"]
pred_dir = os.path.join(BASE_PATH, "pred_pdbs")
reference_dir = os.path.join(BASE_PATH, "actual_data")
ALIGN = "/cs/usr/ehassid/PycharmProjects/proteins_hackathon/alignMPtrans.pl"


def get_data():
    """
    returns a list [match_num, transition, RMSD] taken from "2_sol.res" in the current dir
    """
    if not os.path.exists(os.path.join(BASE_PATH,"2_sol.res")):
        return None
    output_file = open(os.path.join(BASE_PATH,"2_sol.res"))
    content = output_file.readlines()
    RMSD = float((content[12].split()[-1]))
    return RMSD


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
            sp.run([ALIGN, ref_path, f, "out"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
            data_list = get_data()  # get relevant data from 2_sol.res
            if data_list[0] > match_num_threshold:
                data_dict[f] = data_list

    os.chdir("..")
    return data_dict


def get_pred_sh2_rmsds():
    """
    returns a list of all predicted peptides RMSD from alignment against the reference peptide
    """
    sh2_rmsds = []
    os.chdir(BASE_PATH)
    for pdb_dir in os.listdir(pred_dir):
        # print("----- checking RMSD for SH2: ", pdb_dir)
        for pdb_file in os.listdir(os.path.join(pred_dir,pdb_dir)):
            if pdb_file.find("SH2") != -1:
                sh2_pred_path = os.path.join(pred_dir,pdb_dir,pdb_file)
                pdb_ref_path = os.path.join(reference_dir, pdb_dir)
                sh2_ref_path = ""
                for ref_file in os.listdir(pdb_ref_path):
                    if pdb_file.find("SH2") != -1:
                        sh2_ref_path = os.path.join(pdb_ref_path, ref_file)
                sp.run([ALIGN, sh2_ref_path, sh2_pred_path, "out"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
                rmsd = get_data()  # get relevant data from 2_sol.res
                if (rmsd == None):
                    print("No RMSD for file: ", pdb_file)
                sh2_rmsds.append(rmsd)
    return sh2_rmsds


def get_pred_peptide_rmsds():
    """
    returns a list of all predicted peptides RMSD from alignment against the reference peptide
    """
    peptide_rmsds = []
    os.chdir(BASE_PATH)
    for pdb_dir in os.listdir(pred_dir):
        # print("----- checking RMSD for peptide: ", pdb_dir)
        for pdb_file in os.listdir(os.path.join(pred_dir,pdb_dir)):
            if pdb_file.find("peptide") != -1:
                pept_pred_path =os.path.join(pred_dir,pdb_dir,pdb_file)
                pdb_ref_path = os.path.join(reference_dir, pdb_dir)
                pept_ref_path = ""
                for ref_file in os.listdir(pdb_ref_path):
                    if pdb_file.find("SH2") != -1:
                        pept_ref_path = os.path.join(pdb_ref_path, ref_file)
                sp.run([ALIGN, pept_ref_path, pept_pred_path, "out"], stdout=sp.DEVNULL, stderr=sp.DEVNULL)
                rmsd = get_data()  # get relevant data from 2_sol.res
                if (rmsd == None):
                    print("No RMSD for file: ", pdb_file)
                peptide_rmsds.append(rmsd)
    return peptide_rmsds


if __name__ == "__main__":
    sh2_rmsds = get_pred_sh2_rmsds()
    peptide_rmsds = get_pred_peptide_rmsds()
    print(len(sh2_rmsds))
    print(len(peptide_rmsds))

    df = pd.DataFrame(data=[sh2_rmsds, peptide_rmsds], index=['SH2', 'Peptide'])
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111)
    # Creating plot
    ax.boxplot(df)
    plt.xticks([1, 2], ["SH2", "Peptide"])
    ax.set_xlabel('protein')
    ax.set_ylabel('RMSD')
    plt.show()