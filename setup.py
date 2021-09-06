from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'SolarWattEnergyManagerAPI',
  packages = ['SolarWattEnergyManagerAPI'],
  version = '0.5',
  license='MIT',
  description = 'API wrapper for solar watt energy manager',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Sebastian Wallat',
  author_email = 'wallatsebastian@gmail.com',
  url = 'https://github.com/SebastianWallat/SolarWattEnergyManagerAPI',
  download_url = 'https://github.com/SebastianWallat/SolarWattEnergyManagerAPI/archive/v_05.tar.gz',
  keywords = ['IOT', 'Solar', 'Local'],
  install_requires=[
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)