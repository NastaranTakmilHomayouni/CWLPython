# 'overseer' function for performing & logging subtraction without
# any kind of windowing.
import numpy as np
from fit_regmat_to_signalmat import fit_regmat_to_signalmat
# [data,cfg]=m_do_everything(data,cfg)
from ypstruct import struct
def m_do_everything(outputData,cfg):
# probably can be removed..
# cfg.cwregression.srate = 1000;              %srate=1000;
# cfg.cwregression.windowduration = 1.3;      %windowduration=2.0;
# cfg.cwregression.delay = 0.050;             %delay=0.050;
# cfg.cwregression.taperingfactor = 2;        %taperingfactor=1;
# cfg.cwregression.taperingfunction = @hann;  %taperingfunction=@hann;
# cfg.cwregression.regressorinds = 33:40;     %regressorinds=1:30;
# cfg.cwregression.channelinds = 1:31;        %channelinds=33:40;
# cfg.cwregression.method='taperedhann';     % What method are we using??
## 'everything','none','slidingwindow' are the other options for method.
    #cfg=struct()
    #cfg = namedtuple("cfg", "cwregression ")
    #cwregression={'do_logging':1}
    #cfg={'cwregression':cwregression}
    cwregression=cfg.cwregression
    #cwregression = namedtuple('cwregression','do_logging')
    if 'do_logging' in cwregression.__dict__:
        do_logging = cwregression.do_logging
    else:
        do_logging = 0

    delay_in_samples = np.floor(cwregression.srate*cwregression.delay)

    x=outputData.data[cwregression.channelinds,:]
    regs=outputData.data[cwregression.regressorinds,:]

    window=[]

    [subtracted_signals,logging]=fit_regmat_to_signalmat(x,regs,window,delay_in_samples,[],do_logging);

    cfg.cwregression.logging = logging
    outputData.subtracted_data = subtracted_signals

    return (outputData, cfg)