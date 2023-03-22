from setuptools import setup
import os


setup(
    name='spm_tool',
    version='0.1',
    install_requires=[
        f"{pack} @ file://localhost/{os.getcwd()}/lang/src/{pack}/" 
        for pack in ['spm', 'spmgen', 'spm-cli', 'spl', 'splgen', 'spl-cli']
    ],
)
