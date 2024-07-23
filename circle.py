import matplotlib.pyplot as plt
import numpy as np
from scipy import constants as cst
import subprocess as sub
import re

#Program that computes the global position of particles in a constant magnetic field B based on a circle
B=1

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

#Function that computes a circle based on three coordinates (0,0,0) and two points at 10cm and 20cm in x. 
def circle():
    x1, y1 = 0, 0
    #puts two detectors, one at 10cm and the other at 20cm
    write('allpix_conf/detector.conf',10,f'position = 0mm 0cm 20cm')
    write('allpix_conf/simple_detector.conf',4,f'number_of_events = 1')
    write('allpix_conf/detector.conf',3,f'position = 0mm 0cm 10cm')
    sub.run('allpix -c allpix_conf/simple_detector.conf',shell=True)

    #get the global coordinates of the particle in the two detector.
    with open('output/data.txt','r') as file:
        lines = file.readlines()
        pattern = re.compile(f"[-]*\d+\.\d+")
        l2 = pattern.findall(lines[8])
        x2 = float(l2[0])
        y2 = float(l2[2])
        l3 = pattern.findall(lines[22])
        x3 = float(l3[0])
        y3 = float(l3[2])

    #computes the center of the circle
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

#Theorical circle
def theory(E,m):
    E*=1.60218*10**(-13)
    m*=1.78266*10**(-30)
    c=(np.sqrt((E+m*cst.c**2)**2-m**2*cst.c**4))/(cst.e*B*cst.c)
    print(c)
    omega=(B*cst.e)/(E+m)
    t=np.linspace(0,2*np.pi/omega,1000)
    x=np.zeros(1000)
    y=np.zeros(1000)
    x=-c*(1-np.cos(omega*t))
    y=-c*np.sin(omega*t)
    return x, y

#draws the experimental circle
def draw_circle():
    write('allpix_conf/simple_detector.conf',4,f'number_of_events = 1')
    fix, ax = plt.subplots()
    write('allpix_conf/simple_detector.conf',16,f'particle_type = "pi+"')
    xc,yc,Rc = circle()
    xc/=1000
    yc/=1000
    Rc/=1000
    circle1 = plt.Circle((xc,yc),Rc,edgecolor = 'blue',facecolor = 'none')


    #write('allpix_conf/simple_detector.conf',16,f'particle_type = "mu+"')
    #xc,yc,Rc = circle()
    #circle2 = plt.Circle((xc,yc),Rc,edgecolor = 'black',facecolor = 'none')
    ax.add_patch(circle1)
    #ax.add_patch(circle2)

    ax.plot(x_th, y_th , linestyle='-', color='r')

    ax.set_aspect('equal','box')
    plt.show()



x_th,y_th=theory(700,139)
draw_circle()
