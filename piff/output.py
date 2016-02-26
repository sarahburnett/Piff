# Copyright (c) 2016 by Mike Jarvis and the other collaborators on GitHub at
# https://github.com/rmjarvis/Piff  All rights reserved.
#
# Piff is free software: Redistribution and use in source and binary forms
# with or without modification, are permitted provided that the following
# conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the disclaimer given in the accompanying LICENSE
#    file.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the disclaimer given in the documentation
#    and/or other materials provided with the distribution.

"""
.. module:: output
"""

from __future__ import print_function

def process_output(config, logger=None):
    """Parse the output field of the config dict.

    :param config:      The configuration dict.
    :param logger:      A logger object for logging debug info. [default: None]

    :returns: an OutputHandler
    """
    import piff

    if logger is None:
        logger = config.setup_logger(verbosity=0)

    if 'output' not in config:
        raise ValueError("config dict has no output field")
    config_output = config['output']

    # Get the class to use for handling the output data
    # Default type is 'File'
    # Not sure if this is what we'll always want, but it would be simple if we can make it work.
    output_handler_class = eval('piff.Output' + config_output.pop('type','File'))

    # Read any other kwargs in the output field
    kwargs = output_handler_class.parseKwargs(config_output)

    # Build handler object
    output_handler = output_handler_class(**kwargs)

    return output_handler

class OutputHandler(object):
    """The base class for handling the output for writing a Piff model.

    This is essentially an abstract base class intended to define the methods that should be
    implemented by any derived class.
    """
    @classmethod
    def parseKwargs(cls, config_output):
        """Parse the output field of a configuration dict and return the kwargs to use for
        initializing an instance of the class.

        The base class implementation just returns the kwargs as they are, but derived classes
        might want to override this if they need to do something more sophisticated with them.

        :param config_output:    The output field of the configuration dict, config['output']

        :returns: a kwargs dict to pass to the initializer
        """
        return config_output

    def write(self, psf):
        """Write a PSF object to the output file.
        """
        raise NotImplemented("Derived classes must define the write function")

    def read(self):
        """Read a PSF object that was written to an output file back in.

        :returns: a piff.PSF instance
        """
        raise NotImplemented("Derived classes must define the read function")


class OutputFile(OutputHandler):
    """An OutputHandler that just writes to a FITS file.

    :param file_name:   The file name to write the data to.
    """
    def __init__(self, file_name):
        self.file_name = file_name


    def write(self, psf):
        """Write a PSF object to the output file.
        """
        open(self.file_name, 'w').write(str(psf))

    def read(self):
        """Read a PSF object that was written to an output file back in.

        :returns: a piff.PSF instance
        """
        pass

