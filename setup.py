import setuptools

import versioneer

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pychronos-executor",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Bruce Abbott",
    author_email="hey@moonmaus.com",
    description="A Python 3.9 script executor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abbott/pychronos",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
