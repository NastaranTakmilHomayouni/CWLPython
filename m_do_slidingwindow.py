# 'overseer' function for performing & logging subtraction with sliding
# windows.
# [data, cfg] = m_do_slidingwindow(data, cfg)
import numpy as np
import pdb
from fit_regmat_to_signalmat import fit_regmat_to_signalmat
def m_do_slidingwindow(outputData, cfg):
    cwregression = cfg.cwregression
    if 'do_logging' in cwregression.__dict__:
        do_logging = cwregression.do_logging
    else:
        do_logging = 0
    ##############################################################################################
    number_of_samples_in_window = int(np.floor(cwregression.srate  * cwregression.windowduration + 1))
    step_in_samples = number_of_samples_in_window - 1
    delay_in_samples = np.floor(cwregression.srate * cwregression.delay)
    window = []
    x = outputData.data[cwregression.channelinds,:]
    regs = outputData.data[cwregression.regressorinds,:]
    print(type(x))
    print(type(regs))
    # for now...just store the subtracted data, so I can view it...
    subtracted_signals = np.zeros(x.shape)
# stores logging (fitparameters, etc).
    store_logging={}

# if you later decide to skip certain bad fits / windows, the division needs
# to be accounted for separately.Since this is a bit more complicated, we
# now divide (see later on) by 2 ^ (taper_factor-1) and leave it at that.
# for this purpose, matrix_weights_fits would exist (see commented code).

# keyboard;
# jcheck=1;
    current_sample = 1
    count=0

    #try:
    while current_sample < x.shape[1] - number_of_samples_in_window:
        count = count + 1
        #
        range=np.arange(current_sample-1,(current_sample + number_of_samples_in_window-1))
        #range=slice(current_sample,current_sample + number_of_samples_in_window,1)

            #range = slice(current_sample, current_sample + number_of_samples_in_window, 1)
        # do a new window;
        xpart = x[:, range]
        regspart = regs[:, range]
        #print()
        [fittedregs,logging] = fit_regmat_to_signalmat(xpart, regspart, [], delay_in_samples, [], do_logging)

        subtracted_signals[:, range[0: -1]] = fittedregs[:, 0: -1]

        # disp([range(1) range(end - 1)]);
        store_logging = np.append(store_logging, logging)

        current_sample = current_sample + step_in_samples

    #except:
        #pdb.set_trace()
        #my_input=input('write sth')
    cfg.cwregression.logging = store_logging
    outputData.subtracted_data = subtracted_signals

    return (outputData, cfg)
