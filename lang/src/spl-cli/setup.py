from setuptools import setup

setup(
    name="spl-cli",
    version='0.0.1',
    py_modules=['splcli.cli'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        spl=splcli.cli:cli
    ''',
)
