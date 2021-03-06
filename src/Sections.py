#   Author: Jagadishwar R. Sirigiri
#   Bridge12 Technologies, Inc.
#   37 Loring Drive, Framingham, MA 01702
#   Date Created: September 25, 2019
#   Classes defining different types of geometry for CORRUG

import math
import numpy as np

class SmoothSection():
    # This class creates a profiled smooth section for Corrug program
    def __init__(self, name="SmoothSection",sd=1,ed=2,length=10,numsegments=100,nummodes=5,shape='Linear',z=[],r=[],rn=[]):
        self.name = name
        self.sd = sd
        self.ed = ed
        self.length = length
        self.numsegments = numsegments
        self.nummodes = nummodes
        self.shape = shape
        self.z = z
        self.r = r
        self.rn =rn
        
    def points(self):
        # calculates the end points
        dz = (self.length/self.numsegments)
        self.z = [float(dz)]*(self.numsegments)
        self.n = np.full((self.numsegments,1),self.nummodes)
        mu = self.length/2
        s = self.length/2
        for i in range(0,int(self.numsegments)):
            if (self.shape == 'Linear'):
                rad = self.sd/2 + i*(self.ed/2-self.sd/2)/(self.numsegments-1)
            elif (self.shape == 'Sine Squared'):
                rad = self.sd/2 + (self.ed/2-self.sd/2)*math.sin(i*0.5*math.pi/(self.numsegments-1))
            elif (self.shape == 'Raised Cosine'):
                rad = self.sd/2 + (self.ed/2-self.sd/2)*0.5*(1+(i*(self.length/(self.numsegments-1))-mu)/s+ (1/math.pi)*math.sin(((i*self.length/(self.numsegments-1))-mu)*math.pi/s))
            self.r.append(str(rad))
            self.rn.append(str(rad) + ' ' + str(self.nummodes))
        return


class CorrugatedSection():
    # This class creates a profiled smooth section for Corrug program
    def __init__(self, name="SmoothSection",sd=1,ed=2,scd=0.1,ecd=0.2,csw=0.5,ctw=0.1,length=10,numsegments=1,nummodes=5,shape='Linear',z=[],r=[],rn=[]):
        self.name = name
        self.sd = sd
        self.ed = ed
        self.scd = scd
        self.ecd = ecd
        self.csw = csw
        self.ctw = ctw
        self.length = length
        self.numsegments = numsegments
        self.nummodes = nummodes
        self.shape = shape
        self.z = z
        self.r = r
        self.rn = rn
        
    def points(self):
        self.numsegments = int(self.length/(self.csw + self.ctw))
        self.length = self.numsegments*(self.csw+self.ctw)
        self.n = np.full((self.numsegments,1),self.nummodes)
        for i in range(0,self.numsegments):
            self.z.append(self.csw)
            self.z.append(self.ctw)
        
        mu = self.length/2
        s = self.length/2
        for i in range(0,int(self.numsegments)):
            if (self.shape == 'Linear'):
                rad = self.sd/2 + i*(self.ed/2-self.sd/2)/(self.numsegments-1)
            elif (self.shape == 'Sine Squared'):
                rad = self.sd/2 + (self.ed/2-self.sd/2)*math.sin(i*0.5*math.pi/(self.numsegments-1))
            elif (self.shape == 'Raised Cosine'):
                rad = self.sd/2 + (self.ed/2-self.sd/2)*0.5*(1+(i*(self.length/(self.numsegments-1))-mu)/s+ (1/math.pi)*math.sin(((i*self.length/(self.numsegments-1))-mu)*math.pi/s))
            self.r.append(str(rad + self.scd +i*(self.ecd-self.scd)/self.numsegments))
            self.rn.append(str(rad + self.scd +i*(self.ecd-self.scd)/self.numsegments)+' '+str(self.nummodes))
            self.r.append(str(rad))
            self.rn.append(str(rad) + ' ' + str(self.nummodes))
        self.numsegments = 2*self.numsegments
        return