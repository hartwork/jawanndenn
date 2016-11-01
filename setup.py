# Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
# Licensed under AGPL v3 or later

import sys
from setuptools import setup

from jawanndenn.metadata import APP_NAME, VERSION_STR


if __name__ == '__main__':
    setup(
        name=APP_NAME,
        version=VERSION_STR,

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
                'static/*',
            ],
        },

        entry_points={
            'console_scripts': [
                '%s = %s.main:main' % (APP_NAME, APP_NAME),
            ],
        },
    )
