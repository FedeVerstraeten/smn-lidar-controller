#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smnar-lidar-controller",
    version="0.0.1",
    author="Federico Verstraeten",
    description="SMN Argentina LICEL controller",
    long_description="A controller for 'Servicio Meteorológico Nacional de Argentina (Argentine National Meteorological Service)' LIDAR system using LICEL (Lidar Transient Recorder)",
    long_description_content_type="text/markdown",
    url="https://github.com/FedeVerstraeten/smnar-licel-controller",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)