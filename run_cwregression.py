import numpy as np
import pickle
import os
from Data import Data
from Vararg import Varargin,Varargout
from Configuration import cfg
from m_do_taperedhann import m_do_taperedhann
from m_do_slidingwindow import m_do_slidingwindow
from m_do_everything import m_do_everything
#from bcg_correction_tool_ui import bcg_correction_tool_ui
import time
import scipy.io
###############################################################################
##############################################################################
def run_cwregression(CWLVarargin):
    from Configuration import cfg
    if len(CWLVarargin.__dict__)<9 and len(CWLVarargin.__dict__)==0:
        raise('not enough inputs')
    elif len(CWLVarargin.__dict__)>10:
        raise('too many arguments')
    ###############################################
    if len(CWLVarargin.__dict__)==10 or len(CWLVarargin.__dict__)==9:
        if str(CWLVarargin.data) == 'object':
            outputData =CWLVarargin.data.data
        else:
            outputData=CWLVarargin.data

        cfg.cwregression=cfg.cwregression(CWLVarargin.srate,CWLVarargin.windowduration,CWLVarargin.delay,CWLVarargin.taperingfactor,CWLVarargin.taperingfunction,CWLVarargin.regressorinds,CWLVarargin.channelinds,CWLVarargin.regressionmethod,CWLVarargin.doui)

        if len(CWLVarargin.__dict__) == 10:
            doui=CWLVarargin.doui
        else:
            doui=1
    elif len(CWLVarargin.__dict__)==1:
        print('using default values')
        doui=1
        outputdata = CWLVarargin.data
        from Configuration import cfg
        cwregression = cfg.cwregression([], 4.0, 0.021,
                                    1, 'taperedhann',[],
                                    [], 'none',1)
    ######################################################################
    main_path=os.getcwd()
    if (cfg.cwregression.method is 'taperedhann'):
        print('running cwregerssion on data with shape {} with method : taperedhann'.format(outputData.data.shape))
        (outputData,cfg) = m_do_taperedhann(outputData,cfg)
        #os.chdir('C:/Users/nasta/PycharmProjects/CWL/data/LernMulti3/raw/Python')
        os.makedirs(os.path.join(main_path, 'PythonOutput','TaperedHann'))
        os.chdir(os.path.join(main_path, 'PythonOutput','TaperedHann'))
        subtracted_data_taper=outputData.subtracted_data
        scipy.io.savemat('subtracted_data_taper.mat', {'subtracted_data_taper': subtracted_data_taper})
        #np.save('subtracted_data_weights.npy', outputData.subtracted_data_weights)
        #np.save('subtracted_data.npy', outputData.subtracted_data)
    elif (cfg.cwregression.method is 'slidingwindow'):
        print('running cwregerssion on data with shape {} with method : slidingwindow'.format(outputData.data.shape))
        (outputData, cfg) = m_do_slidingwindow(outputData, cfg)
        #os.chdir('C:/Users/nasta/PycharmProjects/CWL/data/LernMulti3/raw/Python')
        os.makedirs(os.path.join(main_path, 'PythonOutput','SlidingWindow'))
        os.chdir(os.path.join(main_path, 'PythonOutput','SlidingWindow'))
        #np.save('subtracted_data.npy', outputData.subtracted_data)
        subtracted_data_sw=outputData.subtracted_data
        scipy.io.savemat('subtracted_data_sw.mat', {'subtracted_data_sw': subtracted_data_sw})

    elif (cfg.cwregression.method is 'everything'):
        print('running cwregerssion on data with shape {} with method : everything'.format(outputData.data.shape))
        (outputData, cfg) = m_do_everything(outputData, cfg)
        #os.chdir('C:/Users/nasta/PycharmProjects/CWL/data/LernMulti3/raw/Python')
        os.makedirs(os.path.join(main_path, 'PythonOutput','Everything'))
        os.chdir(os.path.join(main_path, 'PythonOutput','Everything'))
        #np.save('subtracted_data.npy', outputData.subtracted_data)
        subtracted_data_ev=outputData.subtracted_data
        scipy.io.savemat('subtracted_data_ev.mat', {'subtracted_data_ev': subtracted_data_ev})

    elif (cfg.cwregression.method is 'none'):
        print('no correction will be performed')
    else:
        raise('some error occured!')

    #CWLVarargout = Varargout(outputData,cfg)














