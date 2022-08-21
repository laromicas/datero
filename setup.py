import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='datero',
    version='0.3.0',
    description='Python command line tool to download and organize your Dat Roms.',
    long_description=open('README.rst').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/laromicas/datero',
    author='Lacides Miranda',
    author_email='laromicas@hotmail.com',
    license='MIT License',
    packages=['datero'],
    include_package_data=True,
    install_requires=[
                    'tinydb==4.7.0',
                    'pydantic==1.9.2',
                    'python-dateutil==2.8.2',
                    'xmltodict==0.13.0',
                    'internetarchive==3.0.2',
                    'typing_extensions==4.3.0',

                    'six==1.16.0',
                    'certifi==2022.6.15',
                    'charset-normalizer==2.1.1',
                    'contextlib2==21.6.0',
                    'docopt==0.6.2',
                    'idna==3.3',
                    'jsonpatch==1.32',
                    'jsonpointer==2.3',
                    'requests==2.28.1',
                    'schema==0.7.5',
                    'tqdm==4.64.0',
                    'urllib3==1.26.11',
                    ],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: System :: Emulators',
    ],
    entry_points={
        "console_scripts": [
            "datero=datero.__main__:main",
        ]
    },
)
