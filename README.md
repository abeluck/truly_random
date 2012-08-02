# truly_random - a python RNG that uses /dev/random

This is a simplified version of truly_random from [Danny Yoo](https://hkn.eecs.berkeley.edu/~dyoo/python/truly_random/)
(dyoo@hkn.eecs.berkeley.edu).

Implements python's standard library random interface.


example usage:

    import truly_random
    ruly_random.random() #-> 0.27969009844631798
    ruly_random.choice('aeiou') #-> e

Licensed under the Python Software Foundation License
