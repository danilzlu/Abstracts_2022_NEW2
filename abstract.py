import os
import re
from io import TextIOWrapper

TITLE_RE = r"\\title{[\w\s\,\.\\\$\-\~]*}"
AUTHORS_RE_UNDERLINED = r"\\author{[\w\s\,\.\\\$\-\~]*\\underline{[\w\s\,\.\\\$\-\~]*}[\w\s\,\.\\\$\-\~]*}"
AUTHORS_RE = r"\\author{[\w\s\,\.\\\$\-\~]*}"
AUTHORS_RE_AFILLS_UNDERLINED = \
    r"\\author\[[\d\,\s]*\]{[\w\s\,\.\\\$\-\~]*\\underline{[\w\s\,\.\\\$\-\~]*}[\w\s\,\.\\\$\-\~]*}"
AUTHORS_RE_AFILLS = r"\\author\[[\d\,\s]*\]{[\w\s\,\.\\\$\-\~]*}"


def extractAuthorsFromRawLine(line: str):
    # chech if there are afills in the line
    if re.match(r"\\author{", line) is not None:    # no afills
        result = re.sub(r'\\author{', '', line)[:-1]
    else:                                           # with afills
        result = re.sub(r"\\author\[[\d\s\,]+\]{", "", line)[:-1]
    return result


def extractPackageFromLine(line):
    """
    Extracts packages from the line in .tex sent abstract file
    :param line:
    :return: set of the extracted abstracts
    """
    result = re.sub(r"\\usepackage\{", '', line)
    result = re.sub(r"[\{\}\,]", ';', result)
    result = re.split(r';', result)
    return result


def extractTitleFromText(text: str):
    """
    Extracts title from the text of .tex sent abstract file
    :param text: text of the .tex sent abstract file
    :return: title of the talk
    """
    title = re.findall(TITLE_RE, text)[0]
    title = re.sub(r'\\title{', '', title)
    title = re.sub(r'\\bf', '', title)
    title = re.sub(r"\\Large", '', title)
    title = re.sub(r"}", '', title)
    return title


def extractAuthorsFromTextRaw(text: str):
    """
    Finds and extracts \\author commands with its content and makes set of raw lines
    :param text: text of the .tex sent abstract file
    :return: set of raw content of \\author commands
    """
    names = set(re.findall(AUTHORS_RE, text))
    names = names.union(set(re.findall(AUTHORS_RE_UNDERLINED, text)))
    names = names.union(set(re.findall(AUTHORS_RE_AFILLS, text)))
    names = names.union(set(re.findall(AUTHORS_RE_AFILLS_UNDERLINED, text)))
    new_names = []
    for authorName in names:
        new_names.append(extractAuthorsFromRawLine(authorName))
    return new_names


def generateFileNameFromAuthorNamesList(authors_names: list):
    """
    Makes file name consisting of last names and initials of authors based on \\author commands content
    :param authors_names: list of raw \\author command content
    :return: string with name of the file to proceed with
    """
    result = []
    for author_name in authors_names:
        name = re.sub(r'[\s\.\,\{\}]*', '', author_name)
        name = re.sub(r"\\underline", '', name)
        result.append(name)
    result.sort()
    return ''.join(result)


def makeTocContent(author_names, title):
    def clearUnderline(author_name):
        name = re.sub(r"\\underline\{", '', author_name)
        name = re.sub(r"\}", '', name).lower()
        return name
    author_names.sort(key=clearUnderline)
    return "\\addcontentsline{toc}{section}{\n" \
           "\\textbf{" + title.strip() + "}\\\\\n" \
                                 "\\textit{" + ' '.join(author_names).strip() + "}}\n"


class Abstracts(object):
    """
    This is class containing all information for processing single abstracts using my template
    """
    '''
    def __init__(self, names: list, title: str, affiliations: list, text: str, packages: set):
        """
        Constructor
        :param names: list of names of authors
        :param title: the title of the talk
        :param affiliations: list of affiliations
        :param text: text of the abstract
        :param packages: set of the packages used in the abstract to push in the main file
        """
        self.names = names.copy()
        self.title = title
        self.affiliations = affiliations.copy()
        self.text = text
        self.packages = packages
        self.file_name = ''.join([name['last_name'] for name in names])
        self.toc = ''
    '''

    def __init__(self):
        self.names = []
        self.text = ''
        self.packages = []
        self.title = ''
        self.file_name = ''
        self.toc = ''

    def getInfoFromFile(self, file: TextIOWrapper):
        """
        Function extracts information to class instance from .tex file of the sent abstracts
        :param file: sent file of the abstract
        :return: None
        """
        # getting text
        abstract_text = file.read()
        self.text = re.split(r"\\end\{document\}", re.split(r"\\begin\{document\}", abstract_text)[1])[0]

        # getting packages
        packages = set()
        for line in file:
            if '\\usepackage' in line:
                packages.union(extractPackageFromLine(line))
        self.packages = packages
        self.title = extractTitleFromText(abstract_text)
        self.names = extractAuthorsFromTextRaw(abstract_text)
        self.file_name = generateFileNameFromAuthorNamesList(self.names)
        self.toc = "\\begingroup\n" + makeTocContent(self.names, self.title) + \
                   "\\vspace{1cm}\n" \
                   "\\input{edited/" + self.file_name + \
                   "}\n" \
                   "\\endgroup\n"

    def __str__(self):
        return '\t'.join([str(self.names), str(self.title), str(self.file_name)])

    def __le__(self, other):
        return self.file_name <= other.file_name

    def __lt__(self, other):
        return self.file_name < other.file_name
