"""Console Output Helpers
"""
import sys

class ProgressBar:

    def __init__(self, total=100, length=25, fill='#'):
        self.total = total
        self.length = length
        self.fill = fill

    def update(self, label, value):
        progress = value / self.total
        blocks = int(round(self.length * progress))
        msg = "\r{0}: [{1}] {2}%".format(label, self.fill * blocks + "-" * (self.length - blocks), round(progress * 100, 2))
        if progress >= 1: msg += " DONE\r\n"
        sys.stdout.write(msg)
        sys.stdout.flush()

def line(message, end='\n', pre=''):
    return print(pre + message, end=end)

def title():
    block('Theme Compiler for Android-Based Operating Systems\n'
        'by: Gerard Balaoro',
        title='THEMEFORGE')

def block(contents, title='', padding=1):
    hline = chr(9552)
    vline = chr(9553)
    cor_ur = chr(9559)
    cor_ul = chr(9556)
    cor_dr = chr(9565)
    cor_dl = chr(9562)
    cor_mr = chr(9571)
    cor_ml = chr(9568)

    lines = []
    if not isinstance(contents, list):
        contents = str(contents)
        contents = contents.split('\n')

    def mkline(text, size, l, r):
        return l + text.center(size) + r

    size = len(max(title, max(contents, key=len), key=len)) + padding * 2

    lines.append(mkline(hline * size, size, cor_ul, cor_ur))

    if len(title):
        lines.append(mkline(title, size, vline, vline))
        lines.append(mkline(hline * size, size, cor_ml, cor_mr))

    for line in contents:
        lines.append(mkline(line, size, vline, vline))
        
    lines.append(mkline(hline * size, size, cor_dl, cor_dr))
    print('\n'.join(lines))


