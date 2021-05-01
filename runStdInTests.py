"""
Program to automate tests and compare to an expected output for a specified program
Requires bash diff command on OS to work, only tested on on Linux machine, with a handful of files.
Author: John Ericson
🧉
"""

import os, glob, re


def runTest(programCommand, fileToTest, rootname, pathOfTests, relDestPathToTests):
    os.system(f"{programCommand} {fileToTest} < {pathOfTests}/{rootname}.in > {relDestPathToTests}{rootname}.myout")


def getFileNames(testFilesPath):

    """
    Gets names of files with ".in" extension, and returns them in list

    :param testFilesPath: path relative to this file, where test files with extension of ".in" are located
    :return: a list of files names in folder with .in extension
    """
    # saving current path
    curPath = os.path.dirname(os.path.abspath(__file__))
    # switching to testfile location
    os.chdir(testFilesPath)
    # retrieving files ending in '.in'
    filenames = glob.glob("*.in")
    # returning to saved path
    os.chdir(curPath)

    filenames.sort()
    return filenames


def runTestsInFilePath(programCommand, fileToTest, testInPath, testOutPath):
    """
    Will run tests with extension ".in" located in specified folder on a specified program. output of these
     tests will be generated with extesion ".myout" and stored where specified by testOutPath.

    :param programCommand: bash command for running program, ie ruby, python, raku
    :param fileToTest: the file that the tests are associated with
    :param testInPath: relative path to this file where input/output tests are located
    :param testOutPath: relative path where resulting files should be sent to
    """

    if testInPath[-1] != '/':
        testInPath += '/'
    if testOutPath[-1] != '/':
        testOutPath += '/'
    for filename in getFileNames('./tests'):
        # removing extension from names
        rootname = re.search(r'(.*)\.in$', filename).group(1)
        runTest(programCommand, fileToTest, rootname, testInPath, testOutPath)


def findDifferences(testInPath, testOutPath):
    """
    Looks for differences between files with ".out" format located in testInPath and compares them to files with
     same name and ".myout" extension. differences compared with bash diff command. These are piped to stdout and saved
      in a folder called differences.txt, which is saved to testOutPath
    :param testInPath: relative path to this file where expected output paths are located
    :param testOutPath: relative path where actual test results are located
    :return:
    """
    if testInPath[-1] != '/':
        testInPath += '/'
    if testOutPath[-1] != '/':
        testOutPath += '/'
    #clearing contents of differences.txt
    os.system(f"> differences.txt")
    for filename in getFileNames(testInPath):
        # removing extension from names
        rootname = re.search(r'(.*)\.in$', filename).group(1)
        os.system(f"echo \"\n\n\n=========differences in test {filename} ========= \">>  differences.txt")
        os.system(f"diff {testInPath}{rootname}.out {testOutPath}{rootname}.myout>>  differences.txt")
    #piping differences to stdout
    os.system(f"cat differences.txt")

#change values below or comment out
runTestsInFilePath('ruby', './lab3.rb', './tests', './')
findDifferences('./tests', './')

