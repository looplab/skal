Introduction
============
Skal is a wrapper for the argparser library to make it easier to write
applications that uses commands with subcommands, much like git and
heroku does.

Skal can be used with different combinations of command sources; a subclass of
SkalApp, any number of modules and any number of packages. Currently usage with
classes and modules are supported.

The test cases are a good source of different ways to use Skal appart
from what is described here.

Subclass as command source
==========================
A custom subclass of SkalApp is one way to get some commands added, and
may be the shortest version.

In file myapp.py:
```python
from skal import SkalApp, command

class MyApp(SkalApp):
    @command
    def hello(self):
        print('hello')

    @command
    def yes(self):
        print('yes')

if __name__ == '__main__':
    MyApp().run()
```

Running the program:
```
> python myapp.py hello
hello

> python myapp.py yes
yes
```

Modules as command source
=========================
There are two ways in which modules can be used to source commands;
either as a flat hirearchy where every function in every module gets
added or with a bit of hirearchy where each module becomes a command and
its functions becomes subcommands. Using either is determined by how the
module names are passed to the SkalApp constructor, and any combination
is also valid. The only advice is to specify a overridden version and
description string for the whole app, as Skal wouldn't otherwise know
where to get that information from. When using only modules there is no
need to override the SkalApp class.

First a module called do.py:
```python
from skal import command

@command
def hello(self):
    print('hello')

@command
def yes(self):
    print('yes')
```

Using do.py as plain commands in myapp.py:
```
from skal import SkalApp

if __name__ == '__main__':
    SkalApp(command_modules = ['do']).run()
```

Running the program:
```
> python myapp.py hello
hello

> python myapp.py yes
yes
```

Using do.py as a subcommand in myapp.py:
```
from skal import SkalApp

if __name__ == '__main__':
    SkalApp(subcommand_modules = ['do']).run()
```

Running the program:
```
> python myapp.py do hello
hello

> python myapp.py do yes
yes
```

Per Command Arguments
======================
This shows the usage of custom arguments per command. This works for all
supported command sources, not only classes.
```python
from skal import SkalApp, command, default

class MyApp(SkalApp):
    """Help line for application"""

    __args__ = {
        '-a': {'help': 'Help for a', 'action': 'store_true'},
        '-b': {'help': 'Help for b', 'action': 'store_true'}
    }

    @command({
        ('-d', '--delete'): {'help': 'Help for d', 'action': 'store_true'}
    })
    def hello(self):
        """Help line for hello"""
        if self.args.a:
            print('a')
        if self.args.b:
            print('b')
        if self.args.delete:
            print('deleting')
        print('hello')

    @command
    def yes(self):
        """Help line for yes"""
        if self.args.a:
            print('a')
        if self.args.b:
            print('b')
        print('yes')

if __name__ == '__main__':
    app = MyApp()
    sys.exit(app.run())
```

Running it:
```
> python myapp.py -a hello --delete
a
deleting
hello

> python myapp.py -b yes
b
yes
```

License
=======
Skal is licensed under Apache License 2.0

http://www.apache.org/licenses/LICENSE-2.0

