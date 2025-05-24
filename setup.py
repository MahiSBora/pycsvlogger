from setuptools import setup, find_packages

setup(
    name="pycsvlogger",
    version="0.1.0",
    description="Flexible, general-purpose CSV-based structured logging for Python",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Mahipal Bora",
    author_email="mahi123bora@gmail.com",
    url="https://github.com/MahiSBora/pycsvlogger.git",  # update with your repo
    license="MIT",
    packages=find_packages(),          # will include the pycsvlogger/ package
    python_requires=">=3.7",
    install_requires=[],              # no external dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)