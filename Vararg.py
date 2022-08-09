import numpy as np
class Varargin(object):
    def __init__(self,data,regressorinds,channelinds):
        self.data=data
        self.regressorinds=regressorinds
        #regressorinds=input('enter the regressorinds')
        self.channelinds=channelinds
        #channelinds=input('enter the channelinds')

        #srate=input('enter the sampling rate')
        self.srate=250
        #if srate!= 0: self.srate= float(srate)

        #windowduration=input('enter the windowduration')
        self.windowduration=2.000000
        #4.0
        #if windowduration!= 0: self.windowduration = float(windowduration)

        #delay=input('enter the delay')
        self.delay=0.05000
        #0.021
        #if delay!= 0: self.delay = float(delay)

        self.taperingfactor=1
        #taperingfactor=input('enter the taperingfactor')
        #if taperingfactor!= 0: self.taperingfactor = float(taperingfactor)

        self.doui=0
        #doui = input('enter the doui')
        #if doui!= 0: self.doui = float(doui)

        self.taperingfunction=lambda x: np.hanning(x)
        #taperingfunction=input('enter the taperingfunction')
        #if len(taperingfunction) != 0: self.taperingfunction = taperingfunction

        self.regressionmethod='taperedhann'
        #regressionmethod=input('enter the regressionmethod')
        #if len(regressionmethod) != 0: self.regressionmethod = regressionmethod

class Varargout:
    def __init__(self,data,cfg):
        self.data=data
        self.cfg=cfg

