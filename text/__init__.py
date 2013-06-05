# -*- coding: utf-8 -*-

import unicodedata
from .format_string_to_fit_in_n_chars import squeeze_sms_message, format_string_to_fit_in_n_chars
from ec2HostnameToIp import ec2HostnameToIp
from split import splitString
from . import case

def ensureAscii(text):
    if type(text) == unicode:
        encodedText = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')
    else:
        encodedText = text

    return encodedText


def stringify(obj):
    """Convert any numeric elements to strings."""
    if type(obj) is dict:
        for k, v in list(obj.items()):
            obj[stringify(k)] = stringify(v)
    elif type(obj) is list:
        return map(stringify, obj)
    elif type(obj) is int or type(obj) is long:
        return str(obj)
    return obj


__all__ = [
    'ec2HostnameToIp',
    'squeeze_sms_message',
    'format_string_to_fit_in_n_chars',
    'ensureAscii',
    'splitString',
    'case',
    'stringify',
]

