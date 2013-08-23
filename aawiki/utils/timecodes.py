#https://github.com/louissobel/srt.py/blob/master/srt.py
#https://github.com/riobard/srt.py


import re


def tc2ms(tc):
    '''
    converts timecode to millisecond

    >>> tc2ms('12:34:56,789')
    >>> tc2ms('01:02:03,004')
    >>> tc2ms('1:2:3,4')
    >>> tc2ms(',4')
    >>> tc2ms('3')
    >>> tc2ms('3,4')
    >>> tc2ms('1:2')
    >>> tc2ms('1:2,3')
    >>> tc2ms('1:2:3')
    
    also accept "." instead of "," as millsecond separator
    '''
    sign    = 1
    if tc[0] in "+-":
        sign    = -1 if tc[0] == "-" else 1
        tc  = tc[1:]

    TIMECODE_RE     = re.compile('(?:(?:(?:(\d?\d):)?(\d?\d):)?(\d?\d))?(?:[,.](\d?\d?\d))?')
    match   = TIMECODE_RE.match(tc)
    if not match:
        raise ValueError
    hh, mm, ss, ms = (int(x or 0) for x in match.groups())
    return ((hh * 3600 + mm * 60 + ss) * 1000 + ms) * sign


def ms2tc(ms, fract=True, always_fract=False, fract_delim=',', always_hours=False):
    '''
    converts millisecond to timecode
    
    returns a string in HH:MM:SS[.xxx] notation if fract is True, uses .xxx if
    either necessary (non-zero) OR alwaysfract is True

    >>> ms = (1000 * 60) + 123
    >>> ms2tc(ms)
    '01:00,123'
    >>> ms2tc(ms, always_hours=True)
    '00:01:00,123'
    >>> ms2tc(ms, fract_delim='.')
    '01:00.123'
    >>> ms2tc(ms, fract=False)
    '01:00'

    >>> ms = (1000 * 60)
    >>> ms2tc(ms, always_fract=True)
    '01:00,000'
    '''
    sign    = '-' if ms < 0 else ''
    ms      = abs(ms)
    ss, ms  = divmod(ms, 1000)
    hh, ss  = divmod(ss, 3600)
    mm, ss  = divmod(ss, 60)

    tc = '%s' % sign

    if hh or always_hours:
        tc += '%02d:' % hh

    tc += '%02d:%02d' % (mm, ss)

    if (ms and fract) or always_fract:
        tc += '%s%03d' % (fract_delim, ms)

    return tc


if __name__ == "__main__":
    import doctest
    doctest.testmod()
