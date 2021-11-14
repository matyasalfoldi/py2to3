from pathlib import Path
import re
import sys
import yaml


def main():
    if len(sys.argv) != 2:
        print("Usage: py2to3.py <py2file>")
    pyFile = PythonFile(sys.argv[1])
    pyFile.create_py3_file()


class PythonFile:
    def __init__(self, fileName):
        self._fileName = fileName

    def create_py3_file(self):
        self._load_content()
        self._apply_rules()
        self._write_to_py3_file()

    def _load_content(self):
        if not hasattr(self, '_content'):
            with open(self._fileName) as src:
                self._content = src.read()

    def _apply_rules(self):
        self._content = Rules().apply(self._content)

    def _write_to_py3_file(self):
        py3FileName = self._fileName + "3"
        if Path(py3FileName).is_file():
            sys.exit(f"{py3FileName} already exists, aborting!")
        else:
            with open(py3FileName, "w") as dest:
                dest.write(self._content)
            print(f"{py3FileName} created!")


class Rules:
    def __init__(self):
        self._load_rules()

    def _load_rules(self):
        try:
            with open("rules.yaml") as rules:
                try:
                    self.rules = yaml.safe_load(rules)
                except yaml.YAMLError as exc:
                    sys.exit(str(exc))
        except FileNotFoundError as exc:
            sys.exit(str(exc))

    def apply(self, content):
        for ruleName, rule in self.rules.items():
            print("applying rule:", ruleName)
            content = re.sub(rule['regex'], rule['replace'], content, flags = re.M)
        return content


if __name__ == "__main__":
    try:
        main()
    except SystemExit as exc:
        print(exc)
