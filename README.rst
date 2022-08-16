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

   pip install -r requirements.txt

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
----

-  Don't update when same filename
-  Tests
-  More dat repositories
-  Show updated
-  Mega.nz download support (https://pypi.org/project/mega.py/)
-  Better structure for the downloaders
-  Main command line executable for easy executions
-  Pip installer
-  Refactor repos to dat seeds
-  Removing unneeded dependencies
-  Modular design for dat repositories (TBD)
-  Option to disable repositories
-  Option to disable individual dats
-  Configurable folder structure (instead of emulator-focused structure use dat-repositories or viceversa)
-  Dat structure for ClrMamePro or another dat manager (TBD).
-  Web interface (TBD)
-  Download from central repositories (an S3 or something like that to prevent overload main sites) (TBD)
   -  Lambda to download dats and upload to S3
   -  Downloading from S3
-  Auto-Import MIA Lists (TBD)

Contributing
------------

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.

License
-------

`MIT <https://choosealicense.com/licenses/mit/>`__




=HYPERLINK(H11,H11)
=HYPERLINK(H11,IMAGE(H11))
=ENCODEURL(LOWER(B11))
= https://scryfall.com/search?q=&G11&&unique=cards&as=grid&order=name
="https://api.scryfall.com/cards/named?exact="&J11&"&format=image"


function MTG_IMAGE(input) {
  encoded = encodeURIComponent(input.toLowerCase());
  url = "https://scryfall.com/search?q=" + encoded + "&unique=cards&as=grid&order=name"
  img_url = "https://api.scryfall.com/cards/named?exact=" + encoded + "&format=image"
  link = HYPERLINK(url, url)
  img_link = HYPERLINK(img_url, IMAGE(img_url))
  return img_link
}

var ss = SpreadsheetApp.getActiveSpreadsheet();
var sheet = ss.getSheets()[0];

var cell = sheet.getRange("B5");
cell.setFormula("=SUM(B3:B4)");