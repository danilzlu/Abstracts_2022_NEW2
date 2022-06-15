from abstract import *
import os


def squeezeContentFromTemplateFile(file):
    abstract_text = file.read()
    result = re.split(r"\\begin\{document}", abstract_text)[1]
    result = re.split(r"\\end\{document}", result)[0]
    return result


def makePartialFileToInput(input_file, output_file):
    output_file.write(squeezeContentFromTemplateFile(input_file))


def editAllFilesInFolder(folder_path=os.walk(os.path.dirname(__file__)+'\\raw')):
    for address, dirs, files in folder_path:
        for name in files:
            if name.endswith('.tex'):
                infile = open('raw/' + name, 'r')
                outfile = open('edited/' + name, 'w')
                makePartialFileToInput(infile, outfile)
                infile.close()
                outfile.close()


def generateListOfParticipantsPackages(folder_path=os.walk(os.path.dirname(__file__)+'\\raw')):
    packages = set()
    for address, dirs, files in folder_path:
        for name in files:
            if name.endswith('.tex'):
                infile = open('raw/' + name, 'r')
                for inline in infile:
                    if '\\usepackage' in inline:
                        result = extractPackageFromLine(inline)[:-1]
                        packages = packages.union(result)
    return packages


def mainTest():
    abstracts_list = []
    for address, dirs, files in os.walk(os.path.dirname(__file__)+'\\raw'):
        for name in sorted(files):
            if name.endswith('.tex'):
                infile = open('raw/' + name, 'r')
                abstract = Abstracts()
                abstract.getInfoFromFile(infile)
                abstracts_list.append(abstract)
    makeBookOfAbstracts(abstracts_list)


def notMainTest(name=''):
    print(extractAuthorsFromTextRaw(name))
    print(generateFileNameFromAuthorNamesList(extractAuthorsFromTextRaw(name)))


if __name__ == '__main__':
    mainTest()
