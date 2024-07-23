import numpy as np
import re
from scipy import constants as cst

#Computes every possible particle generated from the collision proton-titanium from the physic list
def read_from_file():
    file_path = 'particles_from_target.txt'
    file_o = 'simple_detector.conf'
    mass_list = np.zeros(50)
    mass_list[1] = 938.272
    mass_list[8] = 939.5654
    mass_list[10] = 105.65837
    mass_list[11] = 105.65837
    mass_list[13] = 139.57018
    mass_list[14] = 139.57018
    mass_list[15] = 493.67
    mass_list[17] = 1115.68
    mass_list[25] = 497.61
    mass_list[24] = 497.61
    mass_list[-6] = 3727.379
    mass_list[-5] = 2808.39
    mass_list[-3] = 1875.6
    mass_list[-4] = 2808.921136
    with open (file_path,'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            ID, x, y, z, px, py, pz = map(float,line.split())
            ID = int(ID)
            x,y,z = map(str,[x,y,z])
            if ID == 1:
                l16 = "particle_type = 2212"
            elif ID == 8:
                l16 = "particle_type = 2112"
            elif ID == 10:
                l16 = "particle_type = -13"
            elif ID == 11:
                l16 = "particle_type = 13"
            elif ID == 13:
                l16 = "particle_type = 211"
            elif ID == 14:
                l16 = "particle_type = -211"
            elif ID == 15:
                l16 = "particle_type = 321"
            elif ID == 17:
                l16 = "particle_type = 3122"
            elif ID == 24:
                l16 = "particle_type = 311"
            elif ID == 25:
                l16 = "particle_type = -311"
            elif ID == -3:
                l16 = "particle_type = 1000010020"
            elif ID == -4:
                l16 = "particle_type = 1000010030"
            elif ID == -5:
                l16 = "particle_type = 1000020030"
            elif ID == -6:
                l16 = "particle_type = 1000020040"
            else:
                print("unknown particle",ID)
                continue
            p = px**2+py**2+pz**2
            psquared = np.square(p)
            energy = np.sqrt(p + mass_list[ID]**2) - mass_list[ID]
            write(file_o,16,l16)
            write(file_o,19,"source_position = "+x+"cm "+y+"cm "+z+"cm")
            write(file_o,18,f"source_energy = {energy}MeV")
            write(file_o,23,f"beam_direction = {px/psquared} {py/psquared} {pz/psquared}")
    return 0
                
    
    
def write(nom_fichier, numero_ligne, contenu):
    with open(nom_fichier, 'r') as f:
        lignes = f.readlines()

    if numero_ligne <= len(lignes):
        lignes[numero_ligne-1] = contenu + '\n'
    else:
        print("Invalid line number.")

    with open(nom_fichier, 'w') as f:
        f.writelines(lignes)



read_from_file()
