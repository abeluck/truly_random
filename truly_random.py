"""
Simplified version of truly_random from [0]

A random number generator that uses /dev/random. Uses the same interface
as python's random module

Licensed under the Python Software Foundation License

usage:
    import truly_random
    ruly_random.random() #-> 0.27969009844631798
    ruly_random.choice('aeiou') #-> e

[0]: https://hkn.eecs.berkeley.edu/~dyoo/python/truly_random/
     Danny Yoo (dyoo@hkn.eecs.berkeley.edu)
"""
## For these following import statements, we put underscores in front
## of the names to prevent name confusion between the module '_random'
## and the function 'random'.

import random as _random
import urllib as _urllib
import math as _math
import string as _string


class RandomBitSource:
    """An abstract class for any "source" of random bits."""

    ## All subclasses of RandomBitSource should implement the __call__
    ## method.
    def __call__(self, n):
        """Returns a list of n random bits."""
        pass

class DevRandomBitSource(RandomBitSource):
    _DEV_RANDOM_DEVICE = '/dev/random'


    def __init__(self, file=_DEV_RANDOM_DEVICE):
        self._devrandom = open(file)


    def __call__(self, n):
        """Returns a list of n random bits."""
        self.bits = []
        while len(self.bits) < n:
            byte = self._devrandom.read(1)
            self.bits.extend(byte_to_binary(ord(byte)))
        return self.bits[:n]


######################################################################


class TrulyRandom(_random.Random):
    """A subclass of _random.Random that supplies truly random
    numbers, using a RandomBitSource as a supply of random bits."""


    """Tim Peters suggests using 53 bits for each random number we
    generate, since the floating point mantissa should be able to
    represent it."""
    _BITS_USED = 53


    def __init__(self, source):
        self._source = source


    def random(self):
        """Returns a random float within the half-open interval [0, 1)."""
        bits = self._source(self._BITS_USED)
        return _math.ldexp(binary_list_to_long(bits), -self._BITS_USED)


    ## The rest of these functions won't be useful, since our source
    ## is truly random and can't be seeded.
    def seed(self, a=None): pass
    def getstate(self): return None
    def setstate(self, state): pass
    def jumpahead(self, n): pass

######################################################################

## Finally, for the remainder of the code, we want to emulate the
## interface of the Standard Library's random module.

"""The following functions are defined in the random module:"""
_module_functions = _string.split("""
seed
random
uniform
randint
choice
randrange
shuffle
normalvariate
lognormvariate
expovariate
vonmisesvariate
gammavariate
gauss
betavariate
paretovariate
weibullvariate
getstate
setstate
jumpahead""")


_inst = None
def set_default_randomizer(randomizer):
    """This modifies the module so that the randomizer's methods, listed
in _module_functions, become accessible as if they were functions."""
    global _inst
    _inst = randomizer
    module = globals()
    for function_name in _module_functions:
        module[function_name] = getattr(randomizer, function_name)

def set_default_as_dev_random():
    """Sets the default random bit source as /dev/random."""
    set_default_randomizer(TrulyRandom(DevRandomBitSource()))

## Finally, we set our module's default to use dev_random as the
## BitSource.
set_default_as_dev_random()
