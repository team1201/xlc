#!/usr/bin/env python

import os
from setuptools import setup

requires = []

dependency_links = [
    'http://192.168.18.18/project/hhl/tool/zrong-0.2.2.tar.gz'
]

entry_points = {
    'console_scripts': [
        'xlc = xlc:call',
    ]
}

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.4',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

package_data = {
    'hhlc':['build.conf'],
}

#data_files = [(root, [os.path.join(root, f) for f in files])
#    for root, dirs, files in os.walk('bin')]

setup(
    name="xlc",
    version="0.3.0",
    url='http://zengrong.net/',
    author='zrong',
    author_email='zrongzrong@gmail.com',
    description="Convert xls to lua and csv file.",
    packages=['xlc'],
    classifiers=classifiers,
    #include_package_data=True,
    #package_data=package_data,
    #data_files=data_files,
    #install_requires=requires,
    #entry_points=entry_points,
    #dependency_links = dependency_links,
    #test_suite='hhlb.test',
)
