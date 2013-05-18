# -*- coding: utf-8 -*-

import os
import setuptools
import setup_util as deps

requires = deps.parse_requirements(['deps.txt'])
depend_links = deps.parse_dependency_links(['deps_txt'])

setuptools.setup(
  name='lemooc2013',
  version='0.1dev',
  author='Stefane Fermigier',
  author_email='sf@fermigier.com',
  packages=['website'],
  zip_safe=False,
  platforms='any',
  setup_requires=['setuptools-git'],
  install_requires=requires,
  dependency_links=depend_links,
  include_package_data=True,
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    ],
)
