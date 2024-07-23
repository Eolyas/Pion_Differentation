import numpy as np
import re
from scipy import constants as cst

#makes a list of every particle of type 211
def search():
    file_path = input("File path: ")
    list_particle = []

    with open(file_path,'r') as file:
        lines = file.readlines()
        pattern_f = re.compile(f"[-]*\d*\.\d+")
        for i in range(len(lines)):
            test = re.match("Particle type \(PDG ID\):     211",lines[i])
            if test:
                i += 2
                pos_list = pattern_f.findall(lines[i])
                i += 4
                pos_list.append(pattern_f.findall(lines[i])[0])
                list_particle.append(pos_list)

    list_particle_no_time = np.zeros((len(list_particle),3))
    for j in range(len(list_particle)):
        for k in range(4):
            list_particle[j][k] = float(list_particle[j][k])
            if not k == 3:
                list_particle_no_time[j][k] = list_particle[j][k]
    return list_particle,list_particle_no_time

#Calculates the speed and momentum of every particle and outputs them in a readable file
def calcul():
    list_particle, off = search()
    weight = 139.57018
    c = cst.speed_of_light
    nb_dect = 6
    file_output = input("Output file : ")
    with open(file_output,'w') as file:
        vnorm = np.zeros(5)
        pnorm = np.zeros(5)
        for j in range(int(len(list_particle)/nb_dect)):
            vx = []
            vy = []
            vz = []
            p = []
            weight = 139.57018
            j *= nb_dect
            i=0
            file.write("Particle {}\n".format(1+int(j/5)))
            for i in range(nb_dect-1):
                vx.append((10**6)*(list_particle[i+j][0] - list_particle[i+1+j][0]) / (list_particle[i+j][3] - list_particle[i+1+j][3]))
                vy.append((10**6)*(list_particle[i+j][1] - list_particle[i+1+j][1]) / (list_particle[i+j][3] - list_particle[i+1+j][3]))
                vz.append((10**6)*(list_particle[i+j][2] - list_particle[i+1+j][2]) / (list_particle[i+j][3] - list_particle[i+1+j][3]))
                v = np.sqrt(vx[i]**2+vy[i]**2+vz[i]**2)
                gamma = np.sqrt(1/(1-(v/c)**2))
                p = gamma*weight*v
                E = gamma*weight
                Ec = E-weight
                vnorm[i] += np.sqrt(vx[i]**2+vy[i]**2+vz[i]**2)
                file.write("===============================================\n"
                "Timestep {}\n"
                "                x           y           z\n"
                "Speed:      {:.3f}  {:.3f}  {:.3f}  m/s\n"
                "momentum:  {:.3f}\n"
                "Energy:    {:.3f}\n"
                "Energy c:  {:.3f}\n".format(i+1, vx[i], vy[i], vz[i],p,E,Ec))
            file.write("\n\n")
        vnorm *= 0.1
        pnorm = weight*vnorm*(1/np.sqrt(1-(vnorm/c)**2))
        file.write("Avg     Speed       Momentum\n"
                   "1       {:.3f}  {:.3f}\n"
                   "2       {:.3f}  {:.3f}\n"
                   "3       {:.3f}  {:.3f}\n"
                   "4       {:.3f}  {:.3f}\n".format(vnorm[0],pnorm[0],vnorm[1],pnorm[1],vnorm[2],pnorm[2],vnorm[3],pnorm[3]))
    
    return 0

calcul()
