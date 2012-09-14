Skal Changelog
==============

Skal follows the Semantic Versioning standard, although not for development
before version 1. Read more at http://semvar.org


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
