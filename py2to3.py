"""
Usage: python py2to3.py <py2file>
Classes:
- PythonFile: Applies the rules from rules.yaml to given python 2 file,
  and creates a <filename>.py3 file.
- Rules: Applies the rules from rules.yaml to given content.
"""
from pathlib import Path
import re
import sys
import yaml


def _main():
    if (len(sys.argv) != 2 or
        sys.argv[1] == "-h" or sys.argv[1] == "--help"):
        _help()
    pyFile = PythonFile(sys.argv[1])
    pyFile.create_py3_file()


def _help():
    print("Usage: python py2to3.py <py2file>")
    sys.exit(0)

class PythonFile:
    """
    Given a python file, it creates a new <filename>.py3 file
    that is converted to python 3 based on the conversion rules.
    """
    def __init__(self, fileName):
        self._fileName = fileName
        self._content = None

    def create_py3_file(self):
        """Creates a <filename>.py3 file, after applying python 2 to 3 conversion rules on it."""
        self._load_content()
        self._apply_rules()
        self._write_to_py3_file()

    def _load_content(self):
        if self._content is None:
            try:
                with open(self._fileName, encoding="utf-8") as src:
                    self._content = src.read()
            except FileNotFoundError as fileExc:
                sys.exit(str(fileExc))

    def _apply_rules(self):
        self._content = Rules().apply(self._content)

    def _write_to_py3_file(self):
        py3FileName = self._fileName + "3"
        if Path(py3FileName).is_file():
            sys.exit(f"{py3FileName} already exists, aborting!")
        else:
            with open(py3FileName, "w", encoding="utf-8") as dest:
                dest.write(self._content)
            print(f"{py3FileName} created!")


class Rules:
    """
    Loads all the rules from rules.yml at initialization,
    and can apply to a given content the rules.
    """
    def __init__(self):
        self._load_rules()

    def _load_rules(self):
        try:
            with open("rules.yaml", encoding="utf-8") as rules:
                try:
                    self.rules = yaml.safe_load(rules)
                except yaml.YAMLError as exc:
                    sys.exit(str(exc))
        except FileNotFoundError as exc:
            sys.exit(str(exc))

    def apply(self, content):
        """Returns the content after applying the loaded rules on it."""
        for ruleName, rule in self.rules.items():
            print("applying rule:", ruleName)
            content = re.sub(rule['regex'], rule['replace'], content, flags = re.M)
        return content


if __name__ == "__main__":
    try:
        _main()
    except SystemExit as sysExc:
        print(sysExc)
