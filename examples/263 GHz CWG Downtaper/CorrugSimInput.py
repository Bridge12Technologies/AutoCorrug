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
    results_path = '//10.12.70.26/B12TProjArchive/Projects/0133-COLU/TransmissionLine/CWGDowntaper/IV'
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

    var_range['CWGDowntaper Profile'] = ['Sine Squared','Linear','Raised Cosine'] # 'Linear', 'Sine Squared', 'Raised Cosine']
    var_range['CWGDowntaper Length'] = [300]
    var_range['CWGDowntaper End Dia'] = [8.0]
    var_range['CWGDowntaper Corrug Depth'] = [0.29]
    var_range['CWGDowntaper Corrug Slot Width'] = [0.15]
    var_range['CWGDowntaper Corrug Tooth Width'] = [0.15]

    var_range['OutputCWGSection Profile'] = ['Linear'] # 'Linear', 'Sine Squared', 'Raised Cosine']
    var_range['OutputCWGSection Length'] = [20,30,40]
    var_range['OutputCWGSection Corrug Depth'] = [0.29]
    var_range['OutputCWGSection Corrug Slot Width'] = [0.15]
    var_range['OutputCWGSection Corrug Tooth Width'] = [0.15]

    var_list = [['OutputCWGSection Length','CWGDowntaper Profile','Frequency']]

    return nodes, results_path, var_list, var_range

def define_geometry(var_register,step_directory):

    geometry = []

    # adding a small smooth section of 1 mm at the start of the simulation to avoid launching the mode at a discontinuity. 
    # needs further investigation to determine if it is necessary. Using this at the moment to avoid an issue with the geometry.out file exclusively used for plotting
    nummodes = int(var_register['Number of Modes at Input Crosssection'][0])
    geometry.append(SmoothSection(name='InputSec',sd=var_register['InputCWGSection Dia'][0],ed=var_register['InputCWGSection Dia'][0], 
    length=1,numsegments=5,nummodes=nummodes,shape='Linear',z=[],r=[],rn=[]))
       
    nummodes = int(var_register['Number of Modes at Input Crosssection'][0])
    geometry.append(CorrugatedSection(name='InputCWGSection',sd=var_register['InputCWGSection Dia'][0],ed=var_register['InputCWGSection Dia'][0],
    scd=var_register['InputCWGSection Corrug Depth'][0],ecd=var_register['InputCWGSection Corrug Depth'][0],
    csw=var_register['InputCWGSection Slot Width'][0],ctw=var_register['InputCWGSection Tooth Width'][0],  
    length=var_register['InputCWGSection Length'][0],numsegments=1,nummodes=nummodes,shape=var_register['InputCWGSection Profile'][0],z=[],r=[],rn=[]))
    
    nummodes = int(var_register['Number of Modes at Input Crosssection'][0])
    geometry.append(CorrugatedSection(name='CWGDowntaper',sd=var_register['InputCWGSection Dia'][0],ed=var_register['CWGDowntaper End Dia'][0], 
    scd=var_register['InputCWGSection Corrug Depth'][0],ecd=var_register['CWGDowntaper Corrug Depth'][0],
    csw=var_register['CWGDowntaper Corrug Slot Width'][0],ctw=var_register['CWGDowntaper Corrug Tooth Width'][0],  
    length=var_register['CWGDowntaper Length'][0],numsegments=1,nummodes=nummodes,shape=var_register['CWGDowntaper Profile'][0],z=[],r=[],rn=[]))

    nummodes = int(var_register['Number of Modes at Input Crosssection'][0]*var_register['CWGDowntaper End Dia'][0]/var_register['InputCWGSection Dia'][0])
    geometry.append(CorrugatedSection(name='OutputCWGSection',sd=var_register['CWGDowntaper End Dia'][0],ed=var_register['CWGDowntaper End Dia'][0],
    scd=var_register['OutputCWGSection Corrug Depth'][0],ecd=var_register['OutputCWGSection Corrug Depth'][0],
    csw=var_register['OutputCWGSection Corrug Slot Width'][0],ctw=var_register['OutputCWGSection Corrug Tooth Width'][0],  
    length=var_register['OutputCWGSection Length'][0],numsegments=1,nummodes=nummodes,shape=var_register['OutputCWGSection Profile'][0],z=[],r=[],rn=[]))

    return geometry
