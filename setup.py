#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='python-wrapper',
      version='0.0.1',
      description='This package provision K8 Cluster on different cloud providers',
      author='Anuj Jain',
      author_email='anuj2jain@gmail.com',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),

      )
