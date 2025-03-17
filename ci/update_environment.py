#!/usr/bin/env python
"""Updates the book user and Binder environments."""

# Imports
import boto3
from pathlib import Path
import shutil
import time


def main():
    def backup_env(env_file="environment.yml"):
        """Creates a backup copy of the current environment file."""
        # Create filename for backup file
        timestr = time.strftime("%Y%m%d-%H%M%S")
        new_filename = f"environment-{timestr}.yml"
        print(f"Creating backup of {env_file} as {new_filename}...")

        # Create file paths
        orig_file = Path(env_file)
        new_file = Path(new_filename)

        # Make backup copy
        shutil.copy(orig_file, new_file)

        return None

    def extract_user_env(book_env="py312-book-building.yaml"):
        """Prunes book building stuff from the book building environment."""
        # Make empty list for user environment content
        user_env_content = []

        # List of libraries needed only for book building
        book_build_only = [
            "sphinx",
            "ipython",
            "ipykernel",
            "nbsphinx",
            "sphinx-book-theme",
            "sphinxcontrib-bibtex",
            "jupytext",
            "black",
            "black-jupyter",
            "jupyterlab-spellchecker",
            "nbconvert",
            "pip",
            "pandoc",
            "boto3",
        ]

        # Read in book building environment file
        with open(book_env) as f:
            bb_file = f.readlines()

            # Find indices of lines containing "dependencies" and "pip:"
            start_index = [idx for idx, s in enumerate(bb_file) if "dependencies" in s][
                0
            ]
            end_index = [idx for idx, s in enumerate(bb_file) if "pip:" in s][0]
            # Add one to start_index to skip line containing "dependencies"
            start_index += 1

            # Write lines not containing one of the book-only libraries to the user_env list
            for line in bb_file[start_index:end_index]:
                lib = line.split("=")[0]
                if "-" in lib:
                    lib = lib.split("- ")[1]
                    if not lib in book_build_only:
                        user_env_content.append(line.split("\n")[0])

        return user_env_content

    def write_user_env(user_env, env_file="environment.yml", env_name="pythongis"):
        """Writes content to the user environment file."""
        print(f"Writing new environment file to {env_file}...")
        with open(env_file, "w") as f:
            header = (
                f"name: {env_name}\n\nchannels:\n  - conda-forge\n\ndependencies:\n"
            )
            f.write(header)
            for line in user_env:
                f.write(f"{line}\n")

        return None

    def copy_env_to_binder_dir(env_file="environment.yml"):
        """Copies updated environment file to the binder directory."""
        # Define file paths
        src_file = Path(env_file)
        dest_file = Path.cwd().parent / "binder" / src_file

        # Report progress
        print(f"Copying {src_file} to {dest_file}...")

        # Make backup copy
        shutil.copy(src_file, dest_file)

        return None

    def copy_env_to_allas(upload=False, env_file="environment.yml"):
        """Uploads the environment file to Allas."""
        # Set S3 resource location
        s3_resource = boto3.resource("s3", endpoint_url="https://a3s.fi")

        # Upload new environment file to Allas
        if upload:
            print(f"Uploading {env_file} to Allas...")
            s3_resource.Object("PythonGIS", "environment/environment.yml").upload_file(
                "environment.yml"
            )

        return None

    backup_env()
    user_env = extract_user_env()
    write_user_env(user_env)
    copy_env_to_binder_dir()
    # Set upload to True to update file in Allas
    copy_env_to_allas(upload=False)


if __name__ == "__main__":
    main()
