#!/usr/bin/env python
from setuptools import setup
import subprocess

try:
    subprocess.call(['conda','install','--file','requirements.txt'])
except Exception:
    pass

setup(name='pyOpticalFlow',
	  description='Pure Python optical flow with Horn Schunck and Lucas Kanade',
	  url='https://github.com/scienceopen/Optical-Flow-LucasKanade-HornSchunck',
	  install_requires=['pathlib2'],
      packages=['pyOpticalFlow'],
	  )
