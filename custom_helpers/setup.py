from setuptools import setup, find_packages

setup(
    name="custom_helpers",  # The package name users will use to install
    version="0.1.0",
    packages=find_packages(where="src"),  # Look for packages in the "src" folder
    package_dir={"": "src"},  # Map root of the package to "src"
    install_requires=[
        "omegaconf"
    ],
    description="A set of helper functions",
    author="Rodion Khvorostov",
    author_email="rodion.khvorostov@jetbrains.com",
)
