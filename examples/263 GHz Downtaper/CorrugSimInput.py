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
    nodes = ['10.12.70.71','10.12.70.76','10.12.70.77','10.12.70.79']
    # nodes on which the simulation is run
    results_path = '//10.12.70.26/B12TProjArchive/Projects/0133-COLU/TransmissionLine/CWGDowntaper'
    var_range = {}

    var_range['version_num'] = ['CWGDowntaper']    # version number
    var_range['Frequency'] = [258,259,260,261,262,263]
    var_range['Input Modes'] = ['HE11'] # TE11, HE11
    var_range['Number of Modes at Input Crosssection'] = [20]
    var_range['NTheta'] = [10]
    var_range['DTheta'] = [10]

    var_range['InputCWGSection Profile'] = ['Linear'] # 'Linear', 'Sine Squared', 'Raised Cosine']
    var_range['InputCWGSection Length'] = [20]
    var_range['InputCWGSection Dia'] = [19.05]
    var_range['InputCWGSection Corrug Depth'] = [0.29]
    var_range['InputCWGSection Slot Width'] = [0.15]
    var_range['InputCWGSection Tooth Width'] = [0.15]

    var_range['SmoothDowntaper Profile'] = ['Linear', 'Sine Squared', 'Raised Cosine']
    var_range['SmoothDowntaper Length'] = [100]
    var_range['SmoothDowntaper Segments'] = [1000]
    var_range['SmoothDowntaper End Dia'] = [8.0]

    # var_range['CWGDowntaper Profile'] = ['Sine Squared', 'Linear', 'Raised Cosine'] # 'Linear', 'Sine Squared', 'Raised Cosine']
    # var_range['CWGDowntaper Length'] = [300]
    # var_range['CWGDowntaper End Dia'] = [8.0]
    # var_range['CWGDowntaper Corrug Depth'] = [0.29]
    # var_range['CWGDowntaper Corrug Slot Width'] = [0.15]
    # var_range['CWGDowntaper Corrug Tooth Width'] = [0.15]

    var_range['OutputCWGSection Profile'] = ['Linear'] # 'Linear', 'Sine Squared', 'Raised Cosine']
    var_range['OutputCWGSection Length'] = [20,30,40]
    var_range['OutputCWGSection Corrug Depth'] = [0.29]
    var_range['OutputCWGSection Corrug Slot Width'] = [0.15]
    var_range['OutputCWGSection Corrug Tooth Width'] = [0.15]

    var_list = [['OutputCWGSection Length', 'SmoothDowntaper Profile', 'Frequency']]

    return nodes, results_path, var_list, var_range

def define_geometry(var_register,step_directory):

    geometry = []
    
    # nummodes = var_register['Number of Modes at Input Crosssection'][0] 
    # geometry = [SmoothSection(name='Smooth Section',sd=var_register['TE11 Uptaper Start Dia'][0],ed=var_register['TE11 Uptaper End Dia'][0], 
    # length=var_register['TE11 Uptaper Length'][0],numsegments=var_register['TE11 Uptaper Segments'][0],nummodes=nummodes,shape=var_register['TE11 Uptaper Profile'][0],z=[],r=[],rn=[])]
    
    nummodes = int(var_register['Number of Modes at Input Crosssection'][0])
    geometry.append(CorrugatedSection(name='InputCWGSection',sd=var_register['InputCWGSection Dia'][0],ed=var_register['InputCWGSection Dia'][0],
    scd=var_register['InputCWGSection Corrug Depth'][0],ecd=var_register['InputCWGSection Corrug Depth'][0],
    csw=var_register['InputCWGSection Slot Width'][0],ctw=var_register['InputCWGSection Tooth Width'][0],  
    length=var_register['InputCWGSection Length'][0],numsegments=1,nummodes=nummodes,shape=var_register['InputCWGSection Profile'][0],z=[],r=[],rn=[]))
    
    # nummodes = int(var_register['Number of Modes at Input Crosssection'][0])
    # geometry.append(CorrugatedSection(name='SmoothDowntaper',sd=var_register['InputCWGSection Dia'][0],ed=var_register['CWGDowntaper End Dia'][0], 
    # scd=var_register['InputCWGSection Corrug Depth'][0],ecd=var_register['CWGDowntaper Corrug Depth'][0],
    # csw=var_register['CWGDowntaper Corrug Slot Width'][0],ctw=var_register['CWGDowntaper Corrug Tooth Width'][0],  
    # length=var_register['CWGDowntaper Length'][0],numsegments=1,nummodes=nummodes,shape=var_register['CWGDowntaper Profile'][0],z=[],r=[],rn=[]))

    nummodes = var_register['Number of Modes at Input Crosssection'][0] 
    geometry = [SmoothSection(name='Smooth Section',sd=var_register['InputCWGSection Dia'][0],ed=var_register['SmoothDowntaper End Dia'][0], 
    length=var_register['SmoothDowntaper Length'][0],numsegments=var_register['SmoothDowntaper Segments'][0],nummodes=nummodes,shape=var_register['SmoothDowntaper Profile'][0],z=[],r=[],rn=[])]

    nummodes = int(var_register['Number of Modes at Input Crosssection'][0]*var_register['SmoothDowntaper End Dia'][0]/var_register['InputCWGSection Dia'][0])
    geometry.append(CorrugatedSection(name='OutputCWGSection',sd=var_register['SmoothDowntaper End Dia'][0],ed=var_register['SmoothDowntaper End Dia'][0],
    scd=var_register['OutputCWGSection Corrug Depth'][0],ecd=var_register['OutputCWGSection Corrug Depth'][0],
    csw=var_register['OutputCWGSection Corrug Slot Width'][0],ctw=var_register['OutputCWGSection Corrug Tooth Width'][0],  
    length=var_register['OutputCWGSection Length'][0],numsegments=1,nummodes=nummodes,shape=var_register['OutputCWGSection Profile'][0],z=[],r=[],rn=[]))


    return geometry

    # NumSegments = 0
    # for section in geometry:
    #     section.points()
    #     NumSegments = NumSegments + section.numsegments

    # with open(step_directory+'\\'+'input.i', 'w') as inputfile:
    #     with open(step_directory+'\\'+'geometry.out', 'w') as geometryfile:
    #         inputfile.write(str(var_register['Frequency'][0]) + ' ' + str(1)+ ' '+ str(NumSegments))
    #         inputfile.write('\n')

    #         for section in geometry:
    #             savetxt(inputfile,section.z)
            
    #         for section in geometry:
    #             savetxt(inputfile,(section.rn), fmt="%s")

    #         # specify input mode mixture
    #         if (var_register['Input Modes'][0] == 'TE11'):
    #             inputfile.write(str(1))
    #             inputfile.write('\n')
    #             inputfile.write(str(1) + '  ' + str(0))
    #             inputfile.write('\n')
    #         elif (var_register['Input Modes'][0] == 'HE11'):
    #             inputfile.write(str(4))
    #             inputfile.write('\n')
    #             inputfile.write(str(0.91978) + '  ' + str(0)) #TE11
    #             inputfile.write('\n')
    #             inputfile.write(str(0.38079) + '  ' + str(180)) #TM11
    #             inputfile.write('\n')
    #             inputfile.write(str(0.031623) + '  ' + str(0)) #TE12
    #             inputfile.write('\n')
    #             inputfile.write(str(0.07746) + '  ' + str(180)) #TM12
    #             inputfile.write('\n')

    #         zold = 0
    #         seccount = 1
    #         for section in geometry:
    #             if seccount == 1:
    #                 j = 0
    #                 for k in section.z:
    #                     geometryfile.write(str(zold)+','+str(section.r[j])+'\n')
    #                     zold = k + zold
    #                     j = j + 1
    #                 seccount = seccount + 1
    #             else:
    #                 j = 0
    #                 for k in section.z:
    #                     geometryfile.write(str(zold)+','+str(section.r[j])+'\n')
    #                     geometryfile.write(str(k+zold)+','+str(section.r[j])+'\n')
    #                     zold = k + zold
    #                     j = j + 1
    #                 seccount = seccount + 1

    # # write a list file with runtime input for corrug.exe
    # with open(step_directory+'\\'+'commands.in', 'w') as inputfile:
    #     inputfile.write('input.i')
    #     inputfile.write('\n')  
    #     inputfile.write('output.o')
    #     inputfile.write('\n')  
    #     inputfile.write('pattern.pat')
    #     inputfile.write('\n')  
    #     inputfile.write(str(var_register['NTheta'][0]))
    #     inputfile.write('\n')  
    #     inputfile.write(str(var_register['DTheta'][0]))
    #     inputfile.write('\n')  
    #     inputfile.write('Y')
    #     inputfile.close()

    # return