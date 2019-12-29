'''
Microphone Class for Simulating Room Impulse Response

author: github.com/ludlows
2019-11 

This program is designed with the hope that it will be useful, but WITHOUT ANY GUARANTEE.
'''
import numbers
import math

from .speaker import Speaker

class Microphone:
    """
    Base Class for microphones
    Args:
        position: tuple (x,y,z) or list [x,y,z]
    """
    _mic_id = 0
    def __init__(self, position, name=None):
        """
        Args:
            position: tuple (x,y,z) or list [x,y,z]
        """
        if len(position) != 3:
            raise ValueError('The length of microphone position should be 3.')
        if not all([isinstance(v, numbers.Number) for v in position]):
            raise ValueError('All the elements of microphone position should be numeric.')
        self._pos = tuple(position)
        if not name:
            self._name = "Mic_{:d}".format(self._mic_id)
        else:
            self._name = name 
        self._mic_id += 1
    
    def get_pos(self):
        return self._pos

    def generate_speaker(self, radius, azimuth_deg, elevation_deg=0):
        """
        Args:
            radius    (meter)     :  the distance between microphone and speaker, meter
            azimuth_deg   (degree):  regarding the microphone as the center, the azimuth angle (degree) from mic to speaker
            elevation_deg (degree):  regarding the microphone as the center, the elevation angle (degree) from  mic to speaker
        
        Returns:
            Speaker instance
        """
        x = self._pos[0] + radius * math.cos(elevation_deg / 180.0 * math.pi) * math.cos(azimuth_deg / 180.0 * math.pi)
        y = self._pos[1] + radius * math.cos(elevation_deg / 180.0 * math.pi) * math.sin(azimuth_deg / 180.0 * math.pi)
        z = self._pos[2] + radius * math.sin(elevation_deg / 180.0 * math.pi)
        return Speaker((x,y,z))
    
    def __str__(self):
        return "{}_x_{:.1f}_y_{:.1f}_z_{:.1f}".format(self._name, *self._pos)
    



class Omni(Microphone):
    """
    class for omnidirectional microphone
    Args:
        position: [x,y,z] or (x,y,z) in meter
        name    : str, optional
    """
    def __init__(self, position, name=None):
        """
        position: [x,y,z] or (x,y,z) in meter
        name    : str, optional
        """
        super(Omni, self).__init__(position, name)
        self._name += "_Omni"


class Hypercardioid(Microphone):
    """
    class for hypercardioid microphone
    Args:
        position:     [x,y,z] or (x,y,z) in meter
        orientation:  (azimuth_deg, elevation_deg) in degree
        name       :  str, optional
    """
    def __init__(self, position, orientation, name=None):
        """
        Args:
            position:     [x,y,z] or (x,y,z) in meter
            orientation:  (azimuth_deg, elevation_deg) in degree
            name       : str
        """
        super(Hypercardioid, self).__init__(position, name)
        if len(orientation) != 2:
            raise ValueError('The length of microphone orientation should be 2 .')
        self._orient = tuple(orientation)
        self._name += "_Hypercardioid"
    
    def get_orient(self):
        """
        Returns (azimuth_deg, elevation_deg) the orientation of Hypercardioid Beam Pattern 
        """
        return self._orient
    
    def __str__(self):
        return "{}_azimDeg_{:.1f}_elevDeg_{:.1f}".format(super().__str__(), *self._orient) 


class Cardioid(Microphone):
    """
    class for Cardioid microphone
    Args:
        position:     [x,y,z] or (x,y,z) in meter
        orientation:  (azimuth_deg, elevation_deg) in degree
        name       :  str, optional
    """
    def __init__(self, position, orientation, name=None):
        """
        Args:
            position:     [x,y,z] or (x,y,z) in meter
            orientation:  (azimuth_deg, elevation_deg) in degree
            name       : str
        """
        super(Cardioid, self).__init__(position, name)
        if len(orientation) != 2:
            raise ValueError('The length of microphone orientation should be 2 .')   
        self._orient = tuple(orientation)
        self._name += "_Cardioid"
    
    def get_orient(self):
        """
        Returns (azimuth_deg, elevation_deg) the orientation of Hypercardioid Beam Pattern 
        """
        return self._orient
    
    def __str__(self):
        return "{}_azimDeg_{:.1f}_elevDeg_{:.1f}".format(super().__str__(), *self._orient) 

    
class Dipole(Microphone):
    """
    class for Dipole microphone
     Args:
        position:     [x,y,z] or (x,y,z) in meter
        orientation:  (azimuth_deg, elevation_deg) in degree
        name       :  str, optional
    """
    def __init__(self, position, orientation, name=None):
        """
        Args:
            position:     [x,y,z] or (x,y,z) in meter
            orientation:  (azimuth_deg, elevation_deg) in degree
            name       : str
        """
        super(Dipole, self).__init__(position, name)
        if len(orientation) != 2:
            raise ValueError('The length of microphone orientation should be 2 .')
        self._orient = tuple(orientation)
        self._name += "_Dipole"

    def get_orient(self):
        """
        Returns (azimuth_deg, elevation_deg) the orientation of Hypercardioid Beam Pattern 
        """
        return self._orient
    
    def __str__(self):
        return "{}_azimDeg_{:.1f}_elevDeg_{:.1f}".format(super().__str__(), *self._orient) 


class Subcardioid(Microphone):
    """
    class for Subcardioid microphone
    Args:
        position:     [x,y,z] or (x,y,z) in meter
        orientation:  (azimuth_deg, elevation_deg) in degree
        name       :  str, optional
    """
    def __init__(self, position, orientation, name=None):
        """
        Args:
            position:     [x,y,z] or (x,y,z) in meter
            orientation:  (azimuth_deg, elevation_deg) in degree
            name       : str
        """
        super(Subcardioid, self).__init__(position, name)
        if len(orientation) != 2:
            raise ValueError('The length of microphone orientation should be 2 .')
        self._orient = tuple(orientation)
        self._name += "_Subcardioid"
    
    def get_orient(self):
        """
        Returns (azimuth_deg, elevation_deg) the orientation of Hypercardioid Beam Pattern 
        """
        return self._orient
    
    def __str__(self):
        return "{}_azimDeg_{:.1f}_elevDeg_{:.1f}".format(super().__str__(), *self._orient) 


