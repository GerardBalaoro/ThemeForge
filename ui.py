"""Console Output Helpers
"""
import terminaltables as tb

def banner(text, table=tb.DoubleTable, end='\n', align=['center'], padding=1):
    _banner = table([[text]])
    _banner.inner_heading_row_border = False
    _banner.inner_row_border = True
    _banner.padding_left = padding
    _banner.padding_right = padding
    for i, v in enumerate(align):
        _banner.justify_columns[i] = v
        
    return print(_banner.table, end=end)

def table(data, table=tb.DoubleTable, end='\n', align=['center'], padding=1):
    _table = table(data)
    _table.padding_left = padding
    _table.padding_right = padding
    for i, v in enumerate(align):
        _table.justify_columns[i] = v
        
    return print(_table.table, end=end)

def line(message, end='\n', pre=''):
    return print(pre + message, end=end)

def title():
    table([
        ['THEMEFORGE'],
        ['Theme Compiler for Android-Based Operating Systems'],
        ['by: Gerard Balaoro']
    ])

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
    if isinstance(contents, str):
        contents = contents.split('\n')

    size = len(max(title, max(contents, key=len), len))

    lines.append()

