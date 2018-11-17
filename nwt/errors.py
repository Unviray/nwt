# -*- coding: utf-8 -*-
"""
    nwt.errors
    ----------

    Contains NwtError and a few subclasses (in an extra module to avoid
    circular import problems).
"""

class NwtError(Exception):
    """
    Base class for Nwt errors.

    This is the base class for "nice" exceptions. When such an exception is
    raised. Nwt will abort the build and present the exception category and
    message to the user.

    Extensions are encouraged to derive from this exception for their custom
    errors.

    .. attribute:: category

       Description of the exception "category", used in converting the
       exception to a string ("category: message").  Should be set accordingly
       in subclasses.
    """
    category = 'Nwt error'


class NwtWarning(NwtError):
    """
    Warning, treated as error.
    """
    category = 'Nwt error'


class ConfigError(NwtError):
    """
    Configuration error.
    """
    category = 'Configuration error'


class InputError(NwtError):
    """
    User input error.
    """
    category = 'Input error'
