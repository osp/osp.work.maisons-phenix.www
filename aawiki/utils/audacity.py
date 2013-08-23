import re
from timecodes import ms2tc, tc2ms

TIME_RE = r'(\d?\d:)?(\d\d):(\d\d)([,.]\d{1,3})?'
TIMECODE_RE = r'(?P<begin>%(TIME_RE)s)[ \t]*-->([ \t]*(?P<end>%(TIME_RE)s))?' % {'TIME_RE': TIME_RE}
pattern = re.compile(TIMECODE_RE)


def srt2audacity(txt):
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
            if force_endtime:
                if len(stack) and stack[-1]['end'] == '':
                    stack[-1]['end'] = tc2ms(t['begin'])
                end = tc2ms(t['end']) if t['end'] else ''
            else:
                end = tc2ms(t['end']) if t['end'] else tc2ms(t['begin'])

            stack.append({
                'begin': tc2ms(t['begin']),
                'end': end,
                'body': t['body'].strip('\n').replace('\n', r'\n'),
            })

        template = u"{e[begin]}\t{e[end]}\t{e[body]}\n"
        return u"".join([template.format(e=e) for e in stack])

    return srt_formater(txt)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
