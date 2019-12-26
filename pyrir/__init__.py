
import numpy as np

from .microphone import Omni, Cardioid, Dipole, Hypercardioid
from .speaker import Speaker
from .cyrir import rir


class RIR:
    pass 

class Field:
    def __init__(self, fs, sound_speed=340):
        self.fs = fs 
        self.sound_speed = sound_speed
    