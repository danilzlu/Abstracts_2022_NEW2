import os
import re


def extractPackageFromLine(line):
    result = re.sub(r"\\usepackage\{", '', line)
    result = re.sub(r"[\{\}\,]", ';', result)
    result = re.split(r';', result)
    return result


class Abstracts(object):
    """
    This is class containing all information for processing single abstracts using my template
    """
    def __init__(self, names, title, affiliations, text, packages):
        self.names = names.copy()
        self.title = title
        self.affiliations = affiliations.copy()
        self.text = text
        self.packages = packages
        self.file_name = ''.join([name['last_name'] for name in names])

    def getInfoFromFile(self, file):
        abstract_text = file.read()
        packages = set()
        self.text = re.split(r"\\end\{document\}", re.split(r"\\begin\{document\}", abstract_text)[1])[0]
        for line in file:
            if '\\usepackage' in line:
                packages.union(extractPackageFromLine(line))
        self.packages = packages




