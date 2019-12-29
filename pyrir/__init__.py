'''
pyrir Module for Simulating Room Impulse Response

author: https://github.com/ludlows
2019-11 

This program is designed with the hope that it will be useful, but WITHOUT ANY GUARANTEE.
'''
import os
import numpy as np
from scipy.io import wavfile
from .microphone import Omni, Cardioid, Dipole, Hypercardioid, Subcardioid, Microphone
from .speaker import Speaker
from .room import ReflectRoom, ReverbRoom
from .cyrir import rir


__all__ = [
    'Omni', 'Cardioid', 'Dipole', 'Hypercardioid', 'Subcardioid',
    'RIR', 'Field', 'Speaker', 'ReflectRoom', 'ReverbRoom'
    ] 


class RIR:
    """
    class for RIR (Room Impulse Response)
    Args:
        fs            : integer Sampling rate
        rir_array     : numpy array (n_channel, length of RIR)
        name          : str
        channel_names : list or tuple of str
        speaker_name  : str
    """
    _rir_id = 0
    def __init__(self, fs, rir_array, channel_names, speaker_name, name=None):
        """
        Args:
            fs            : integer Sampling rate
            rir_array     : numpy array (n_channel, length of RIR)
            name          : str
            channel_names : list or tuple of str
            speaker_name  : str
        """ 
        self._rir_array = rir_array 
        self._fs = fs
        if len(rir_array.shape) == 2:
            self._n_mic, self._n_sample = rir_array.shape
        else:
            raise ValueError('The shape of RIR Numpy Array should be 2')
        if not name:
            self._name = "RIR_{:d}_nMic_{:d}_nSample_{:d}".format(
                self._rir_id, self._n_mic, self._n_sample)
        else:
            self._name = name
        self._rir_id += 1
        self._mic_names = channel_names
        self._spk_name = speaker_name
    
    def __str__(self):
        return self._name
    
    def get_numpy(self):
        """
        Returns numpy array of RIR
        """
        return self._rir_array.copy()
    
    def apply2audio1D(self, audio1d):
        """
        Returns the reverb audio for each mirophone
        Args:
            audio1d: 1d numpy float array
        """
        length = audio1d.shape[0]
        ans = np.empty((self._n_mic, length))
        for i in range(self._n_mic):
            ans[i] = np.convolve(self._rir_array[i, :], audio1d, mode='same') 
        return ans

    def apply2audio_file(self, filepath):
        """
        Returns A list of numpy array, the length of the list is the number of auio channels
        Args:
            filepath: the audio filepath, supporting .WAV format only
        """
        fs, data = wavfile.read(filepath)
        if fs != self._fs:
            raise RuntimeError("The Sampling Rate of the Audio File is not compatible with the RIR.")
        if len(data.shape) == 1:
            n_channel = 1
        elif len(data.shape) == 2:
            n_channel = data.shape[0]
        else:
            raise ValueError('The Channel Number of Input Audio File is Wrong.')
        if not np.issubdtype(data.dtype, np.floating):
            data = data.astype(np.float32) / np.iinfo(data.dtype).max 
        if n_channel == 1:
            return [self.apply2audio1D(data)]
        return [self.apply2audio1D(data[:,i]) for i in range(n_channel)]

    def apply2audio_folder(self, audio_folder):
        """
        Returns None but writing reverb audio files with float32 format
            Supporting WAV format only for now
        Args:
           audio_foler: the clean audio folder
        """
        files = [f for f in os.listdir(audio_folder) if f.endswith('.wav') or f.endswith('.WAV')]
        out_folder = self._spk_name + "_" + "_".join(self._mic_names)
        os.makedirs(out_folder, exist_ok=True)
        for k,filename in enumerate(files):
            path = os.path.join(audio_folder, filename)
            arr_list = self.apply2audio_file(path)
            fname = ".".join(filename.split('.')[:-1])
            for i, arr in enumerate(arr_list):
                reverb_fname = fname + "_ch{:d}_Reverb.wav".format(i)
                arr32 = arr.astype(np.float32)
                wavfile.write(os.path.join(out_folder, reverb_fname), self._fs, arr32.T)
            print('Writing {:.2f}%.'.format( (k+1.0) / len(files)))
        

class Field:
    """
    class for Sound (Acoustic) Field 
    Args: 
        fs     (Hz)      : integer, Sampling Rate
        n_sample         : integer, the length of FIR (Finite Impulse Response)
        sound_speed (m/s): double,  the speed of sound
        high_pass        : bool,  enable high pass filter or not
        name             : str
    """
    _field_id = 0
    def __init__(self, fs, n_sample=1024, sound_speed=340, high_pass=True, name=None):
        """
        Args: 
            fs     (Hz)      : integer, Sampling Rate
            n_sample         : integer, the length of FIR (Finite Impulse Response)
            sound_speed (m/s): double,  the speed of sound
            high_pass        : bool,  enable high pass filter or not
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
        self._high_pass = high_pass
    
    def compute_rir(self, room):
        """
        Args:
            room: Room Object with Microphoena and Speaker
        Returns tuple of RIR objects
        """
        # beta array
        if isinstance(room, ReflectRoom):
            beta = room.get_beta_array()
        else: # reverb Room
            # calculate beta array
            rt60 = room.get_rt60()
            x, y, z  = room.get_size()
            vol = x * y * z
            area = 2 * (x*y + x*z + y*z)
            alpha = 24.0 * vol * np.log(10.0) / (self._sound_speed * area * rt60)
            if alpha > 1:
                raise ValueError("The Room Size makes the wall reflection coefficients invalid.")
            beta0 = np.sqrt(1.0-alpha)
            beta = tuple(beta0 for _ in range(6))
        beta = np.array(beta, dtype=np.float64)

        comb = room.mic_speaker_combination()
        n_mic = len(comb[0][0])
        room_size = np.array(room.get_size(), dtype=np.float64)
        rirobj_list = []
        for mic_arr, spk in comb:
            src_pos = np.array(spk.get_pos(),  dtype=np.float64)
            mic_names = [str(mic) for mic in mic_arr]
            rir_numpy_mics = np.empty((n_mic, self._n_sample), dtype=np.float64)
            for i, mic in enumerate(mic_arr):
                mic_pos = np.array(mic.get_pos(), dtype=np.float64)
                if isinstance(mic, Dipole):
                    mic_type = ord('d')
                    mic_azimuth, mic_elevation = mic.get_orient()
                elif isinstance(mic, Subcardioid):
                    mic_type = ord('s')
                    mic_azimuth, mic_elevation = mic.get_orient()
                elif isinstance(mic, Cardioid):
                    mic_type = ord('c')
                    mic_azimuth, mic_elevation = mic.get_orient()
                elif isinstance(mic, Hypercardioid):
                    mic_type = ord('h')
                    mic_azimuth, mic_elevation = mic.get_orient()
                else: # Omni
                    mic_type = ord('o')
                    mic_azimuth, mic_elevation = (0.0,0.0)
                mic_azimuth   = mic_azimuth / 180.0 * np.pi
                mic_elevation = mic_elevation / 180.0 * np.pi 
                rir_numpy = rir(
                    self._sound_speed,
                    self._fs,
                    room_size,
                    mic_pos,
                    src_pos,
                    beta,
                    mic_azimuth,
                    mic_elevation,
                    self._n_sample,
                    self._high_pass,
                    mic_type,
                    room.get_reflect_order()
                )
                rir_numpy_mics[i] = rir_numpy
            
            rirobj_list.append(RIR(self._fs, rir_numpy_mics, tuple(mic_names), str(spk)))
        return tuple(rirobj_list)
    
    def __str__(self):
        return self._name