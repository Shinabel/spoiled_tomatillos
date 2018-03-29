#!/usr/bin/env python3
"""
    Flask application testing for team 53 spoiled tomatillos
"""
from setuptools import setup, find_packages

setup(name="team_53_spoiled_tomatillios",
        version="0.1",
        packages=find_packages(),
        description="Team 53 Spoiled tomatillios project",
        author="Team 53",
        author_email="Team53@noreply.com",
        license = "MIT",
        install_requires=[
            'flask',
        ],
        setup_requires=[
            'pytest-runner',
        ],
        tests_require=[
            'pytest',
        ],
        )
