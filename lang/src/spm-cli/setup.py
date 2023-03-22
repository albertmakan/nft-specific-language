from setuptools import setup

setup(
    name="spm-cli",
    version='0.0.1',
    py_modules=['spmcli.cli'],
    install_requires=[
        'Click', 'starkbank-ecdsa'
    ],
    entry_points='''
        [console_scripts]
        spm=spmcli.cli:cli
    ''',
)
