from setuptools import setup

setup(
    name="spm-cli",
    version='0.0.1',
    py_modules=['cli'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        spm-cli=cli:cli
    ''',
)
