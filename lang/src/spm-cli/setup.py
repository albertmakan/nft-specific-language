from setuptools import setup, find_packages

setup(
    name="spm-cli",
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'Click', 'starkbank-ecdsa'
    ],
    entry_points='''
        [console_scripts]
        spm=spmcli.cli:cli
    ''',
)
