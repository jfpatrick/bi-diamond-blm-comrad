"""
setup.py for bi-diamond-blm-comrad.

For reference see
https://packaging.python.org/guides/distributing-packages-using-setuptools/

"""
from pathlib import Path
from setuptools import setup, find_packages


HERE = Path(__file__).parent.absolute()
with (HERE / 'README.md').open('rt') as fh:
    LONG_DESCRIPTION = fh.read().strip()


REQUIREMENTS: dict = {
    'core': [
        'comrad'
    ],
    'test': [
        'pytest',
		'comrad'
    ],
    'dev': [
        'comrad'
    ],
    'doc': [
        'sphinx',
        'acc-py-sphinx',
    ],
}


setup(
    name='bi-diamond-blm-comrad',
    version="0.0.1.dev0",

    author='martinja',
    author_email='javier.martinez.samblas@cern.ch',
    description='ComRAD project for the GUIs of the BI-DIAMOND-BLM devices.',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='',

    packages=find_packages(),
    python_requires='~=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],

    install_requires=REQUIREMENTS['core'],
    extras_require={
        **REQUIREMENTS,
        # The 'dev' extra is the union of 'test' and 'doc', with an option
        # to have explicit development dependencies listed.
        'dev': [req
                for extra in ['dev', 'test', 'doc']
                for req in REQUIREMENTS.get(extra, [])],
        # The 'all' extra is the union of all requirements.
        'all': [req for reqs in REQUIREMENTS.values() for req in reqs],
    },
)
