#! /usr/bin/env python3
# Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

from setuptools import find_packages, setup

from jawanndenn.metadata import APP_NAME, VERSION_STR


def _read(filename):
    with open(filename, 'r') as f:
        return f.read()


_tests_require = [
    'factory-boy>=2.12.0',
    'parameterized>=0.7.1',
]

_extras_require = {
    'tests': _tests_require,
}


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

        python_requires='>=3.6',
        install_requires=[
            'django>=2.2.7',
            'django-extensions>=2.2.5',
            'django-ratelimit>=2.0.0',
            'djangorestframework>=3.11.0',
            'gunicorn>=20.0.4',
            'gunicorn-color>=0.1.0',
        ],
        extras_require=_extras_require,
        tests_require=_tests_require,

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
                f'{APP_NAME} = {APP_NAME}.__main__:main',
            ],
        },

        classifiers=[
            'Development Status :: 4 - Beta',
            'Framework :: Django',
            'Framework :: Django :: 2.2',
            'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',  # noqa: E501
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',  # noqa: E501
            'Programming Language :: JavaScript',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3 :: Only',
            'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
            'Topic :: Office/Business :: Scheduling',
        ]
    )
