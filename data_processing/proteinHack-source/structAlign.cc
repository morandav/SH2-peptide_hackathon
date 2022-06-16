#include <iostream>
#include <map>
#include "Vector3.h"
#include "Atom.h"
#include "RigidTrans3.h"
#include "Molecule.h"
#include "PDB.h"
#include "Match.h"
#include "GeomHash.h"
#include "Triangle.h"






int main(int argc , char* argv[]){

	if(argc !=4) {
		std::cerr << "Usage: "<<argv[0]<< " epsilon sh2peptide.pdb whole.pdb" << std::endl;
		exit(1);
	}

	//********Parameters********************
	float epsilon = atof(argv[1]); // distance threshold on atoms in correspondence

	// read the two files into Molecule

	std::ifstream fileRefPeptide(argv[2]);
	std::ifstream fileWholePDB(argv[3]);

	if(!fileRefPeptide) {
		std::cout<< "File " << argv[3] << " does not exist." << std::endl;
		return 0;
	}
	if(!fileWholePDB) {
		std::cout << "File " << argv[2] << " does not exist." << std::endl;
		return 0;
	}


	// create molecules
	Molecule<Atom> molRef, molWholePDB;
	molRef.readPDBfile(fileRefPeptide, PDB::CAlphaSelector());
	molWholePDB.readPDBfile(fileWholePDB, PDB::CAlphaSelector());


	// next we insert the whole PDB molecule into hash
	// this will help us to find atoms that are close faster
	GeomHash <Vector3,int> gHash(3,epsilon); // 3 is a dimension and m_fDistThr is the size of the hash
	// cube
	for(unsigned int i=0; i<molWholePDB.size(); i++) {
		gHash.insert(molWholePDB[i].position(), i); // coordinate is the key to the hash, we store atom index
	}


	// match is a class that stores the correspondence list, eg.
	// pairs of atoms, one from each molecule, that are matching
	Match match;
	// find close target molecule atoms using the hash
	for(unsigned int i=0; i<molRef.size(); i++) {
	    HashResult<int> result;
	    Vector3 peptideCa = molRef[i].position();
	    gHash.query(peptideCa, epsilon, result); // key is mol atom coordinate

	    // check if the atoms in the result are inside the distance threshold
	    // the hash is a cube shape, there can be atoms further that the threshold
	    for(auto x = result.begin(); x != result.end(); x++) {
	        float dist = peptideCa.dist(molWholePDB[*x].position());
	        if(dist <= epsilon) {
	            float score = (1 / (1 + dist));
	            match.add( *x , i, score, score );
	        }
	    }
	    result.clear();
	}

	std::map<char, std::vector<int>> results;
	char best = '@';
    for(unsigned int i=0; i<match.size(); i++) {
        unsigned int wholeMolIndex = match[i].model;
        auto iter = results.find(molWholePDB[wholeMolIndex].chainId());
        if ( iter != results.end()) {
            iter->second.push_back(molWholePDB[wholeMolIndex].residueIndex());
        }
        else {
            results.insert( std::pair<char,std::vector<int>>(molWholePDB[wholeMolIndex].chainId(),{}));
        }


        int max_amount=0;
        for (auto val : results){
            if(val.second.size() > max_amount){
                best = val.first;
                max_amount = val.second.size();
            }
        }

    }
    if (best == '@'){
        std::cout << best << " " << 0 << " " << 0 << std::endl;
    }
    else{
        auto n_iter = results.find(best);
        std::cout << best << " " << *min_element(n_iter->second.begin(), n_iter->second.end())-2 << " " << *max_element(n_iter->second.begin(), n_iter->second.end())+2 << std::endl;
    }

	

}
