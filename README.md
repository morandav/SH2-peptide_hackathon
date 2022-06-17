<h1>User manual</h1>

<h2>Description:</h2>
3D protein structure course hackathon. This project predicts SH2 domain and peptide structure using neural network.

<h2>Data Processing</h2>
<h3>Steps:</h3>
1. Download pdb files - 
extract pdb files according to the experimental method: Xray and NMR<br>
2. Choose a pdb file with a good resolution SH2 chain and peptide to be determined as the reference structures.<br>
3. Change .ent to .pdb files extension<br>
4. Split each pdb file to multiple pdb files containing one chain using extract_chains.py. And created the directory structure: all_pdbs/<Xray|NMR>/<pdb_id>/<pdb_id>_<chain_id>.pdb ![image](https://user-images.githubusercontent.com/58668084/174358003-785319d0-78ba-47cb-a62a-849dee8d29ee.png)
<br>
5. Process the data and filter the pdb files to obtain the ones that contain a good resolution SH2 chain and peptide, using process_data.py.<br>

<h3>Setup:</h3>
This setup is made and tested for linux with bash or sh as the running shell.
In order to use the data processing program, follow these setup steps:<br>
<p>* Download files:  
<b>proteinHack</b> - receives epsilon,  a reference pdb and a whole protein pdb. It outputs <chain> <start index> <end index> of the chain that is closest to the reference
<b>Process_data.py</b> - the running program<br>
 <b>alignMPtrans.pl</b> - a program that performs alignment<br>
 <b>pdb data</b> - the data of the pdb as described above<br></p>
<p>* In the file process_data.py change the global variables : <br>
 <b>SH2_REF_PATH</b> - to the absolute path containing the reference pdb to SH2<br>
 <b>PEPTIDE_REF</b> -  to the  absolute path containing the reference pdb to SH2’s peptide<br>
 <b>PROTEINHACK_PATH</b> - to the absolute path where proteinHack is saved<br></p>
 <p>* The pdb data should be in the next format:<br>
1. inside the pdb data directory there should be other directories (NMR / Xray) <br>
2. inside each directory add the file alignMPtrans.pl and a directory for each pdb file  <br>
3. inside the pdb file directory add the relevant pdb file, and a new pdb file for each chain of protein.</p> 

 <h3>Input: </h3>
Run command: <br>
Python process_data.py < path to pdb data directory> 

<h3>Output: </h3>
Inside the pdb data directory a new directory called actual_data contains a directory for each pdb file. Inside each one of these directories there will be a pdb of the peptide and a pdb of the SH2 chain. 
![image](https://user-images.githubusercontent.com/58668084/174358300-dffbdf93-a271-4116-97ae-5268c5082252.png)


<h3>Program overview</h3>
The program filters the pdb files to obtain the ones that contain a good resolution SH2 chain and peptide.<b> SH2_REF_PATH</b> represents the SH2 pdb file with a good resolution which is used as the reference. The program goes over all the chains in each pdb, alignes them to the reference SH2, and identifies the specific chain that has the most atoms aligned with the reference. The program then applies the relevant transformation to the whole pdb file, and searches for the matching peptide. This was done by finding the closest chain to the reference peptide. Only pdf files that contain a SH2 chain and a matching peptide, according to the filtering process explained, were added to the data set.<br>

<p>Extract_chains.py - <br>
This script creates specific pdb files for each chain, using /cs/staff/dina/scripts/extractChains.pl  script. Each pdb file is created inside a directory named pdb_id, the original pdb file containing all chains was also moved inside this directory.</p>
 
 <h2>SH2 and peptide neural network modeling</h2>
<h3>Steps :</h3>
1. utils.ipynb script: creates input and labels to SH2 and peptide neural network<br>
2. net.ipynb script: create a new network / use the saved model. <br>
3. The predicted structures are saved as pdb files splitted to to different directories according to the original pdb name.<br>
<h3>Setup :</h3>
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

<h3>Output : </h3>
Trained model check point
Pdb files of the model predictions

 <h3>Program overview:</h3>
?????????????
