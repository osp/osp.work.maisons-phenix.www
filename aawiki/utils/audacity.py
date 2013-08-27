import re
from timecodes import ms2tc, tc2ms


TIME_RE = r'(\d?\d:)?(\d\d):(\d\d)([,.]\d{1,3})?'
TIMECODE_RE = r'(?P<begin>%(TIME_RE)s)[ \t]*-->([ \t]*(?P<end>%(TIME_RE)s))?' % {'TIME_RE': TIME_RE}


pattern = re.compile(TIMECODE_RE)


def srt2audacity(txt):
    """
    >>> data = '''00:01:30,610 --> 
    ... <BLANKLINE>
    ... first section
    ... <BLANKLINE>
    ... 00:05:45,272 --> 
    ... <BLANKLINE>
    ... second section'''
    >>> print(srt2audacity(data).strip())
    90,610022  90,610022   first section
    345,271874  345,271874 second section

    >>> data = '''00:01:30,610 --> 
    ... <BLANKLINE>
    ... first section
    ... <BLANKLINE>
    ... 00:05:45,272 --> 00:08:32,574
    ... <BLANKLINE>
    ... second section'''
    >>> print(srt2audacity(data).strip())
    90,610022  345,271874   first section
    345,271874  512,573912 second section

    >>> data = '''00:01:30,610 --> 00:05:45,272
    ... <BLANKLINE>
    ... first section
    ... <BLANKLINE>
    ... 00:05:45,272 --> 00:08:32,574
    ... <BLANKLINE>
    ... second section'''
    >>> print(srt2audacity(data).strip())
    90,610022  345,271874   first section
    345,271874  512,573912 second section

    >>> data = '''00:01:30,610 --> 00:05:45,272
    ... <BLANKLINE>
    ... first section
    ... <BLANKLINE>
    ... 00:05:45,272 --> 00:08:32,574
    ... <BLANKLINE>
    ... second section'''
    >>> print(srt2audacity(data).strip())
    90,610022  345,271874   first section
    345,271874  512,573912
    """
    def srt_parser(txt):
        matches = pattern.finditer(txt)

        match = matches.next()
        begin = match.group('begin')
        end = match.group('end')
        index = match.end() 

        for match in matches:
            body = txt[index:match.start()].strip('\n')
            yield dict(begin=begin, end=end, body=body)

            begin = match.group('begin')
            end = match.group('end')
            index = match.end() 

        body = txt[index:].strip('\n')
        yield dict(begin=begin, end=end, body=body)


    def srt_formater(txt):
        force_endtime = True
        stack = []

        for t in srt_parser(txt):
            begin = tc2ms(t['begin']) / 1000.0
            end = tc2ms(t['end']) / 1000.0 if t['end'] else None
            body = t['body'].strip('\n').replace('\n', r'\n')

            # If previous end hasn't been set
            # sets it to the current begin timecode
            if len(stack) and stack[-1]['end'] == '':
                stack[-1]['end'] = begin

            stack.append({
                'begin': begin,
                'end': end,
                'body': body,
            })

        template = u"{e[begin]}\t{e[end]}\t{e[body]}\n"
        return u"".join([template.format(e=e) for e in stack])

    return srt_formater(txt)


def audacity_to_srt(data, explicit=False):
    """
    >>> data = '''90,610022  90,610022   first section
    ... 345,271874  345,271874 second section'''
    >>> print(audacity_to_srt(data).strip())
    00:01:30,610 --> 
    <BLANKLINE>
    first section
    <BLANKLINE>
    00:05:45,272 --> 
    <BLANKLINE>
    second section

    >>> data = '''90,610022  345,271874   first section
    ... 345,271874  512,573912 second section'''
    >>> print(audacity_to_srt(data).strip())
    00:01:30,610 --> 
    <BLANKLINE>
    first section
    <BLANKLINE>
    00:05:45,272 --> 00:08:32,574
    <BLANKLINE>
    second section

    >>> data = '''90,610022  345,271874   first section
    ... 345,271874  512,573912 second section'''
    >>> print(audacity_to_srt(data, explicit=True).strip())
    00:01:30,610 --> 00:05:45,272
    <BLANKLINE>
    first section
    <BLANKLINE>
    00:05:45,272 --> 00:08:32,574
    <BLANKLINE>
    second section
    """
    stack = []

    for line in data.splitlines():
        try:
            (start, end, body) = tuple(line.split(None, 2))
        except ValueError:
            try:
                # A marker without label
                (start, end) = tuple(line.split(None, 1))
                body = ""
            except ValueError:
                # A blank line? Get lost!
                break

        start = float(start.replace(',', '.'))
        end = float(end.replace(',', '.'))

        #start = timecode_fromsecs(start, alwaysfract=True, alwayshours=True, fractdelim=',')
        #end = timecode_fromsecs(end, alwaysfract=True, alwayshours=True, fractdelim=',')
        start = ms2tc(start / 1000)
        end = ms2tc(end / 1000)

        # If the end time equals the start time we ommit it.
        if end == start:
            end = ""

        if not explicit:
            # Deletes previous end time if equal to actual start time
            if len(stack) and stack[-1]['end'] == start:
                stack[-1]['end'] = ""

        body = body.replace(r'\n', '\n')

        stack.append({'start': start, 'end': end, 'body': body})

    template = "{e[start]} --> {e[end]}\n\n{e[body]}\n\n"
    return "".join([template.format(e=e) for e in stack])


if __name__ == "__main__":
    import doctest
    doctest.testmod()
