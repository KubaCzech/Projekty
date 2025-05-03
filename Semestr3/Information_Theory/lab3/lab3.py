#Authors: Kuba Czech, 156035 and Adam Wilczynski, 156065
import struct

def readFile(name):
    f = open(name, "r")
    text = f.read()
    f.close()
    return text

def readBinaryFile(name):
    f = open(name, "rb")
    text = f.read()
    text = [chr(i) for i in list(text)]
    f.close()
    return " ".join(text)

def readBinaryCompressedFile(name):
    f = open(name, "rb")
    text = f.read()
    text = [str(int(i)) for i in list(text)]
    f.close()
    return " ".join(text)

def writeToFile(name, text):
    f = open(name, "w")
    f.write(text)
    f.close()
    return

def writeToBinaryFile(name, text):
    text = [int(i) for i in text.split()]
    with open(name, 'wb') as binary_file:
        for char in text:
            binary_data = struct.pack('i', char)
            binary_file.write(binary_data)
    return

def compress(text):
    dictLZW = {chr(i): i for i in range(256)}
    old = text[0]
    encodedText = list()
    for letter in text[1:]:
        new = letter
        if (old+new in dictLZW.keys()):
            old = old+new
        else:
            encodedText.append(dictLZW[old])
            dictLZW[old+new] = len(dictLZW)
            old = new
    encodedText.append(dictLZW[old])
    encodedText = [str(i) for i in encodedText]
    return " ".join(encodedText)

def decompress(encodedText):
    dictLZW = {chr(i): i for i in range(256)} #char: code
    dictLZWrev = {i: chr(i) for i in range(256)} #code: char
    textToDecode = encodedText.split()
    textToDecode = [int(i) for i in textToDecode]
    old = dictLZWrev[textToDecode[0]]
    decodedText = ""+old
    for code in textToDecode[1:]:
        new = code
        if new in dictLZWrev.keys():
            new = dictLZWrev[new]
            dictLZW[old+new[0]] = len(dictLZW)
            dictLZWrev[len(dictLZW)-1] = old+new[0]
        else:
            new = old + old[0]
            dictLZW[new] = len(dictLZW)
            dictLZWrev[len(dictLZW)-1] = new
        decodedText = decodedText + new
        old = new
    return decodedText

def compressAndWriteToFile(fileName, binary = False):
    if(binary):
        text = readBinaryFile(fileName)
    else:
        text = readFile(fileName)
    encodedText = compress(text)
    index = fileName.find(".")
    newFileName = fileName[:index] + "_results" + fileName[index:]
    if (binary):
        writeToBinaryFile(newFileName, encodedText)
    else:
        writeToFile(newFileName, encodedText)

#AUTHORS:
print("AUTHORS:")
print("Kuba Czech, 156035")
print("Adam Wilczynski, 156065", end = '\n\n')

#TASK 1:
print("TASK 1:")
properText = readFile("norm_wiki_sample.txt")
compressAndWriteToFile("norm_wiki_sample.txt")
compressedText = readFile("norm_wiki_sample_results.txt")
decompressedText = decompress(compressedText)
if (properText == decompressedText):
    print("SUCCESS - first file compressed and decompressed properly")

properText = readFile("wiki_sample.txt")
compressAndWriteToFile("wiki_sample.txt")
compressedText = readFile("wiki_sample_results.txt")
decompressedText = decompress(compressedText)
if (properText == decompressedText):
    print("SUCCESS - second file compressed and decompressed properly")
print("\n")

#TASK 2:
print("TASK 2:")
compressAndWriteToFile("lena.bmp", True)
print("SUCCESS - lena.bmp compressed properly")