"""main help string"""


from skal import command


__args__ = {
    '-b': {'help': 'bool argument', 'action': 'store_true'},
    ('-s', '--string'): {'help': 'string argument with long name'}
}


@command
def first(args):
    """first command"""
    print('first')
    if args.b:
        print('b')
    if args.string:
        print(args.string)


def second(args):
    """second command"""
    print('second')


@command({
    '-i': {'help': 'bool argument', 'action': 'store_true'},
    ('-t', '--test'): {'help': 'string argument with long name'}
})
def third(args):
    """third command"""
    print('third')
    if args.i:
        print('i')
    if args.test:
        print(args.test)


@command
def ctrlc(args):
    """ctrl c test"""
    raise KeyboardInterrupt
