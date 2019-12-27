'''
pyrir Module for Simulating Room Impulse Response

author: github.com/ludlows
2019-11 

This program is designed with the hope that it will be useful, but WITHOUT ANY GUARANTEE.
'''

import numpy as np
from scipy.io import wavfile
from .microphone import Omni, Cardioid, Dipole, Hypercardioid, Subcardioid, Microphone
from .speaker import Speaker

from .cyrir import rir



class RIR:
    """
    class for RIR (Room Impulse Response)
    """
    _rir_id = 0
    def __init__(self, rir_array, name=None):
        """
        Args:
            rir_array: numpy array (n_channel, length of RIR, n_speaker)
            name     : str
        """ 
        self._rir_array = rir_array
        if len(rir_array.shape) == 3:
            self._n_mic, self._n_sample, self._n_speaker = rir_array.shape
        elif len(rir_array.shape == 2):
            self._n_mic, self._n_sample = rir_array.shape
            self._n_speaker = 1
        else:
            raise ValueError('The shape of RIR Numpy Array should be either 2 or 3')

        if not name:
            self._name = "RIR_{:d}_nMic_{:d}_nSample_{:d}_nSpeaker_{:d}".format(
                self._rir_id, self._n_mic, self._n_sample, self._n_speaker)
        else:
            self._name = name
        self._rir_id += 1
    
    def __str__(self):
        return self._name
    
    def get_numpy(self):
        """
        Returns numpy array of RIR
        """
        return self._rir_array.copy()


class Field:
    """
    class for Sound (Acoustic) Field 
    """
    _field_id = 0
    def __init__(self, fs, n_sample = 1024, sound_speed=340, name=None):
        """
        Args: 
            fs     (Hz)      : integer, Sampling Rate
            n_sample         : integer, the length of FIR (Finite Impulse Response)
            sound_speed (m/s): double,  the speed of sound
            name             : str
        """
        self._fs = fs 
        self._n_sample = n_sample
        self._sound_speed = sound_speed
        if not name:
            self._name = "Field_{:d}_fs_{:d}_nSample_{:d}".format(self._field_id, fs, n_sample)
        else:
            self._name = name
        self._field_id += 1
    
    def compute_rir(self, room):
        """
        Args:
            room: Room Object with Microphoena and Speaker
        Returns a list of RIR objects
        """
        pass

    @staticmethod
    def apply_rir2array(rir_obj, audio_array):
        """
        Returns 
        
        Args:

           rir_obj:
           audio_arrya: 1D numpy array
        """
        pass 

    def apply_rir2folder(self, rir_obj_list, audio_folder, out_folder='out'):
        """
        check sampling frequency
        """
        pass
    
