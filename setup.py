# -*- coding: UTF-8 -*-

import pathlib
import re

import setuptools

project_path = pathlib.Path(__file__).parent


def find_readme():
    with open(project_path / 'README.md', encoding='utf-8') as readme_file:
        result = readme_file.read()
        return result


def find_requirements():
    with open(project_path / 'requirements.txt',
              encoding='utf-8') as requirements_file:
        result = [each_line.strip()
                  for each_line in requirements_file.read().splitlines()]
        return result


def find_version():
    with open(project_path  /  '__init__.py', 'r+',
              encoding='utf-8') as version_file:
        pattern = '^__version__ = [\'\"]([^\'\"]*)[\'\"]'
        match = re.search(pattern, version_file.readline().strip())
        if match:
            result = match.group(1)
        # lines = version_file.readline()
        # for line in lines:
        #     if line.startswith('__version__'):
        #         version = line.split("=")[-1].strip()
        #         major,minor = version.split(".")
                
            return result

    
setuptools.setup(
    name='gtalk',
    version=find_version(),
    description='Use gtalk to manage your daily task '
                '- by interactive CLI',
    long_description=find_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/cove9988/gtalk',
    author='Paul Guo',
    author_email='cove9988@gmail.com',
    license='MIT',
    keywords='manage all git reposities on one place with interactive command line',
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data ={
        "":[".git_talk.ini"],
    },
    install_requires=find_requirements(),
    python_requires='>=3.6',
    entry_points={'console_scripts': ['gtalk=git_talk.cmd:main']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)