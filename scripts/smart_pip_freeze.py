"""
### Smart Pip Freeze

This script updates the requirements.txt file with pipreqs and adds version constraints.

Idea:
1. Find all the packages in the target folder using pipreqs (recursive search).
2. Loosen the version constraints for the packages.
3. Update the requirements.txt file with the loosened version constraints.
    Note: If the package already exists in the requirements.txt file, keep the existing version constraint.
"""

import argparse
import os
import subprocess
from typing import List, Tuple
import tempfile

def get_parser():
    """
    Set up argument parser for the script.
    """
    parser = argparse.ArgumentParser(description="Update requirements.txt with pipreqs and add version constraints.")
    parser.add_argument("target_folder", type=str, help="Path to the target folder containing the code.")
    parser.add_argument("requirements_path", type=str, default="requirements.txt", help="Path to the requirements.txt file.")
    return parser


def get_package_info(package: str) -> dict[str, str]:
    """
    Get package information from PyPI.

    Example:
    pandas>=2.2.0,<3.0 --> ("pandas", ">=2.2.0,<3.0")
    numpy --> ("numpy", "")
    tqdm>=4.0 --> ("tqdm", ">=4.0")
    gensim==3.8.3 --> ("gensim", "==3.8.3")

    Returns:
    {
        "name": "package_name",
        "constraint": ">=2.2.0,<3.0"
    }
    """
    first_split_symbol_idx = None
    for i, char in enumerate(package):
        if char in "=<>":
            first_split_symbol_idx = i
            break
    
    first_split_symbol_idx = first_split_symbol_idx or len(package)
    name, constraint = package[:first_split_symbol_idx], package[first_split_symbol_idx:]
    return dict(name=name, constraint=constraint)

def convert_to_info_dict(packages: List[str]) -> List[dict[str, str]]:
    """
    Convert a list of packages to a list of dictionaries containing package information.
    """
    return [get_package_info(package) for package in packages]

def get_loosened_constraint(constraint: str) -> str:
    """
    Get loosened version constraint for a package.
    Applies only to the strict equality constraint. (e.g. "==3.8.3")

    ==2.2.3 --> >=2.2.0,<3.0
    """
    if not constraint.startswith("=="):
        return constraint
    
    # replace == with ~=
    loosened_constraint = constraint.replace("==", "~=", 1)
    return loosened_constraint
    # version = constraint[2:]

    # if version.count(".") == 3:  # e.g. ==1.2.3.3
    #     major, minor, patch, _ = version.split(".")
    #     loosened_constraint = f">={major}.{minor}.{patch},<{int(major) + 1}.0"
    # elif version.count(".") == 2:
    #     major, minor, _patch = version.split(".")
    #     loosened_constraint = f">={major}.{minor}.0,<{int(major) + 1}.0"
    # elif version.count(".") == 1:  # e.g. ==1.2
    #     major, minor = version.split(".")
    #     loosened_constraint = f">={major}.{minor}.0,<{int(major) + 1}.0.0"
    # return loosened_constraint

def convert_to_loosened_constraint(packages: List[dict[str, str]]) -> List[dict[str, str]]:
    """
    Convert a list of package dictionaries to loosened version constraints.
    """
    loosened_packages = []
    for package in packages:
        loosened_constraint = get_loosened_constraint(package["constraint"])
        loosened_packages.append(dict(name=package["name"], constraint=loosened_constraint))
    return loosened_packages


def read_requirements(file_path: str) -> List[str]:
    """
    Read the existing requirements.txt file if it exists.
    Otherwise, return an empty list.
    """
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        reqs = f.read().splitlines()
        # Remove empty lines and comments
        reqs = [req.strip() for req in reqs if req.strip() and not req.strip().startswith("#")]
        return reqs

def get_requirements_with_pipreqs(target_folder: str) -> List[str]:
    """
    Generate a temporary requirements.txt using pipreqs.
    """
    with tempfile.NamedTemporaryFile() as temp_file:
        subprocess.run(
            ["pipreqs", target_folder, "--force", "--savepath", temp_file.name],
            check=True
        )
        reqs = read_requirements(temp_file.name)
    return convert_to_info_dict(reqs)

def merge_requirements(existing: List[dict[str, str]], new: List[dict[str, str]]) -> List[dict[str, str]]:
    """
    Merge existing and new requirements.
    In case of the same packages, keep the existing version constraint.
    """
    existing_dict = {package["name"]: package["constraint"] for package in existing}
    new_dict = {package["name"]: package["constraint"] for package in new}
    new_dict.update(existing_dict)
    return [{"name": name, "constraint": constraint} for name, constraint in new_dict.items()]

def save_requirements(file_path: str, requirements: List[dict[str, str]]) -> None:
    """
    Save the requirements to a file.
    """
    with open(file_path, "w") as f:
        for package in requirements:
            f.write(f"{package['name']}{package['constraint']}\n")

def update_requirements(target_folder: str):
    """
    Update requirements.txt with pipreqs and add loosened version constraints.
    """
    requirements_file = "requirements.txt"
    pipreqs_requirements = get_requirements_with_pipreqs(target_folder)
    pipreqs_requirements = convert_to_loosened_constraint(pipreqs_requirements)

    existing_requirements = convert_to_info_dict(read_requirements(requirements_file))
    merged_requirements = merge_requirements(existing_requirements, pipreqs_requirements)

    save_requirements(requirements_file, merged_requirements)
    

def main():
    """
    Main function to execute the script.
    """
    parser = get_parser()
    args = parser.parse_args()

    # Run the update
    update_requirements(args.target_folder)

if __name__ == "__main__":
    main()