r"""
Listing Sage packages

This module can be used to see which Sage packages are installed
and which packages are available for installation.

For more information about creating Sage packages, see
the "Packaging Third-Party Code" section of the
Sage Developer's Guide.

Actually installing the packages should be done via the command
line, using the following commands:

- ``sage -i PACKAGE_NAME`` -- install the given package

- ``sage -f PACKAGE_NAME`` -- re-install the given package, even if it
  was already installed
  
Packages available
------------------

**Standard packages:**

{STANDARD_PACKAGES}

**Optional packages:**

{OPTIONAL_PACKAGES}

**Experimental packages:**

{EXPERIMENTAL_PACKAGES}

Functions
---------
"""

#*****************************************************************************
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************
        
import os

def is_package_installed(package):
    """
    Return False in sage-on-gentoo.
    """
    return False

class PackageNotFoundError(RuntimeError):
    """
    This class defines the exception that should be raised when a
    function, method, or class cannot detect a Sage package that it
    depends on.

    This exception should be raised with a single argument, namely
    the name of the package.

    When an ``PackageNotFoundError`` is raised, this means one of the
    following:

    - The required optional package is not installed.

    - The required optional package is installed, but the relevant
      interface to that package is unable to detect the package.

    EXAMPLES::

        sage: from sage.misc.package import PackageNotFoundError
        sage: raise PackageNotFoundError("my_package")
        Traceback (most recent call last):
        ...
        PackageNotFoundError: the package 'my_package' was not found. It may or may not be available in portage
    """
    def __str__(self):
        """
        Return the actual error message.

        EXAMPLES::

            sage: from sage.misc.package import PackageNotFoundError
            sage: str(PackageNotFoundError("my_package"))
            "the package 'my_package' was not found. It may or may not be available in portage"
        """
        return ("the package {0!r} was not found. "
            "It may or may not be available in portage"
            .format(self.args[0]))
