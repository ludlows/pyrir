# distutils: language=C

"""
2019-Dec
github.com/ludlows
Python Wrapper for Room Impulse Response
"""


import cython
import numpy as np
cimport numpy as np


cdef extern from "rir.c":
    cdef void comp_rir(double sound_speed, double fs, 
	          double size_x, double size_y, double size_z, 
	          double  mic_x, double  mic_y, double  mic_z, 
	          double  src_x, double  src_y, double  src_z, 
	          double * beta_arr,                           
	          double mic_azimuth, double mic_elevation,    
	          double * impulse, int impulse_len,           
              int     high_pass,                           
	          char    mic_type,                            
	          int     reflect_order)

cpdef np.ndarray[np.float64_t, ndim=1, mode="c"] rir(double sound_speed, double fs, 
        np.ndarray[np.float64_t, ndim=1, mode="c"] room_size,
        np.ndarray[np.float64_t, ndim=1, mode="c"] mic_pos, 
        np.ndarray[np.float64_t, ndim=1, mode="c"] src_pos,
        np.ndarray[np.float64_t, ndim=1, mode="c"] beta_arr,
        double mic_azimuth,
        double mic_elevation,
        int    impulse_len,
        int    high_pass,
        char   mic_type,
        int    reflect_order):
    
    cdef np.ndarray[np.float64_t, ndim=1, mode="c"] impulse = np.zeros((impulse_len,), dtype=np.float64)
    comp_rir(
        sound_speed, fs, 
        room_size[0], room_size[1], room_size[2],
        mic_pos[0], mic_pos[1], mic_pos[2],
        src_pos[0], src_pos[1], src_pos[2],
        &(beta_arr[0]),
        mic_azimuth, mic_elevation,
        &(impulse[0]), impulse_len,
        high_pass,
        mic_type,
        reflect_order)
    return impulse
