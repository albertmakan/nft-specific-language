from setuptools import setup, find_packages

setup(
    name="spl-cli",
    version='0.0.1',
    packages=find_packages(),
    package_data={"splcli": ["templates/*"]},
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        spl=splcli.cli:cli
    ''',
)
