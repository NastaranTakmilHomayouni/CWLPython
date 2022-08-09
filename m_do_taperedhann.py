# [data, cfg] = m_do_taperedhann(data, cfg)
from fit_regmat_to_signalmat import fit_regmat_to_signalmat
from IPython.display import display
from math import remainder as rem
import numpy as np
import os
def m_do_taperedhann(outputData, cfg):
    #global range
    cwregression = cfg.cwregression
    if 'do_logging' in cwregression.__dict__:
        do_logging = cwregression.do_logging
    else:
        do_logging = 0
    ##########################################################
    print('breakpoint')
    taper_factor = cwregression.taperingfactor
    function_to_calculate_nwindows = lambda x : 2 * (2 ** x - 1) + 1
    nwindows = function_to_calculate_nwindows(taper_factor)
    number_of_samples_in_window = int(np.floor(cwregression.srate * cwregression.windowduration+ 1))
    print('number of samples in a window',number_of_samples_in_window)
    #print((number_of_samples_in_window - 1) % (2 ** taper_factor)) it is 0
    while ((number_of_samples_in_window - 1) / (2 ** taper_factor))%1 > 0:
        number_of_samples_in_window = number_of_samples_in_window + 1
        print('number of samples in each windows is now', number_of_samples_in_window)

    window = cwregression.taperingfunction(number_of_samples_in_window)
    window = np.expand_dims(window, axis=0)

    print('size of each windows is ', window.shape)
# bugfix for own custum windows...
    if (window.shape[0] == 1):
        window = np.transpose(window)
        print('size of each windows is ', window.shape)
    np.save('window.npy', window)
    nsteps = 2 ** taper_factor
    step_in_samples =int(np.floor((number_of_samples_in_window - 1) / nsteps))
    begins_segments = [1] #
    for i in np.arange(1,nsteps,1):#
        begins_segments=np.append(begins_segments,step_in_samples+begins_segments[-1])
        print(begins_segments)
# how long is one step?
    delay_in_samples = np.floor(cwregression.srate*cwregression.delay)
    print('delay in samples is',delay_in_samples)
# how much should we divide by - - note this would need updating probably!
    division_factor = 2 ** (taper_factor - 1)  #

    x = outputData.data[cwregression.channelinds,:]  #
    regs = outputData.data[cwregression.regressorinds,:] #
    if taper_factor == 0:
        print('no subtraction will occur; taper factor is zero (should be >=1)!')

    matrix_stored_fits = np.zeros((nwindows,len(cwregression.channelinds), number_of_samples_in_window))
    print('matrix_stored_fits dimension is',matrix_stored_fits.shape)
    matrix_stored_weights = np.zeros((number_of_samples_in_window, nwindows))
    subtracted_signals = np.zeros(x.shape)
    subtracted_signals_weights = np.zeros((x.shape[1], 1))

    store_logging={}
    summation=np.zeros((len(cwregression.channelinds), step_in_samples+1))
    print('summation dimension is ', summation.shape) #69 by 501
    summation_weights=np.zeros((step_in_samples+1, 1)) #501 by 1
    print('summation_weights dimension is ', summation_weights.shape)

    jcheck=0 # just a counter...
    max_windows = np.round(outputData.data.shape[1] / step_in_samples) - 2 ** taper_factor
    print('max_windows is',max_windows)
    current_sample = 1
    while current_sample < x.shape[1] - number_of_samples_in_window:
        print(current_sample, '<', x.shape[1], '-', number_of_samples_in_window)
        jcheck = jcheck + 1
        print('doing window{}: out of approx.{}'.format( jcheck, max_windows))
        #range= np.arange(current_sample-1,((current_sample-1)+number_of_samples_in_window))
        range=slice(current_sample-1,current_sample + number_of_samples_in_window-2,1)
        #print(range.shape)
        if current_sample >= number_of_samples_in_window:
            summation[:]=0
            summation_weights[:]=0
            print('summation_weights shape', summation_weights.shape)
            for i in np.arange(1,(2 ** taper_factor)+1,1):
                print('i is now :' , i)
                sumrange =np.arange((i - 1) * step_in_samples,i * step_in_samples+1)
                print('sumrange shape is ',sumrange.shape)
                #sumrange=slice(((i - 1) * step_in_samples),(i * step_in_samples)+1,1)
                summation = summation + matrix_stored_fits[i-1,:, ((i - 1) * step_in_samples):(i * step_in_samples)+1] #summation is 69 by 501
                #np.save('summation.npy', summation)
                print('summation shape is ',summation.shape)
                print('summation_weights shape', summation_weights.shape)
                an_array = matrix_stored_weights[((i - 1) * step_in_samples):(i * step_in_samples) + 1, i-1]
                an_array = np.expand_dims(an_array, axis=1)
                #np.save('an_array.npy', an_array)
                #np.save('matrix_stored_weights.npy', matrix_stored_weights)
                summation_weights = summation_weights + an_array
                print('summation_weights shape is ',summation_weights.shape)
                print('matrix_stored_weights[({} * {}):({} * {})+1, {}] size is {}'.format((i - 1),step_in_samples,i,step_in_samples,i,an_array.shape))

            #subtractrange = slice((current_sample - step_in_samples + 1),current_sample+1,1)

            subtractrange = np.arange((current_sample - step_in_samples ), current_sample)
            print('subtractrange shape is',subtractrange.shape)
            #subtractrange=np.expand_dims(subtractrange,axis=0)
            my_array=summation_weights[1:] #(500, 501)
            new_array=subtracted_signals_weights[(current_sample - step_in_samples + 1):current_sample+1] #(500, 1)
            print(my_array.shape)
            print(subtracted_signals_weights.shape)
            print(new_array.shape)
            #print('subtractrange dimension is ', subtractrange.shape)
            print('subtracted_signals dimension is ', subtracted_signals.shape)
            print('subtracted_signals_weights dimension is ', subtracted_signals_weights.shape)

            subtracted_signals[:,(current_sample - step_in_samples ):current_sample] = summation[:, 1:] #69 by 500
            p1=subtracted_signals_weights
            p2=summation_weights[1:]
            #np.save('summation_weights.npy', summation_weights)
            #np.savetxt("array.txt", summation_weights)
            print('shape of subtracted_signals_weights',p1.shape)
            print('shape of summation_weights[1:]', p2.shape)
            subtracted_signals_weights[(current_sample - step_in_samples ):current_sample] = summation_weights[1:]
            #np.save('subtracted_signals_weights.npy', subtracted_signals_weights)

        #xpart = x[:, range]
        #regspart = regs[:, range]
        xpart=x[:,current_sample-1:current_sample + number_of_samples_in_window-1]
        regspart =regs[:,current_sample-1:current_sample + number_of_samples_in_window-1]
        #xpart = np.round(xpart, 4)
        #regspart = np.round(regspart, 4)
        [fittedregs,logging] = fit_regmat_to_signalmat(xpart, regspart, window, delay_in_samples, [], do_logging)
        print('matrix_stored_fits.shape is ',matrix_stored_fits.shape)
        print(np.arange(matrix_stored_fits.shape[2]-1,0,-1))

        for im in np.arange(matrix_stored_fits.shape[0],1,-1):
            print('im nastaran is ' ,im)
            print(matrix_stored_fits.shape)
            matrix_stored_fits[im-1,:,:]=matrix_stored_fits[im - 2,:,:]
            matrix_stored_weights[:,im-1]=matrix_stored_weights[:, im - 2]

        matrix_stored_fits[0,:,:] = fittedregs[:]
        mstw=matrix_stored_weights[:, 0]
        print('matrix_stored_weights shape is', mstw.shape)
        matrix_stored_weights[:, 0] = np.squeeze(window)
        store_logging=np.append(store_logging,logging)
        current_sample = current_sample + step_in_samples
    #inds = subtracted_signals_weights > 0
    #inds=[i for i in range(0,len(subtracted_signals_weights)) if subtracted_signals_weights[i][0] >0]
    #subtracted_signals_weights.tofile('variable.txt')
    indexs = np.where(subtracted_signals_weights > 0.0)[0]
    os.chdir('C:/Users/nasta/PycharmProjects/CWL/data/LernMulti3/PythonOutput')
    np.save('subtracted_signals_weights.npy', subtracted_signals_weights)
    np.save('subtracted_signals_weights.npy', subtracted_signals_weights)
    if np.any(indexs):
        subtracted_signals[:, indexs] = np.divide( subtracted_signals[:, indexs], (  np.ones((x.shape[0], 1)  ) @ subtracted_signals_weights[ indexs].T ))


        cfg.cwregression.logging = store_logging
        outputData.subtracted_data = subtracted_signals
        outputData.subtracted_data_weights = subtracted_signals_weights

    #np.save('subtracted_data.npy', subtracted_signals)
    return (outputData,cfg)


