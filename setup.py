#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

requirements = ["numpy", "pandas", "pydantic", "streamlit", "loguru"]

if __name__ == "__main__":
    setup(
        author="Angus Lee",
        author_email="agsl0905@gmail.com",
        python_requires=">=3.10",
        classifiers=[
            "Development Status :: 2 - Pre-Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Natural Language :: English",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
        ],
        description="Comission Calculator",
        install_requires=requirements,
        license="MIT license",
        long_description=readme,
        include_package_data=True,
        keywords="commission_calculator",
        name="commission_calculator",
        packages=find_packages(include=["commission_calculator"], exclude=["test"]),
        url="https://github.com/angusll/commission_calculator",
        version="0.1.0",
        zip_safe=False,
    )
