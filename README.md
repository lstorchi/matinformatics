
Just some basic test used in a cooperative work related to material informatics 

Run using separate Data and AtomicData

  # generate features
  python3 generatefeats.py  -f ./data/Data.xlsx -b "IP[1];EA[1];Z[0];rs[2];rp[2];rd[2];HOMOKS[3];LUMOKS[3]" -d 10

  # select best 1D features
  python3 ffilter.py -f newadata.pkl -n 50

  # generate 2D features starting from the best 1D and select the best ones
  python3 generate2Dfeats.py -f feature_rmse.csv -n 50 -k newadata.pkl --numoffeatures 1000

  # generate 3D features starting from the best 1D and select the best ones
  python3 generate3Dfeats.py  -f feature_rmse.csv -n 50 -k newadata.pkl --numoffeatures 10

  # collect output and 
  python3 23Dfeatsexctratand.py -d ./2DFeatures/ -k newadata.pkl
  python3 23Dfeatsexctratand.py -d ./3DFeatures/ -k newadata.pkl --set3Don

Run using a single Dataset no Atomic Data 

  Label are  formation_energy_ev_natom[5];bandgap_energy_ev[5]

  # generates basic features
  python3 generatefeats_matdata.py -b "spacegroup[1];number_of_total_atoms[1];percent_atom_al[2];percent_atom_ga[2];percent_atom_in[2];lattice_vector_1_ang[3];lattice_vector_2_ang[3];lattice_vector_3_ang[3];lattice_angle_alpha_degree[4];lattice_angle_beta_degree[4];lattice_angle_gamma_degree[4];avg_dist_Ga[6];avg_dist_Al[6];avg_dist_In[6];V_alpha[1];Density[7]" -f ./data/updated_dataset.xlsx
  python3 generatefeats_matdata.py -b "spacegroup[1];number_of_total_atoms[1];percent_atom_al[2];percent_atom_ga[2];percent_atom_in[2];lattice_vector_1_ang[3];lattice_vector_2_ang[3];lattice_vector_3_ang[3];lattice_angle_alpha_degree[4];lattice_angle_beta_degree[4];lattice_angle_gamma_degree[4];avg_dist_Ga[6];avg_dist_Al[6];avg_dist_In[6];V_fu[1];Density[7]" -c ./data/V_fu_added.csv -v -r 

  # split by spacegroup

  for id in  33 194 227 167 12 206
  do
    python3 generatefeats_matdata.py -b "percent_atom_al[2];percent_atom_ga[2];percent_atom_in[2];lattice_vector_1_ang[3];lattice_vector_2_ang[3];lattice_vector_3_ang[3];lattice_angle_alpha_degree[4];lattice_angle_beta_degree[4];lattice_angle_gamma_degree[4];avg_dist_Ga[6];avg_dist_Al[6];avg_dist_In[6];V_fu[1];Density[7]" -c ./data/V_fu_added.csv -v -r  --split "spacegroup;$id" > out_"$id" &
  done


  for id in  33 194 227 167 12 206
  do 
    python3 ffilter.py -f newadataspacegroup_"$id".pkl -i "./data/V_fu_added.csv,formation_energy_ev_natom" --split "spacegroup;$id" -o feature_rmse_"$id".csv > out_ff_"$id" &
  done

Running using our data (three atoms):

  # to generate 1D features
  python generatefeats_pelect.py -f ./data/param.xlsx -b "rs[1];rp[1];EA[2];IP[2]"
  python generatefeats_pelect.py -f ./data/param.xlsx -b "rs[1];rp[1];EA[2];IP[2]" -m 2 -v -r 

  # select best 1D features
  python3 ffilter.py -f newadata.pkl -n 50


