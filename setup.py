from setuptools import setup

# read the contents of your README file
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='LocalSolarWatt',
    packages=['LocalSolarWatt'],
    version='0.6',
    license='MIT',
    description='python api wrapper for solar watt devices',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='AlgorithmicEntropy',
    url='https://github.com/AlgorithmicEntropy/SolarWattEnergyManagerAPI',
    download_url='https://github.com/SebastianWallat/SolarWattEnergyManagerAPI/archive/v_06.tar.gz',
    keywords=['IOT', 'Solar', 'Local'],
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
    ],
)
