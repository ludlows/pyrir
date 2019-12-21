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

    """
    def __init__(self, position):
        """
        position: tuple (x,y,z) or list [x,y,z]
        """
        if len(position) != 3:
            raise ValueError('The length of microphone position should be 3 !!!')
        if not all([isinstance(v, numbers.Number) for v in position]):
            raise ValueError('All the elements of microphone position should be numeric!!!')
        self._pos = tuple(position)
    
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


class Omni(Microphone):
    """
    class for omnidirectional microphone
    """
    def __init__(self, position):
        super(Omni, self).__init__(position)


class Hypercardioid(Microphone):
    """
    class for hypercardioid microphone
    """
    def __init__(self, position, orientation):
        super(Hypercardioid, self).__init__(position)
        if len(orientation) != 2:
            raise ValueError('The length of microphone orientation should be 2 !!!')
        theta, phi = orientation
        if not all([theta >= 0 and theta <= math.pi, phi >= -math.pi and phi <= math.pi]):
            raise ValueError('The value of micophone orientation seems wrong !!!')
        self._orient = tuple(orientation)
