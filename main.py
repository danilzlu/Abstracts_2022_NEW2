import os
import re


def squeezeContentFromTemplateFile(file):
    abstract_text = file.read()
    result = re.split(r'\\begin\{document\}', abstract_text)[1]
    result = re.split(r'\\end\{document\}', result)[0]
    return result


def makePartialFileToInput(inputFile, outputFile):
    text = squeezeContentFromTemplateFile(inputFile)
    outputFile.write(text)


def editAllFilesInFolder(folder_path=os.walk(os.path.dirname(__file__)+'\\raw')):
    for address, dirs, files in folder_path:
        for name in files:
            if name.endswith('.tex'):
                infile = open('raw/' + name, 'r')
                outfile = open('edited/' + name, 'w')
                makePartialFileToInput(infile, outfile)
                infile.close()
                outfile.close()


if __name__ == '__main__':
    pass


