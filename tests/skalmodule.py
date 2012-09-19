"""main help string

more help here
"""


from skal import command


__args__ = {
    '-b': {'help': 'bool argument', 'action': 'store_true'},
    ('-s', '--string'): {'help': 'string argument with long name'}
}


@command
def first(**args):
    """first command"""
    print('first')
    if 'b' in args:
        print('b')
    if 'string' in args:
        print(args['string'])


def second(**args):
    """second command"""
    print('second')


@command({
    '-i': {'help': 'bool argument', 'action': 'store_true'},
    ('-t', '--test'): {'help': 'string argument with long name'}
})
def third(**args):
    """third command"""
    print('third')
    if 'i' in args:
        print('i')
    if 'test' in args:
        print(args['test'])


@command
def no_doc(**args):
    print('there are no docs for this function')


@command
def ctrlc(**args):
    """ctrl c test"""
    raise KeyboardInterrupt
