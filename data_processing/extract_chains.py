import os
import sys
import subprocess as sp


def extract_chains_to_subdir(path):
    """
    Split all pdb files to pdb files according to chains.
    :param path: pdbs directory path
    """
    os.chdir(path)
    for pdb_file in os.listdir():
        print("extracting: ",pdb_file)
        os.chdir(path)
        dir_name = pdb_file.split('.')[0]
        if dir_name in os.listdir('.'):
            if len(os.listdir(dir_name)) <2:
                sp.run(["/cs/staff/dina/scripts/extractChains.pl", pdb_file])
                continue
            continue
        os.mkdir(dir_name)
        os.replace(pdb_file, dir_name+"/"+pdb_file)
        os.chdir(dir_name)
        sp.run(["/cs/staff/dina/scripts/extractChains.pl", pdb_file])


if __name__ == "__main__":
    nmr_path = "/cs/usr/moran_david/Downloads/original/all_pdbs/NMR/"
    xray_path = "/cs/usr/moran_david/Downloads/all_pdbs/Xray"

    print("####### NMR dir:")
    extract_chains_to_subdir(nmr_path)
    print("####### Xray dir:")
    extract_chains_to_subdir(xray_path)

