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
        self._write_content_to_file(self._fileName + "3")

    def _load_content(self):
        if not hasattr(self, '_content'):
            with open(self._fileName) as src:
                self._content = src.read()

    def _apply_rules(self):
        self._content = Rules().apply(self._content)

    def _write_content_to_file(self, fileName):
        if Path(fileName).is_file():
            print("File already exists, aborting!") 
        else:
            with open(fileName, "w") as dest:
                dest.write(self._content)
            print(f"{fileName} created!")

class Rules:
    def __init__(self):
        self.rules = self._load_rules()

    def _load_rules(self):
        try:
            with open("rules.yaml") as rules:
                try:
                    return yaml.safe_load(rules)
                except yaml.YAMLError as exc:
                    print(exc)
                    sys.exit(1)
        except FileNotFoundError as exc:
            print(exc)
            sys.exit(1)

    def apply(self, content):
        for ruleName, rule in self.rules.items():
            print("applying rule:", ruleName)
            content = re.sub(rule['regex'], rule['replace'], content, flags = re.M)
        return content


if __name__ == "__main__":
    main()
