# SH2-peptide_hackathon
3D protein structure course hackathon.
User manual

Program overview:
This project predicts SH2 domain and peptide structure using neural network.

Data Processing
Steps:
Download pdb files - 
extract pdb files according to the experimental method: Xray and NMR
Choose a pdb file with a good resolution SH2 chain and peptide to be determined as the reference structures.
Change .ent to .pdb files extension
Split each pdb file to multiple pdb files containing one chain using extract_chains.py. And created the directory structure: all_pdbs/<Xray|NMR>/<pdb_id>/<pdb_id>_<chain_id>.pdb

Process the data and filter the pdb files to obtain the ones that contain a good resolution SH2 chain and peptide, using process_data.py.

Setup :
This setup is made and tested for linux with bash or sh as the running shell.
In order to use the data processing program, follow these setup steps:
Download files:  
proteinHack - receives epsilon,  a reference pdb and a whole protein pdb. It outputs <chain> <start index> <end index> of the chain that is closest to the reference
Process_data.py - the running program
alignMPtrans.pl - a program that performs alignment
pdb data - the data of the pdb as described above
In the file process_data.py change the global variables : 
SH2_REF_PATH - to the absolute path containing the reference pdb to SH2
 PEPTIDE_REF -  to the  absolute path containing the reference pdb to SH2’s peptide
PROTEINHACK_PATH - to the absolute path where proteinHack is saved
The pdb data should be in the next format:
inside the pdb data directory there should be other directories (NMR / Xray) 
 inside each directory add the file alignMPtrans.pl and a directory for each pdb file  
inside the pdb file directory add the relevant pdb file, and a new pdb file for each chain of protein. 
Input  :
Run command: 
Python process_data.py < path to pdb data directory> 

Output : 
Inside the pdb data directory a new directory called actual_data contains a directory for each pdb file. Inside each one of these directories there will be a pdb of the peptide and a pdb of the SH2 chain. 


Program overview
The program filters the pdb files to obtain the ones that contain a good resolution SH2 chain and peptide. SH2_REF_PATH represents the SH2 pdb file with a good resolution which is used as the reference. The program goes over all the chains in each pdb, alignes them to the reference SH2, and identifies the specific chain that has the most atoms aligned with the reference. The program then applies the relevant transformation to the whole pdb file, and searches for the matching peptide. This was done by finding the closest chain to the reference peptide. Only pdf files that contain a SH2 chain and a matching peptide, according to the filtering process explained, were added to the data set.



Extract_chains.py - 
This script creates specific pdb files for each chain, using /cs/staff/dina/scripts/extractChains.pl  script. Each pdb file is created inside a directory named pdb_id, the original pdb file containing all chains was also moved inside this directory.
SH2 and peptide neural network modeling
Steps :
utils.ipynb script: creates input and labels to SH2 and peptide neural network
net.ipynb script: create a new network / use the saved model. 
The predicted structures are saved as pdb files splitted to to different directories according to the original pdb name.
Setup :
In order to create SH2 and peptide neural network model
and predict with it, follow these setup steps:
In utils.ipynb: 
Update <data_path> to the path actual_data directory you have created in the previous  step (Data Processing).
If you did not follow the Data Processing steps, you need to give a path which is a path to a directory. In the directory there are several directories, representing different pdbs, contains:
pdb-name_SH2_<chain_id>.pdb 	pdb-name_peptide_<chain_id>.pdb
Update <save_path> to path to where you want to save the data you need for the network train and validation
Run the script
In net.ipynb: 
Optional: update models’ parameters in the parameters section
Update <data_path> to to <save_path> you chose in utils script
If you create a new model: update <ckpt_best_path> to the path to where you want to save your best ckpt
If you want to use exist model: update  <ckpt_path> to the path of the model
Update <save_path> to where you want to save pdb predictions
Run the script

Output : 
Trained model check point
Pdb files of the model predictions

Program overview:
?????????????
