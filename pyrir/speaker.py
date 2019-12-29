'''
Speaker Class for Simulating Room Impulse Response

author: github.com/ludlows
2019-11 

This program is designed with the hope that it will be useful, but WITHOUT ANY GUARANTEE.
'''
import numbers

class Speaker:
    """
    Speaker class
    Args:
            position : (x,y,z) or [x,y,z]
            name     : speaker name, optional
    """
    _speaker_id = 0
    def __init__(self, position, name=None):
        """
        Args:
            position : (x,y,z)
            name     : speaker name
        """
        if len(position) != 3:
            raise ValueError('The length of Speaker position should be 3.')
        if not all([isinstance(v, numbers.Number) for v in position]):
            raise ValueError('All the elements of Speaker position should be numeric.')
        self._pos = tuple(position)
        if not name:
            self._name = "Speaker_{:d}".format(self._speaker_id)
        else:
            self._name = name
        self._speaker_id += 1

    def get_pos(self):
        return self._pos 

    def get_name(self):
        return self._name 

    def __str__(self):
        return "{}_x_{:.1f}_y_{:.1f}_z_{:.1f}".format(self._name, *self._pos)

