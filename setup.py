#! /usr/bin/env python3
# Copyright (C) 2016 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GNU Affero GPL v3 or later

import os

from setuptools import find_packages, setup

from jawanndenn.metadata import APP_NAME, VERSION_STR


def _read(filename):
    with open(filename) as f:
        return f.read()


_tests_require = [
    "factory-boy>=2.12.0",
    "parameterized>=0.7.1",
]

_extras_require = {
    "tests": _tests_require,
}


def _collect_package_data(top_directory):
    for root, dirs, files in os.walk(os.path.join(top_directory, "static")):
        if files:
            relative_root = os.path.relpath(root, top_directory)
            yield os.path.join(relative_root, "*")


if __name__ == "__main__":
    setup(
        name=APP_NAME,
        version=VERSION_STR,
        license="AGPLv3+",
        description="Libre alternative to Doodle",
        long_description=_read("README.md"),
        long_description_content_type="text/markdown",
        author="Sebastian Pipping",
        author_email="sebastian@pipping.org",
        url="https://github.com/hartwork/jawanndenn",
        python_requires=">=3.9",
        setup_requires=[
            "setuptools>=38.6.0",  # for long_description_content_type
        ],
        install_requires=[
            "django>=2.2.7",
            "django-extensions>=2.2.5",
            "django-ratelimit>=4.0.0",
            "djangorestframework>=3.11.0",
            "gunicorn>=20.0.4",
            "gunicorn-color>=0.1.0",
            "python-dateutil>=2.8.1",
            "python-rapidjson>=1.0",
            "setuptools<81",  # for pkg_resources
        ],
        extras_require=_extras_require,
        tests_require=_tests_require,
        packages=find_packages(),
        package_data={
            APP_NAME: list(_collect_package_data(APP_NAME)),
        },
        entry_points={
            "console_scripts": [
                f"{APP_NAME} = {APP_NAME}.__main__:main",
            ],
        },
        classifiers=[
            "Development Status :: 4 - Beta",
            "Framework :: Django",
            "Framework :: Django :: 2.2",
            "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",  # noqa: E501
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",  # noqa: E501
            "Programming Language :: JavaScript",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Programming Language :: Python :: 3.13",
            "Programming Language :: Python :: 3 :: Only",
            "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
            "Topic :: Office/Business :: Scheduling",
        ],
    )
