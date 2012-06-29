Introduction
============
Skal is a wrapper for the argparser library to make it easier to write
applications that uses the command-subcommand style, much like git and
heroku.

Basic Usage
===========
Skal can be used on three levels: *class*, *module* and *package*. As this
project is still very young only the class level is implemented as for now.

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
    app = MyApp()
    sys.exit(app.run())
```

Running the small program:
```
> python myapp.py hello
hello

> python myapp.py yes
yes
```

Using Custom Arguments
======================
*Note: this is not yet implemented!*

This shows the future usage of custom arguments per subcommand:
```python
from skal import SkalApp, command, arguments

class MyApp(SkalApp):
    """Application description"""

    __skal__ = {
        '-a': {'help': 'Help for a'},
        '-b': {'help': 'Help for b'}
    }

    @command
    @arguments({
        ('-d', '--delete'): {'help': 'Help for d'}
    })
    def hello(self):
        """Help line for hello"""
        if (self.args.a):
            print('a')
        if (self.args.b):
            print('b')
        if (self.args.delete):
            print('deleting')
        print('hello')

    @default
    @command
    def yes(self):
        """Help line for yes"""
        if (self.args.a):
            print('a')
        if (self.args.b):
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

