Skal Changelog
==============

Skal follows the Semantic Versioning standard, although not for development
before version 1. Read more at http://semvar.org


Version 0.1.13
-------------

Released on January 22nd 2013

- Package restructuring


Version 0.1.12
-------------

Released on January 21st 2013

- Print error output in a clearer way


Version 0.1.11
-------------

Released on November 8nd 2012

- Fixes a bug where ImportErrors in modules are captured as a Skal error


Version 0.1.10
-------------

Released on October 2nd 2012

- Added ability to send global args with the constructor


Version 0.1.9
-------------

Released on September 21th 2012

- Fixes a bug when importing non existing modules


Version 0.1.8
-------------

Released on September 21th 2012

- Fixes a bug when modules inside of modules are used


Version 0.1.7
-------------

Released on September 19th 2012

- Fixes a bug where long command help was incorrectly formated
- Change argument passing to commands to use unpacking
- Change to the order in which version and description is set
- Fix a bug where no doc on a sub class method crashes the app


Version 0.1.6
-------------

Released on September 18th 2012

- Correctly skip and add modules


Version 0.1.5
-------------

Released on September 18th 2012

- Generate correct name for commands from modules inside packages
- Catch NameError and not only SyntaxError on module import


Version 0.1.4
-------------

Released on September 18th 2012

- Duplicate commands from different modules are now ignored and warned for
- Better output of missing documentation and syntax error in commands


Version 0.1.3
-------------

Released on September 14th 2012

- Fixed bug when no documentation was defined for a function
- Code is now completely PEP8 comliant


Version 0.1.2
-------------

Released on September 7th 2012

- Changed the class init to accept command modules AND subcommand modules
- Added override for description and version in SkalApp constructor


Version 0.1.1
-------------

Released on September 5th 2012

- Removed returning of exit codes
- Removed catching of KeyboardInterrupt
- Chenged to use distribute (setuptools)
- Added elaborate test cases for testing class, module and package versions
- Added better handling of version flag
- Moved output capture for testing to a separate utility class
- Added module introspection for functions and global args


Version 0.1.0
-------------

Released on July 3rd 2012

- First major release of Skal
- Updated setup to use a cfg file, this is also used for tests


Version 0.0.4
-------------

Released on July 1st 2012

- Added command arguments
- Updated readme with new syntax


Version 0.0.3
-------------

Released on June 29th 2012

- Added global arguments
- Added class documentation


Version 0.0.2
-------------

Released on June 28th 2012

- Added this changelog
- Added test cases
- Module can't be run on it's own anymore


Version 0.0.1
-------------

Released on June 27th 2012

- First release
- Basic functionality with a subclass of SkalApp
- Decorator to mark commands to add to command line
