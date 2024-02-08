from setuptools import setup, find_packages

# Read long description from README
with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

# Read the requirements from file
with open("requirements.txt", encoding="utf-8") as file:
    requires = file.read().splitlines()

# Set up the python package with dependencies
setup(
    # Short name of the package
    name="cs-gamestate",
    # Current version of the package
    version="0.0.3",
    # Which packages to include and from where
    packages=find_packages(),
    # Short description of the package
    description="Counter-Strike Game State Integration for Python",
    # Long description from README
    long_description=long_description,
    # The README file is formatted as markdown
    long_description_content_type="text/markdown",
    # Repository URL of the package source
    url="https://github.com/iksnagreb/cs-gamestate",
    # Package author name
    author="Christoph Berganski",
    # Package license name
    license="MIT",
    # Classifiers for categorizing the package
    classifiers=[
        # Classify as open source licensed
        "License :: OSI Approved :: MIT License",
        # Intended for python version 3
        "Programming Language :: Python :: 3",
        # Intended to run on Linux operating systems
        "Operating System :: POSIX :: Linux"
    ],
    # Requirements to be installed with this package
    install_requires=requires,
    # Add non-code files to package
    #   Note: List files to include in MANIFEST.in
    include_package_data=True
)
