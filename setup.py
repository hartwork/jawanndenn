# Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

from setuptools import setup

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

        install_requires=[
            'bottle',
            'paste',
        ],

        packages=[
            APP_NAME,
        ],

        package_data={
            APP_NAME: [
                'static/css/*',
                'static/html/*',
                'static/js/*',
            ],
        },

        entry_points={
            'console_scripts': [
                '%s = %s.main:main' % (APP_NAME, APP_NAME),
            ],
        },

        classifiers=[
            'Development Status :: 4 - Beta',
            'Framework :: Bottle',
            'Framework :: Paste',
            'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Programming Language :: JavaScript',
            'Programming Language :: Python :: 2.7',
            'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
            'Topic :: Office/Business :: Scheduling',
        ]
    )
