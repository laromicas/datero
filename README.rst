::

       .___       __
     __| _/____ _/  |_  ___________  ____
    / __ |\__  \\   __\/ __ \_  __ \/  _ \
   / /_/ | / __ \|  | \  ___/|  | \(  <_> )
   \____ |(____  /__|  \___  >__|   \____/
        \/     \/          \/

Datero
======

Datero is a WIP Python command line tool to download and organize your Dat Roms.
As today the tool supports dat-omatic, redump, and translated-english dats.
It merges all the dats in a tree folder structure thought to use with Emulators rather than dats.
The dat file format must be compatible with `ROMVault <https://www.romvault.com/>`__.

Installation
------------

Use pip or download a release and install it (recommended to use a virtual environment):

.. code-block:: bash

   pip install datero
   pip install datero-0.3.0-py3-none-any.whl

Usage
-----

.. code-block:: bash

   # Show help
   $ datero --help

   # List installed seeds
   $ datero list

   # Doctor the seeds installation
   $ datero doctor [seed]

   # List available seeds
   $ datero seed available

   # Seed install
   $ datero seed install [seed] [--repository REPOSITORY] [--branch BRANCH]

   # Seed remove
   $ datero seed remove [seed]

   # Seed commands
   $ datero [seed] {--fetch|--process} [--filter FILTER]

   optional arguments:
      -h, --help            show the help message and exit, feel free to append to other commands
      -v, --verbose         verbose output
      -q, --quiet           quiet output

How to Build
-----

.. code-block:: bash

   # Install build
   $ pip install build

   # Build
   $ python -m build


Posible Issues
--------------

Be careful when updating dats from datomatic, sometimes they put a captcha, and you may be banned if the captcha fails, captcha support is OTW.


TODO (without priority)
-----------------------

-  Database initialization !!! (priority)

    -  Command to populate DB with initial data

-  Make update rules write to database only when finished
-  Better rules update process
-  Logging
-  Option to disable dat seeds
-  Tests
-  More dat repositories
-  Show updated
-  Mega.nz download support (https://pypi.org/project/mega.py/)
-  Move helpers out from commands
-  Configurable folder structure (instead of emulator-focused structure use dat-repositories or viceversa)

   -  Maybe with a builder, to avoid the need to change the code

-  Commenting datero.ini
-  Modular design for repositories (done for seeds, repositores missing)
-  Don't update when same filename *
-  Option to disable individual dats *
-  Better structure for the downloaders *
-  Better command line support

*(\*) Done but to be improved*

*(\*\*) Did it Yay!!!*



WISHLIST (without priority)
---------------------------

-  Modular design for dat seeds (**)
-  Dat structure for ClrMamePro or another dat manager.
-  Web interface
-  Download from central repositories (an S3 or something like that to prevent overload main sites)
   -  Lambda to download dats and upload to S3
   -  Downloading from S3
-  Auto-Import MIA Lists (for redump)
   -  Add [MIA] to dat roms
-  Deduplicate dats
-  Remove MIA from dats
-  .cue Generator

*(\*\*) Did it Yay!!!*


Contributing
------------

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

License
-------

`MIT <https://choosealicense.com/licenses/mit/>`__

