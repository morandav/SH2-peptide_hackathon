<h1>User manual</h1>

<h2>Description:</h2>
3D protein structure course hackathon. This project predicts SH2 domain and peptide structure using neural network.

<h2>Data Processing</h2>
<h3>Steps:</h3>
1. Download pdb files - 
extract pdb files according to the experimental method: Xray and NMR<br>
2. Choose a pdb file with a good resolution SH2 chain and peptide to be determined as the reference structures.<br>
3. Change .ent to .pdb files extension<br>
4. Split each pdb file to multiple pdb files containing one chain using extract_chains.py. And created the directory structure: all_pdbs/<Xray|NMR>/<pdb_id>/<pdb_id>_<chain_id>.pdb <br>

![Picture2](https://user-images.githubusercontent.com/58668084/174499907-a1ff017e-cf37-4f53-bf10-6ac4a48dcad6.png)
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
Inside the pdb data directory a new directory called actual_data contains a directory for each pdb file. Inside each one of these directories there will be a pdb of the peptide and a pdb of the SH2 chain. <br>
 
![Picture3](https://user-images.githubusercontent.com/58668084/174499951-6e6a64f5-8981-46eb-8739-a8c5b85c25b6.png)


<h3>Program overview</h3>
The program filters the pdb files to obtain the ones that contain a good resolution SH2 chain and peptide.<b> SH2_REF_PATH</b> represents the SH2 pdb file with a good resolution which is used as the reference. The program goes over all the chains in each pdb, alignes them to the reference SH2, and identifies the specific chain that has the most atoms aligned with the reference. The program then applies the relevant transformation to the whole pdb file, and searches for the matching peptide. This was done by finding the closest chain to the reference peptide. Only pdf files that contain a SH2 chain and a matching peptide, according to the filtering process explained, were added to the data set.<br>

 
 <h2>SH2 and peptide neural network modeling</h2>
<h3>Steps :</h3>
 1. <b>utils.ipynb</b> script: creates input and labels to SH2 and peptide neural network<br>
 2. <b>net.ipynb</b> script: create a new network / use the saved model. <br>
3. The predicted structures are saved as pdb files splitted to to different directories according to the original pdb name.<br>
<h3>Setup :</h3>
In order to create SH2 and peptide neural network model
and predict with it, follow these setup steps: <br>
* In utils.ipynb: <br> 
<t>1. Update <data_path> to the path actual_data directory you have created in the previous step (Data Processing). <br>
If you did not follow the Data Processing steps, you need to give a path which is a path to a directory. In the directory there are several directories, representing different pdbs, contains:<br>
pdb-name_SH2_<chain_id>.pdb 	pdb-name_peptide_<chain_id>.pdb<br>
<t>2. Update <save_path> to path to where you want to save the data you need for the network train and validation <br>
<t>3. Run the script <br>
* In net.ipynb: <br>
1. Optional: update models’ parameters in the parameters section <br>
2. Update <data_path> to to <save_path> you chose in utils script <br>
3. If you create a new model: update <ckpt_best_path> to the path to where you want to save your best ckpt <br>
4.If you want to use exist model: update  <ckpt_path> to the path of the model <br>
5. Update <save_path> to where you want to save pdb predictions <br>
6. Run the script<br>

<h3>Input : </h3>
 The input of the neural network is a one-hot encoding matrix of the sequences of the SH2 and peptide, and another 2 columns representing whether the amino acid belongs to the SH2 domain or peptide.
 
<h3>Output : </h3>
* Trained model check point <br>
* The output of the model will be the backbone (N, C⍺, C, O) and Cβ x,y,z coordinates of the SH2 and peptide combined structure <br>
* The script creates pdb files from the network’s output <br>

 <h3>Program overview:</h3>
The program builds a convolution neural network, which predicts a structure of SH2 attached to a peptide.<br>
The network structure is as follow:<br>
 
 ![Picture1](https://user-images.githubusercontent.com/58668084/174499800-97bf4fd4-f687-4359-a710-5ebc24efc63b.png)

 The network consists of the following layers: <br>
1. 1D convolution - ‘decodes’ our one-hot encoding representation<br>
2. First ResNet - this layer consists of k ResNet blocks, each consists of: Input layer -> Batch normalization layer -> 1D convolutional layer -> Relu activation layer -> Batch normalization layer -> 1D convolutional layer -> Relu activation layer -> pointwise addition of the input layer and the last layer. <br>
3. Another 1D convolution <br>
4. Second ResNet - this layer consists of n*m dilated ResNet blocks (n - number of repetitions to make, m- length of the dilation list). each block consists of: Input layer -> Batch normalization layer -> dilated 1D convolutional layer -> Relu activation layer-> Batch normalization layer -> dilated 1D convolutional layer -> Relu activation layer -> pointwise addition of the input layer and the last layer. Again, the last layer becomes the input layer for the next ResNet block.<br>
5. Dropout layer- regularization layer. In each step of training it randomly sets some of the input weights to zero (with a percentage of your choice). <br>
6. Another 1D convolution <br>
7. Dense layer - a simple fully connected layer, projects the matrices to the desired output size.<br>

All parameters (k,n,m,dropout percentage are available in net.ipynb and can be change for you choice)

 


 
