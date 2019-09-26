#   Author: Jagadishwar R. Sirigiri
#   Bridge12 Technologies, Inc.
#   37 Loring Drive, Framingham, MA 01702
#   Date Created: September 25, 2019
#   Define run and geometry parameters for CORRUG

import sys
sys.path.insert(0, '..\\src')
import numpy as np
from numpy import linspace
from numpy import savetxt
from Sections import *


def simulation_parameters():
    nodes = ['10.12.70.12', '10.12.70.64']
    # nodes on which the simulation is run
    results_path = '//10.12.70.26/Shared Data/Projects/FFP-PANS-0099/HE11-Launcher/v1'
    var_range = {}

    var_range['version_num'] = ['A0068-PT2003']    # version number
    var_range['Frequency'] = [95,90,92,93,94,96,98,100]
    var_range['Input Modes'] = ['TE11'] # TE11, HE11
    var_range['Number of Modes at Input Crosssection'] = [5]
    var_range['NTheta'] = [10]
    var_range['DTheta'] = [10]

    var_range['TE11 Uptaper Profile'] = ['Sine Squared'] # 'Linear', 'Sine Squared', 'Raised Cosine']
    var_range['TE11 Uptaper Start Dia'] = [3.7]
    var_range['TE11 Uptaper Length'] = [10]
    var_range['TE11 Uptaper Segments'] = [200]
    var_range['TE11 Uptaper End Dia'] = [6.0]

    var_range['TE11-HE11 Conv Start Corrug Depth'] = [1.579]
    var_range['TE11-HE11 Conv Profile'] = ['Sine Squared' , 'Linear', 'Raised Cosine']  # 'Linear', 'Sine Squared', 'Raised Cosine']
    var_range['TE11-HE11 Conv Length'] = [20, 25, 30, 35]
    var_range['TE11-HE11 Conv End Dia'] = [2*8]
    var_range['TE11-HE11 Conv End Corrug Depth'] = [0.6858]
    var_range['TE11-HE11 Conv Corrug Slot Width'] = [0.6604]
    var_range['TE11-HE11 Conv Corrug Tooth Width'] = [0.1016]

    var_range['CWG Uptaper Profile'] = ['Sine Squared', 'Linear', 'Raised Cosine'] # 'Linear', 'Sine Squared', 'Raised Cosine']
    var_range['CWG Uptaper Length'] = [80]
    var_range['CWG Uptaper End Dia'] = [31.75]
    var_range['CWG Uptaper End Corrug Depth'] = [0.6858]
    var_range['CWG Uptaper Corrug Slot Width'] = [0.6604]
    var_range['CWG Uptaper Corrug Tooth Width'] = [0.1016]

    var_range['CWG Straight Section Profile'] = ['Linear'] # 'Linear', 'Sine Squared', 'Raised Cosine']
    var_range['CWG Straight Section Length'] = [50,60,70,80]
    var_range['CWG Straight Section End Dia'] = [31.75]
    var_range['CWG Straight Section End Corrug Depth'] = [0.6858]
    var_range['CWG Straight Section Corrug Slot Width'] = [0.6604]
    var_range['CWG Straight Section Corrug Tooth Width'] = [0.1016]

    var_list = [['CWG Straight Section Length', 'TE11-HE11 Conv Profile', 'Frequency']]

    return nodes, results_path, var_list, var_range

def create_corrug_input_file(var_register,step_directory):

    geometry = []
    
    nummodes = var_register['Number of Modes at Input Crosssection'][0] 
    geometry = [SmoothSection(name='Smooth Section',sd=var_register['TE11 Uptaper Start Dia'][0],ed=var_register['TE11 Uptaper End Dia'][0], 
    length=var_register['TE11 Uptaper Length'][0],numsegments=var_register['TE11 Uptaper Segments'][0],nummodes=nummodes,shape=var_register['TE11 Uptaper Profile'][0],z=[],r=[],rn=[])]
    
    nummodes = int(var_register['Number of Modes at Input Crosssection'][0]*var_register['TE11 Uptaper End Dia'][0]/var_register['TE11 Uptaper Start Dia'][0])
    geometry.append(CorrugatedSection(name='TE11 - HE11 Converter',sd=var_register['TE11 Uptaper End Dia'][0],ed=var_register['TE11-HE11 Conv End Dia'][0],
    scd=var_register['TE11-HE11 Conv Start Corrug Depth'][0],ecd=var_register['TE11-HE11 Conv End Corrug Depth'][0],
    csw=var_register['TE11-HE11 Conv Corrug Slot Width'][0],ctw=var_register['TE11-HE11 Conv Corrug Tooth Width'][0],  
    length=var_register['TE11-HE11 Conv Length'][0],numsegments=1,nummodes=nummodes,shape=var_register['TE11-HE11 Conv Profile'][0],z=[],r=[],rn=[]))
    
    nummodes = int(var_register['Number of Modes at Input Crosssection'][0]*var_register['TE11-HE11 Conv End Dia'][0]/var_register['TE11 Uptaper Start Dia'][0])
    geometry.append(CorrugatedSection(name='CWG Uptaper',sd=var_register['TE11-HE11 Conv End Dia'][0],ed=var_register['CWG Uptaper End Dia'][0], 
    scd=var_register['TE11-HE11 Conv End Corrug Depth'][0],ecd=var_register['CWG Straight Section End Corrug Depth'][0],
    csw=var_register['CWG Uptaper Corrug Slot Width'][0],ctw=var_register['CWG Uptaper Corrug Tooth Width'][0],  
    length=var_register['CWG Uptaper Length'][0],numsegments=1,nummodes=nummodes,shape=var_register['CWG Uptaper Profile'][0],z=[],r=[],rn=[]))

    nummodes = int(var_register['Number of Modes at Input Crosssection'][0]*var_register['CWG Uptaper End Dia'][0]/var_register['TE11 Uptaper Start Dia'][0])
    geometry.append(CorrugatedSection(name='CWG Straight Section',sd=var_register['CWG Uptaper End Dia'][0],ed=var_register['CWG Uptaper End Dia'][0],
    scd=var_register['CWG Uptaper End Corrug Depth'][0],ecd=var_register['CWG Straight Section End Corrug Depth'][0],
    csw=var_register['CWG Straight Section Corrug Slot Width'][0],ctw=var_register['CWG Straight Section Corrug Tooth Width'][0],  
    length=var_register['CWG Straight Section Length'][0],numsegments=1,nummodes=nummodes,shape=var_register['CWG Straight Section Profile'][0],z=[],r=[],rn=[]))

    NumSegments = 0
    for section in geometry:
        section.points()
        NumSegments = NumSegments + section.numsegments

    with open(step_directory+'\\'+'input.i', 'w') as inputfile:
        with open(step_directory+'\\'+'geometry.out', 'w') as geometryfile:
            inputfile.write(str(var_register['Frequency'][0]) + ' ' + str(1)+ ' '+ str(NumSegments))
            inputfile.write('\n')

            for section in geometry:
                savetxt(inputfile,section.z)
            
            for section in geometry:
                savetxt(inputfile,(section.rn), fmt="%s")

            # specify input mode mixture
            if (var_register['Input Modes'][0] == 'TE11'):
                inputfile.write(str(1))
                inputfile.write('\n')
                inputfile.write(str(1) + '  ' + str(0))
                inputfile.write('\n')
            elif (var_register['Input Modes'][0] == 'HE11'):
                inputfile.write(str(4))
                inputfile.write('\n')
                inputfile.write(str(0.91978) + '  ' + str(0)) #TE11
                inputfile.write('\n')
                inputfile.write(str(0.38079) + '  ' + str(180)) #TM11
                inputfile.write('\n')
                inputfile.write(str(0.031623) + '  ' + str(0)) #TE12
                inputfile.write('\n')
                inputfile.write(str(0.07746) + '  ' + str(180)) #TM12
                inputfile.write('\n')

            zold = 0
            seccount = 1
            for section in geometry:
                if seccount == 1:
                    j = 0
                    for k in section.z:
                        geometryfile.write(str(zold)+','+str(section.r[j])+'\n')
                        zold = k + zold
                        j = j + 1
                    seccount = seccount + 1
                else:
                    j = 0
                    for k in section.z:
                        geometryfile.write(str(zold)+','+str(section.r[j])+'\n')
                        geometryfile.write(str(k+zold)+','+str(section.r[j])+'\n')
                        zold = k + zold
                        j = j + 1
                    seccount = seccount + 1

    # write a list file with runtime input for corrug.exe
    with open(step_directory+'\\'+'commands.in', 'w') as inputfile:
        inputfile.write('input.i')
        inputfile.write('\n')  
        inputfile.write('output.o')
        inputfile.write('\n')  
        inputfile.write('pattern.pat')
        inputfile.write('\n')  
        inputfile.write(str(var_register['NTheta'][0]))
        inputfile.write('\n')  
        inputfile.write(str(var_register['DTheta'][0]))
        inputfile.write('\n')  
        inputfile.write('Y')
        inputfile.close()

    return