#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The setup script.
"""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    README = readme_file.read()

with open('HISTORY.rst') as history_file:
    HISTORY = history_file.read()

REQUIREMENTS = ['Click>=6.0', ]

SETUP_REQUIREMENTS = ['pytest-runner', ]

TEST_REQUIREMENTS = ['pytest', ]


def main():
    """
    main setup script to avoid invoked by importing
    """

    setup(
        author="Unviray",
        author_email='unviray@gmail.com',
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            "Programming Language :: Python :: 2",
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
        ],
        description="Bible new world translation in cli",
        entry_points={
            'console_scripts': [
                'nwt=nwt.cli:main',
            ],
        },
        install_requires=REQUIREMENTS,
        license="MIT license",
        long_description=README + '\n\n' + HISTORY,
        include_package_data=True,
        keywords='nwt bible',
        name='nwt',
        packages=find_packages(include=['nwt']),
        setup_requires=SETUP_REQUIREMENTS,
        test_suite='tests',
        tests_require=TEST_REQUIREMENTS,
        url='https://github.com/Unviray/nwt',
        version='0.2',
        zip_safe=False,
    )


if __name__ == '__main__':
    main()
