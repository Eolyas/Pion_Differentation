import numpy as np
from scipy import constants as cst
import re
import subprocess as sub
import os

#Program that computes the deviation

#Erasing old files to avoid conflicts
if os.path.exists('pi+.txt'):
    os.remove('pi+.txt')
if os.path.exists('kaon+.txt'):
    os.remove('kaon+.txt')
if os.path.exists('mu+.txt'):
    os.remove('mu+.txt')

#Function that computes a circle based on three coordinates (0,0,0) and two points at 10cm and 20cm in x. 
#That circle is then used to calculate the approximate position of the particle up to 2 meters.
def circle():
    x1, y1 = 0, 0
    write('allpix_conf/detector.conf',10,f'position = 0mm 0cm 20cm')
    write('allpix_conf/simple_detector.conf',4,f'number_of_events = 1')
    write('allpix_conf/detector.conf',3,f'position = 0mm 0cm 10cm')
    sub.run('allpix -c allpix_conf/simple_detector.conf',shell=True)

    with open('output/data.txt','r') as file:
        lines = file.readlines()
        pattern = re.compile(f"[-]*\d+\.\d+")
        l2 = pattern.findall(lines[8])
        x2 = float(l2[0])
        y2 = float(l2[2])
        l3 = pattern.findall(lines[22])
        x3 = float(l3[0])
        y3 = float(l3[2])

    A = np.array([[x2 - x1, y2 - y1], [x3 - x2, y3 - y2]])
    B = np.array([[(x2**2 - x1**2 + y2**2 - y1**2) / 2], [(x3**2 - x2**2 + y3**2 - y2**2) / 2]])
    if np.linalg.det(A) != 0:  # Ensure the matrix is not singular
        center = np.linalg.solve(A, B)
        xc, yc = center.flatten()
    else:
        raise ValueError("The points are collinear, which makes a unique circle undefined.")

    # Calculate radius Rc
    Rc = np.sqrt((x1 - xc)**2 + (y1 - yc)**2)
    
    print(f"Center: ({xc}, {yc})")
    print(f"Radius: {Rc}")

    write('allpix_conf/detector.conf',3,f'position = 0mm 0cm 1cm')
    write('allpix_conf/simple_detector.conf',4,f'number_of_events = 1000')
    print(yc)
    return xc, yc, Rc

#Calculates the position of a particle based on the experimental circle and x coordinate
def position(xc, yc, Rc, y):
    #y = float(input("Position en Y ? "))
    if (Rc**2 - (y - yc)**2) >= 0:  # Check if the y-coordinate is within the circle's bounds
        x = xc + np.sqrt(Rc**2 - (y - yc)**2)
    else:
        print("The given z-coordinate is outside the circle's bounds.")
    return x

#Look for and output the global position of each particle on each detector
def magnetic(particle_name, Variable):
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
        pattern_test = re.compile(f"=== \d+ ===")
        nb = 0
        x = np.zeros((2,1000))
        
        #Search for the global coordinates
        while i < len(lines)-14:
            if pattern_particle.findall(lines[i]):
                if pattern_particle.findall(lines[i+14]):
                    x[0][nb]=float(pattern.findall(lines[i+2])[0])
                    x[1][nb]=float(pattern.findall(lines[i+16])[0])
                    nb += 1
                #Test if one electron snuck between the two particles
                elif i<len(lines)-27 and pattern_particle.findall(lines[i+27]):
                    x[0][nb]=float(pattern.findall(lines[i+2])[0])
                    x[1][nb]=float(pattern.findall(lines[i+29])[0])

                    nb += 1
                #Test if two electrons snuck between the two particles
                elif i<len(lines)-40 and pattern_particle.findall(lines[i+40]):
                    x[0][nb]=float(pattern.findall(lines[i+2])[0])
                    x[1][nb]=float(pattern.findall(lines[i+42])[0])

                    nb += 1
                i += 14
            i += 1
        if nb == 0:
            print("error, no particle detected to compute their relative position.")

        #Subtract the position of the first detector
        result = (np.sum(x[1]) - np.sum(x[0])) / nb
        print(nb)

        #removes 0s from the list
        xf = x.flatten()
        filt = xf[xf != 0]
        xnew = filt.reshape(2,-1)
        print(len(xnew[0]))

        #standard deviation
        if len(xnew[0])!=nb:
           print(x,xnew)
        s=np.sqrt(np.sum((xnew[1]-xnew[0]-result)**2)/nb)

    #output the result in a readable file
    with open(output,'a') as file_ow:
        file_ow.writelines(str(Variable) + ' ' + str(result)+ ' '+ str(s) + '\n' )
    print(result)
    return 0

#Loop on each particle and each variable
def main():
    for particle in ['pi+','mu+']:
        write('allpix_conf/simple_detector.conf',16,f'particle_type = "{particle}"')
        #write('allpix_conf/simple_detector.conf',12,f'magnetic_field = 0T 1T 0T')
        xc,yc,Rc = circle()
        for i in np.arange(11,211,10):
            x = position(xc,yc,Rc,i*10)
            write('allpix_conf/detector.conf',10,f'position = {x}mm 0cm {i}cm')
            sub.run('allpix -c allpix_conf/simple_detector.conf',shell=True)
            magnetic(particle, i)

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

main()
