import np
def DetectChannel(raw):
    channel_filter=np.zeros(shape=(1,len(raw.ch_names) ))
    data = raw.get_data()
    total_ch = len(raw.ch_names) #76
    for i in range(total_ch): #from 0 to 75
        channel_filter[0,i] = np.var(data[i,:]) # Filter based on variance

    val=np.min(channel_filter)
    ch= np.where(channel_filter== val)
    ch=ch[1]
    return ch