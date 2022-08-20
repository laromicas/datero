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
The dat structure is compatible with `ROMVault <https://www.romvault.com/>`__.

Installation
------------

Download the code and install requirements (recommended to use a virtual
environment)

.. code-block:: bash

   $ pip install -r requirements.txt

Usage
-----

.. code-block:: bash

   # fill the json database with initial data
   $ ./seed

   # Download dats to tmp folder
   $ lib/repos/<dattype>/update -f
   # e.g.
   $ lib/repos/nointro/update -f

   # process dats and organize them
   lib/repos/<dattype>/update -p

   # process dats filtered by word
   lib/repos/<dattype>/update -p -d <filter>

Posible Issues
--------------

Be careful when updating dats from datomatic, sometimes they put a captcha, and you may be banned if the captcha fails, captcha support is OTW.

TODO (without priority)
-----------------------

-  Don't update when same filename *
-  Option to disable individual dats *
-  Option to disable dat seeds
-  Refactor repos to dat seeds
-  Tests
-  More dat repositories
-  Show updated
-  Mega.nz download support (https://pypi.org/project/mega.py/)
-  Better structure for the downloaders
-  Main command line executable for easy executions
-  Pip installer
-  Removing unneeded dependencies
-  Configurable folder structure (instead of emulator-focused structure use dat-repositories or viceversa)
-  database setup

*(\*) Done but to be improved*



WISHLIST (without priority)
---------------------------

-  Modular design for dat seeds
-  Dat structure for ClrMamePro or another dat manager.
-  Web interface
-  Download from central repositories (an S3 or something like that to prevent overload main sites)
   -  Lambda to download dats and upload to S3
   -  Downloading from S3
-  Auto-Import MIA Lists (for redump)
   -  Add [MIA] to dat roms
-  Deduplicate dats
-  Remove MIA from dats



Contributing
------------

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

License
-------

`MIT <https://choosealicense.com/licenses/mit/>`__

