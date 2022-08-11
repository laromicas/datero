# Datero
Datero is a WIP Python command line tool to download and organize your Dat Roms.
As today the tool supports dat-omatic, redump, and translated-english dats.
It merges all the dats in a tree folder structure thought to use with Emulators rather than dats.

## Installation
<!--- ### TODO
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.
```bash
pip install foobar
```
-->

Download a release and install requirements (recommended to use a virtual environment)
```bash
pip install -r requirements.txt
```


## Usage

```bash
# fill the json database with initial data
$ ./seed

# Download dats to tmp folder
$ lib/repos/<dattype>/update -f
$ lib/repos/nointro/update -f

# process dats and organize them
lib/repos/<dattype>/update -p

# process dats filtered by word
lib/repos/<dattype>/update -p -d <filter>
```

## Posible Issues

Be careful when updating dats from datomatic, sometimes they put a captcha, and you may be banned if the captcha fails, captcha support is OTW

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.


## License

[MIT](https://choosealicense.com/licenses/mit/)
