
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

Last Run using new  data:

  python3 generatefeats.py -f ./data/NewData.xlsx  -b "Z[1];atomic_hfomo[2];atomic_lfumo[2];atomic_ea_by_energy_difference[3];atomic_ip_by_energy_difference[3];atomic_rs_max[4];atomic_rp_max[4]" -j -v
  python3 generatefeats.py -f ./data/NewData.xlsx  -b "Z[1];atomic_hfomo[2];atomic_lfumo[2];atomic_ea_by_half_charged_homo[3];atomic_ip_by_half_charged_homo[3];atomic_rs_max[4];atomic_rp_max[4]" -j -v 
  python3 generatefeats.py -f ./data/NewData.xlsx  -b "Z[1];atomic_hpomo[2];atomic_lpumo[2];atomic_ea_by_energy_difference[3];atomic_ip_by_energy_difference[3];atomic_rs_max[4];atomic_rp_max[4]" -j -v 

  # full production using a set:

  python3 generatefeats.py -f ./data/NewData.xlsx  -b "Z[1];atomic_hpomo[2];atomic_lpumo[2];atomic_ea_by_energy_difference[3];atomic_ip_by_energy_difference[3];atomic_rs_max[4];atomic_rp_max[4]" -j -v
  python3 ffilter.py -f newadata.pkl -n 50
  
  # 2D features on several machines
  for name in lista machine names:
  do
      scp  newadata.pkl newadata.csv feature_rmse.csv feature_rmse.csv formulaslist.txt $machinename:matinformatics/
  done

  # in the script ./run_mutiple.sh set PROGNAME=generate2Dfeats.py, if we want to scan up to 10000 and use 3 processors
  # the script wil suggest the next run
  ./run_mutiple.sh 100 0 3 0 10000

  # in this case will suggest ./run_mutiple.sh 5000 4 3 20000 100000 but I can decrease 
  # the number of process to be used depending on the machine selected:
  ./run_mutiple.sh 5000 4 6 20000 100000

  # and so for the next one I can increase also the number of pairs per processor:
  ./run_mutiple.sh 6000 11 8 55000 100000

  # after I can check the estimated time and adjust:
  ./checktime.sh 

  # then collect all out_* err_* and 2Dfeature_rmse.csv_* in a single machine and dir and run  
  python3 23Dfeatsexctratand.py -d ./2DFeatures/ -k newadata.pkl

  # 3D features on several machines
  for name in lista machine names:
  do
      scp  newadata.pkl newadata.csv feature_rmse.csv feature_rmse.csv formulaslist.txt $machinename:matinformatics/
  done

  # in the script ./run_mutiple.sh set PROGNAME=generate3Dfeats.py, if we want to scan up to 10000 and use 3 processors
  # the script wil suggest the next run
  ./run_mutiple.sh 100 0 3 0 10000
 
  # and after we can proceed as for the 2D features, collecting all out_* err_* and 2Dfeature_rmse.csv_* in a single 
  # machine and dir and run
  python3 23Dfeatsexctratand.py -d ./3DFeatures/ -k newadata.pkl --set3Don

Final run :

  $ python3 generatefeats.py  -f ./data/OAD.xlsx -b "IP[1];EA[1];rs[2];rp[2];rd[2];HOMOKS[3];LUMOKS[3]" -j -m 1 --variancefilter=0.05 2> stderr.data
  $ python3 ffilter.py -f newadata.pkl -n 50
  $ python3 checksingleformula.py -f ./OAD_gen_1/newadata.pkl --formula "...." -n 1000

  $ python3 generatefeats.py  -f ./data/OAD.xlsx -b "IP[1];EA[1];rs[2];rp[2];rd[2];HOMOKS[3];LUMOKS[3]" -j -m 2 --variancefilter=0.05 2> stderr.data
  $ python3 ffilter.py -f newadata.pkl -n 50
  $ python3 checksingleformula.py -f ./OAD_gen_2/newadata.pkl --formula "...." -n 1000

  $ python3 generatefeats.py  -f ./data/OAD.xlsx -b "IP[1];EA[1];rs[2];rp[2];rd[2];HOMOKS[3];LUMOKS[3]" -j -m 3 --variancefilter=0.05 2> stderr.data
  $ python3 ffilter.py -f newadata.pkl -n 50
  $ python3 checksingleformula.py -f ./OAD_gen_3/newadata.pkl --formula "...." -n 1000


  # 2D features on several machines
  for name in lista machine names:
  do
      scp  newadata.pkl newadata.csv feature_rmse.csv feature_rmse.csv formulaslist.txt $machinename:matinformatics/
  done

  # in the script ./run_mutiple.sh set PROGNAME=generate2Dfeats.py, if we want to scan up to 10000 and use 3 processors
  # the script wil suggest the next run
  ./run_mutiple.sh 100 0 3 0 10000

  # in this case will suggest ./run_mutiple.sh 5000 4 3 20000 100000 but I can decrease 
  # the number of process to be used depending on the machine selected:
  ./run_mutiple.sh 5000 4 6 20000 100000

  # and so for the next one I can increase also the number of pairs per processor:
  ./run_mutiple.sh 6000 11 8 55000 100000

  # after I can check the estimated time and adjust:
  ./checktime.sh 

  # specifically I used
  ./run_mutiple.sh 100 0 1 0 5000
  ./run_mutiple.sh 100 2 6 200 5000
  ./run_mutiple.sh 200 9 8 900 5000
  ./run_mutiple.sh 200 18 8 2700 5000
  ./run_mutiple.sh 50 27 3 4500 5000
  ./run_mutiple.sh 50 31 3 4700 5000
  ./run_mutiple.sh 50 35 3 4900 5000

  # then collect all out_* err_* and 2Dfeature_rmse.csv_* in a single machine and dir and run  
  python3 23Dfeatsexctratand.py -d ./2DFeatures/ -k newadata.pkl

  # similarly I run the 3D after modifying the run_mutiple.sh script, specifically I used
  # specifically I used
  ./run_mutiple.sh 10 0 1 0 1000
  ./run_mutiple.sh 15 2 5 20 1000
  ./run_mutiple.sh 30 8 7 110 1000
  ./run_mutiple.sh 50 16 8 350 1000
  ./run_mutiple.sh 20 25 3 800 1000
  ./run_mutiple.sh 20 29 3 880 1000
  ./run_mutiple.sh 15 33 3 960 1000

  # collect all data in a single machine and 
  python3 23Dfeatsexctratand.py -d ./3DFeatures/ -k newadata.pkl --set3Don


# using new atomic DataSet

  $ python3 generatefeats.py  -f ./data/NAD.xlsx -b "IP[1];EA[1];rs[2];rp[2];rd[2];HOMO[3];LUMO[3]" -j -m 1 --variancefilter=0.05 --useatomname "A" 2> stderr
  $ python3 ffilter.py -f newadata.pkl -n 50
  $ python3 checksingleformula.py -f ./NAD_gen_1/newadata.pkl --formula "...." -n 1000

  $ python3 generatefeats.py  -f ./data/NAD.xlsx -b "IP[1];EA[1];rs[2];rp[2];rd[2];HOMO[3];LUMO[3]" -j -m 2 --variancefilter=0.05 --useatomname "A" 2> stderr
  $ python3 ffilter.py -f newadata.pkl -n 50
  $ python3 checksingleformula.py -f ./NAD_gen_2/newadata.pkl --formula "...." -n 1000

  $ python3 generatefeats.py  -f ./data/NAD.xlsx -b "IP[1];EA[1];rs[2];rp[2];rd[2];HOMO[3];LUMO[3]" -j -m 3 --variancefilter=0.05 --useatomname "A" 2> stderr
  $ python3 ffilter.py -f newadata.pkl -n 50
  $ python3 checksingleformula.py -f ./NAD_gen_3/newadata.pkl --formula "...." -n 1000


# For the new data need to consider also the variancefilter maybe

  python3 generatefeats_pelect.py  -f ./data/FENAD.xlsx -b "IP[1];EA[1];rs[2];rp[2];rd[2];HOMO[3];LUMO[3]" -j -m 1 -l "PE-AFE"
  python3 ffilter.py -f newadata.pkl -n 50 -i "./data/FENAD.csv,PE-AFE"
  python3 checksingleformula.py -f  ./FENAD_gen_1/PEAFE/newadata.pkl -i "./data/FENAD.csv,PE-AFE" -n 1000  --formula "..."

  python3 generatefeats_pelect.py  -f ./data/FENAD.xlsx -b "IP[1];EA[1];rs[2];rp[2];rd[2];HOMO[3];LUMO[3]" -j -m 1 -l "FE-AFE"
  python3 ffilter.py -f newadata.pkl -n 50 -i "./data/FENAD.csv,FE-AFE"
  python3 checksingleformula.py -f  ./FENAD_gen_1/PEAFE/newadata.pkl -i "./data/FENAD.csv,FE-AFE" -n 1000  --formula "..."

# After last update

  python3 generatefeats_pelect.py  -f ./data/FENAD.xlsx -b "IP[1];EA[1];rs[2];rp[2];rd[2];HOMOKS[3];LUMOKS[3]" -j -m 1 -l "PE-AFE" --sheetnames "list_compatible_OAD,OAD AtomcData" 
  python3 ffilter.py -f newadata.pkl -n 50 -i "./data/FENAD.xlsx,PE-AFE,list_compatible_OAD"
  python3 ./checksingleformula.py -i "./data/FENAD.xlsx,PE-AFE,list_compatible_OAD" -n 1000 -f ./newadata.pkl
  python3 finallinearfit.py 

  python3 generatefeats_pelect.py  -f ./data/FENAD.xlsx -b "IP[1];EA[1];rs[2];rp[2];rd[2];HOMOKS[3];LUMOKS[3]" -j -m 3 -l "PE-AFE" --sheetnames "list_compatible_OAD,OAD AtomcData"
  python3 ffilter.py -f newadata.pkl -n 50 -i "./data/FENAD.xlsx,PE-AFE,list_compatible_OAD"
  python3 ./checksingleformula.py -i "./data/FENAD.xlsx,PE-AFE,list_compatible_OAD" -n 1000 -f ./newadata.pkl

  python3 generatefeats_pelect.py  -f ./data/FENAD.xlsx -b "IP[1];EA[1];rs[2];rp[2];rd[2];HOMOKS[3];LUMOKS[3]" -j -m 3 -l "PE-AFE" --sheetnames "poolished_revised_list,NAD AtomicData"
  python3 ffilter.py -f newadata.pkl -n 50 -i "./data/FENAD.xlsx,PE-AFE,poolished_revised_list"
  python3 ./checksingleformula.py -i "./data/FENAD.xlsx,PE-AFE,poolished_revised_list" -n 1000 -f ./newadata.pkl
