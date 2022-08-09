#function vec_out
import numpy as np
def my_vector_shifter(vec_in, shift):
    if np.absolute(shift)>len(vec_in):
        raise('the shift value you specified is bigger than the size of the vector!')
    if shift is 0:
        vec_out = vec_in
    elif shift < 0:
        end_point = vec_in[len(vec_in)-1]
        vec_out = np.concatenate(( vec_in[1 - shift-1:len(vec_in)-1], np.multiply( end_point,np.ones( (1, -shift) ) ) ) )
    elif shift > 0:
        begin_point = vec_in[0]
        vec_out = np.concatenate( begin_point*np.ones((1,shift)) ,vec_in[1:len(vec_in)-1- shift] )

