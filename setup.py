#!/usr/bin/env python3

from setuptools import setup, find_packages
import numpy
from setuptools.extension import Extension

__version__ = "1.0.0"

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    install_requires = fh.readlines()

# with open("requirements_test.txt", "r") as fh:
#     test_requirements = fh.readlines()

entry_points = {
    'console_scripts' :
        ['askGompEErtz = GompEErtz.GompEErtz_analisis:main',
     ]
}


#
datos = ['datos/Casos_Diarios_*.csv']
package_data={
    'GompEErtz': datos,
}


setup(
    name="GompEErtz",
    version=__version__,
    packages=find_packages(),
    package_data=package_data,
    include_package_data=True,
#    cmdclass=cmdclass,
    install_requires=install_requires,
#    tests_require=test_requirements,
    entry_points=entry_points,
    author="Emilio Enriquez",
    author_email="jeenriquez@gmail.com",
    description="Analisis epidemiologico de casos COVID en Mexico.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT License",
    keywords="COVID",
    url="https://github.com/jeenriquez/GompEErtz",
    zip_safe=False,
    options={"bdist_wheel": {"universal": "1"}},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Epidemiology",
        ]
)

