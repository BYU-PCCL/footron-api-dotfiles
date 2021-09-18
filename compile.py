import os
import argparse
from typing import Dict, Any
from pathlib import Path
import shutil
import sys

from jinja2 import Template
import toml

IGNORE_DIRS = {"__pycache__", ".git/"}
IGNORE_FILES = {"example-config.toml", "requirements.txt", "compile.py", ".gitignore"}

TEMPLATE_SUFFIX = ".template"
BUILD_DIR = Path("build")

def main(config_filename: str):
    if BUILD_DIR.exists():
        print(f"{BUILD_DIR} already exists, can't compile", file=sys.stderr)
        return

    with open(config_filename) as config_file:
        config = toml.load(config_file)

    for directory, subdirs, files in os.walk("."):
        if any(filter(lambda a: a in directory, IGNORE_DIRS)):
            continue

        built_path = BUILD_DIR / Path(directory).relative_to(".")
        built_path.mkdir(parents=True, exist_ok=True)
        for fname in files:
            if any(filter(lambda a: a in fname, {*IGNORE_FILES, config_filename})):
                continue
            input_file = Path(directory) / fname
            if fname.endswith(TEMPLATE_SUFFIX):
                output_file = built_path / fname[:-len(TEMPLATE_SUFFIX)]
                with open(input_file) as template_file:
                    template = Template(template_file.read())
                    with open(output_file, "w") as rendered_file:
                        rendered_file.write(template.render(**config["secrets"]))
            else:
                output_file = built_path / fname
                shutil.copyfile(input_file, output_file, follow_symlinks=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file", nargs="?", default="config.toml")
    args = parser.parse_args()
    main(args.config_file)
