import numpy as np
from scipy import constants as cst
import re
import subprocess as sub
import os

if os.path.exists('pi+.txt'):
    os.remove('pi+.txt')
if os.path.exists('kaon+.txt'):
    os.remove('kaon+.txt')
if os.path.exists('mu+.txt'):
    os.remove('mu+.txt')


def magnetic(particle_name, magnetic_field):
    file_path = "output/data.txt"
    if particle_name == 'pi+':
        ID = 211
        output = 'pi+.txt'
    elif particle_name == "kaon+":
        ID = 321
        output = 'kaon+.txt'
    elif particle_name == "mu+":
        ID = -13
        output = 'mu+.txt'
    else:
        print("unknown particle")
        return 0
    with open(file_path,'r') as file:
        lines = file.readlines()
        pattern = re.compile(f"[-]*\d*\.\d+")
        pattern_particle = re.compile(f"Particle type \(PDG ID\):     {ID}")
        i = 0
        nb = 0
        x = np.zeros((2,1000))
        while i < len(lines)-14:
            if pattern_particle.findall(lines[i]):
                #print("first occurence")
                if pattern_particle.findall(lines[i+14]):
                    #print("second occurence")
                    x[0][nb]=float(pattern.findall(lines[i+2])[0])
                    x[1][nb]=float(pattern.findall(lines[i+16])[0])
                    nb += 1
                elif i<len(lines)-27 and pattern_particle.findall(lines[i+27]):
                    x[0][nb]=float(pattern.findall(lines[i+2])[0])
                    x[1][nb]=float(pattern.findall(lines[i+29])[0])
                    nb += 1
                elif i<len(lines)-40 and pattern_particle.findall(lines[i+40]):
                    x[0][nb]=float(pattern.findall(lines[i+2])[0])
                    x[1][nb]=float(pattern.findall(lines[i+42])[0])
                    nb += 1
                i += 1
            i += 1
        if nb == 0:
            print("error, no particle detected to compute their relative position.")


        result = (np.sum(x[1]) - np.sum(x[0])) / nb
        print(nb)


        xf = x.flatten()
        filt = xf[xf != 0]
        xnew = filt.reshape(2,-1)
        print(len(xnew[0]))

        if len(xnew[0])!=nb:
           print(x,xnew)
        s=np.sqrt(np.sum((xnew[1]-xnew[0]-result)**2)/nb)

    with open(output,'a') as file_ow:
        file_ow.writelines(str(magnetic_field) + ' ' + str(result)+ ' '+ str(s) + '\n' )
    print(result)
    if result:
        write('allpix_conf/detector.conf',10,f'position = {result-10}mm 0cm 41cm')
    return 0

def main():

    for particle in ['pi+','kaon+','mu+']:
        write('allpix_conf/detector.conf',10,f'position = 0mm 0cm 41cm')


        for i in np.arange(0.2,6.2,0.2):
            write('allpix_conf/simple_detector.conf',12,f'magnetic_field = 0T {i}T 0T')
            write('allpix_conf/simple_detector.conf',16,f'particle_type = "{particle}"')
            sub.run('allpix -c allpix_conf/simple_detector.conf',shell=True)
            magnetic(particle, i)

def write(nom_fichier, numero_ligne, contenu):
    with open(nom_fichier, 'r') as f:
        lignes = f.readlines()

    if 0 < numero_ligne <= len(lignes):
        lignes[numero_ligne-1] = contenu + '\n'
    else:
        print("Invalid line number.")

    with open(nom_fichier, 'w') as f:
        f.writelines(lignes)

main()
