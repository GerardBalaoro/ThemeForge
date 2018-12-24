"""Console Output Helpers
"""
import terminaltables as tb
import console

text = {
    'normal': console.fg.default + console.bg.default,
    'warn': console.fg.yellow,
    'info': console.fg.blue,
    'error': console.fg.red,
    'success': console.fg.green
}

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

def line(message, end='\n', type='normal', pre=''):
    global text
    return print(pre + text[type](message), end=end)

def title():
     ui.table([
        ['THEMEFORGE'],
        [ui.text['info']('Theme Compiler for Android-Based Operating Systems')],
        ['by: Gerard Balaoro']
    ])