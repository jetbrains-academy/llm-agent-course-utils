from setuptools import setup, find_packages

setup(
    name="tools-basics",  # The package name users will use to install
    version="0.1.0",
    packages=find_packages(where="src"),  # Look for packages in the "src" folder
    package_dir={"": "src"},  # Map root of the package to "src"
    install_requires=[],  # Add dependencies here if needed
    description="A set of tools for lesson 01_basics",
    author="Rodion Khvorostov",
    author_email="rodion.khvorostov@jetbrains.com",
)
