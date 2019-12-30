# pyrir
Lite Package for Room Impulse Response

# requirements

```bash
numpy
scipy
cython
```

# install
```bash
pip install pyrir
```
or
```bash
pip install https://github.com/ludlows/pyrir/archive/master.zip
```

# example 

It is supporting Omni, Dipole, Cardioid, Subcardioid and Hypercardioid Beam Patterns. 

## Microphone Array with 1 Speaker
```python
import numpy as np 
from pyrir import Omni, Dipole, Cardioid, Subcardioid, Hypercardioid, Field, RIR, ReflectRoom, ReverbRoom

# Acoustic Field
fs = 48000 # sampling rate
n_sample = 1024 # number of supports of RIR train
field = Field(fs, n_sample=n_sample)

# Construct Room
rt60 = 0.4 # second
room = ReverbRoom((5,5,3.2), rt60)

# Microphon Array
azimuth_degree = 0
elevation_degree = 0
dipole = Dipole((2,1.5,1.6), (azimuth_degree,elevation_degree))
omni = Omni((2,1.5,1.6))

# speaker
doa = 0    # degree 
radius = 1.5 # meter
speaker = dipole.generate_speaker(radius, doa)

# setup speaker and mic array
room.setup_mic_speaker([dipole, omni], speaker)

# RIR object tuple, whose length equals to the number of speakers
rir_tuple = field.compute_rir(room)
np.save('RIR_Dipole_Omni.npy', rir_tuple[0].get_numpy())

# Reverb numpy Array
reverb_numpy_array = rir_tuple[0].apply2audio1D(clean_audio1D)

# Reverb numpy Array List Supporting Multichannel Clean Audio (WAV format only for now) 
speaker_audio_file  = 'speaker_clean_audio.wav'
reverb_numpy_audio_list = rir_tuple[0].apply2audio_file(speaker_audio_file)

# Reverb audio folder
speaker_audio_folder = 'speaker_audio_folder'
rir_tuple[0].apply2audio_folder(speaker_audio_folder)
```


## Microphone Array with Multiple Speaker
```python
import numpy as np 
from pyrir import Omni, Dipole, Cardioid, Subcardioid, Hypercardioid, Field, RIR, ReflectRoom, ReverbRoom

# Acoustic Field
fs = 48000 # sampling rate
n_sample = 1024 # number of supports of RIR train
field = Field(fs, n_sample=n_sample)

# Construct Room by Wall Reflection Coefficeints
room = ReflectRoom((5,5,3.2), (0.8, 0.8, 0.8, 0.8, 0.8, 0.8))

# Microphon Array
azimuth_degree = 0
elevation_degree = 0
dipole = Dipole((2,1.5,1.6), (azimuth_degree,elevation_degree))
omni = Omni((2,1.5,1.6))

# speaker1 and speaker2
doa = 0    # degree 
radius = 1.5 # meter
speaker1 = dipole.generate_speaker(radius, doa)
speaker2 = omni.generate_speaker(1, 90)

# setup speaker and mic array
room.setup_mic_speaker([dipole, omni], [speaker1, speaker2])

# RIR 
rir_spk1, rir_spk2 = field.compute_rir(room)

# merge reverb voice from 2 speakers 
# (spk1.wav and spk2.wav should have same number of channels)
merged_channels = [
    reverb1[:, :min(reverb1.shape[1], reverb2.shape[1])] + reverb2[:,:min(reverb1.shape[1], reverb2.shape[1])] for reverb1, reverb2 in zip(rir_spk1.apply2audio_file('spk1.wav'), rir_spk2.apply2audio_file('spk2.wav'))]
```

# Reference Code
The C Backend Code is from the project of Prof. Emanuël Habets.
https://github.com/ehabets/RIR-Generator   


