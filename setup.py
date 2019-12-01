#! /usr/bin/env python2
# Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

from setuptools import find_packages, setup

from jawanndenn.metadata import APP_NAME, VERSION_STR


def _read(filename):
    with open(filename, 'r') as f:
        return f.read()


if __name__ == '__main__':
    setup(
        name=APP_NAME,
        version=VERSION_STR,

        license='AGPLv3+',
        description='Libre alternative to Doodle',
        long_description=_read('README.rst'),

        author='Sebastian Pipping',
        author_email='sebastian@pipping.org',
        url='https://github.com/hartwork/jawanndenn',

        python_requires='>=2.7, <3',
        install_requires=[
            'Jinja2',
            'bottle',
            'python-dateutil',
            'tornado<6',  # 6.x requires Python 3.x
        ],

        packages=find_packages(),
        package_data={
            APP_NAME: [
                'static/css/*',
                'static/html/*',
                'static/js/*',
            ],
        },

        entry_points={
            'console_scripts': [
                '{} = {}.__main__:main'.format(APP_NAME, APP_NAME),
            ],
        },

        classifiers=[
            'Development Status :: 4 - Beta',
            'Framework :: Bottle',
            'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',  # noqa: E501
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',  # noqa: E501
            'Programming Language :: JavaScript',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 2 :: Only',
            'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
            'Topic :: Office/Business :: Scheduling',
        ]
    )
