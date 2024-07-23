import numpy as np
import scipy.constants as cst
import subprocess as sub
import os

#Program that automatically run multiple simulations in a row to create a plot

#Function substituting lines to modify each Allpix simulation
def write(nom_fichier, numero_ligne, contenu):
    with open(nom_fichier, 'r') as f:
        lignes = f.readlines()

    if 0 < numero_ligne <= len(lignes):
        lignes[numero_ligne-1] = contenu + '\n'
    else:
        print("Invalid line number.")

    with open(nom_fichier, 'w') as f:
        f.writelines(lignes)

#Erasing old files to avoid conflicts
if os.path.exists('pi+.txt'):
    os.remove('pi+.txt')
if os.path.exists('kaon.txt'):
    os.remove('kaon.txt')
if os.path.exists('mu+.txt'):
    os.remove('mu+.txt')

#adaptable loop for each variable
#The detector mimosa23 is in the file detector.conf while the Allpix file to execute is in simple_detector.conf
for particle in ['pi+','kaon+','mu+']:
    write('allpix_conf/simple_detector.conf',16,f'particle_type = "{particle}"')
    for i in np.arange(100,1050,50):
        #write('allpix_conf/detector.conf',5,f'orientation = {i}deg 0deg 0deg')             #angle variation
        write('allpix_conf/simple_detector.conf',18,f'source_energy = {i}MeV')              #energy variation
        #write('allpix_conf/simple_detector.conf',12,f'magnetic_field = 0T {i}T 0T')        #magnetic field variation

        write('data_create.cpp',42,rf'fichier << "{i}\t" << somme << std::endl;')           #write the i variable in a c++ file that will get the result from the simulation in the ROOT file

                                                                                            #name of the output file holding the interesting result
        #write('data_create.cpp',64,rf'data_create("output/modules.root","DetectorHistogrammer/Detector/cluster_size/cluster_size","{particle}.txt");')
        write('data_create.cpp',65,rf'data_create("output/modules.root","DetectorHistogrammer/Detector/charge/total_charge","{particle}.txt");')

        #write('data_create.cpp',58,rf'fichier1 << "{i}\t" << max << std::endl;')           #write the histogram's max value

                                                                                            #execute the simulation
        sub.run('g++ -o data_create.exe data_create.cpp `root-config --cflags --glibs`',shell=True)
        sub.run('allpix -c allpix_conf/simple_detector.conf',shell=True)
        sub.run('./data_create.exe',shell=True)
