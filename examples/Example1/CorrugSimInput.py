#   Author: Jagadishwar R. Sirigiri
#   Bridge12 Technologies, Inc.
#   37 Loring Drive, Framingham, MA 01702
#   Date Created: September 25, 2019
#   Define run and geometry parameters for CORRUG

import sys
sys.path.insert(0, '..\\src')
import numpy as np
from numpy import linspace
from Sections import *


def simulation_parameters():
    # nodes = ['10.12.70.12', '10.12.70.64']
    nodes = ['10.12.50.5']
    # nodes on which the simulation is run
    # results_path = '//10.12.70.26/Shared Data/Projects/FFP-PANS-0099/HE11-Launcher/v1'
    results_path = 'D:/Bridge12/Projects/MyCorrugDesign/results'
    var_range = {}

    var_range['version_num'] = ['HE11Conv']    # version number
    var_range['Frequency'] = [95,90,92,93,94,96,98,100]
    var_range['Input Modes'] = ['TE11'] # TE11, HE11
    var_range['Number of Modes at Input Crosssection'] = [10,20]
    var_range['NTheta'] = [10]
    var_range['DTheta'] = [10]

    var_range['TE11 Uptaper Profile'] = ['Linear','Sine Squared', 'Raised Cosine'] # 'Linear', 'Sine Squared', 'Raised Cosine']
    var_range['TE11 Uptaper Start Dia'] = [2*1.9]
    var_range['TE11 Uptaper Length'] = [10]
    var_range['TE11 Uptaper Segments'] = [50]
    var_range['TE11 Uptaper End Dia'] = [2*3.3]

    var_range['TE11-HE11 Conv Start Corrug Depth'] = [1.6]
    var_range['TE11-HE11 Conv Profile'] = ['Linear', 'Sine Squared', 'Raised Cosine']  # 'Linear', 'Sine Squared', 'Raised Cosine']
    var_range['TE11-HE11 Conv Length'] = [15, 40, 50, 80]
    var_range['TE11-HE11 Conv End Dia'] = [2*6.35]
    var_range['TE11-HE11 Conv End Corrug Depth'] = [0.37]
    var_range['TE11-HE11 Conv Corrug Slot Width'] = [0.5]
    var_range['TE11-HE11 Conv Corrug Tooth Width'] = [0.12]

    var_range['CWG Uptaper Profile'] = ['Linear', 'Raised Cosine'] # 'Linear', 'Sine Squared', 'Raised Cosine']
    var_range['CWG Uptaper Length'] = [6.2]
    var_range['CWG Uptaper End Dia'] = [2*6.35]
    var_range['CWG Uptaper End Corrug Depth'] = [0.37]
    var_range['CWG Uptaper Corrug Slot Width'] = [0.5]
    var_range['CWG Uptaper Corrug Tooth Width'] = [0.12]

    var_range['CWG Straight Section Profile'] = ['Linear'] # 'Linear', 'Sine Squared', 'Raised Cosine']
    var_range['CWG Straight Section Length'] = [10,20,40,60,80,100]
    var_range['CWG Straight Section End Dia'] = [2*6.35]
    var_range['CWG Straight Section End Corrug Depth'] = [0.37]
    var_range['CWG Straight Section Corrug Slot Width'] = [0.5]
    var_range['CWG Straight Section Corrug Tooth Width'] = [0.12]

    var_list = [['CWG Straight Section Length', 'TE11-HE11 Conv Profile', 'Frequency'],['TE11-HE11 Conv Length', 'TE11-HE11 Conv Profile', 'Frequency']]

    return nodes, results_path, var_list, var_range

def define_geometry(var_register,step_directory):

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

    return geometry