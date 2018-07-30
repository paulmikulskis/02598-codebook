#!/usr/bin/env python3
import csv
import linecache
import os.path

print('---------------------------')
print('')
variableStart = input("input desired starting variable number: ")
if not str(variableStart).isnumeric():
    print('please input a number betwwen 1 and 2086')
    print('exiting...')
    exit()
variableStart = int(variableStart)
variableEnd = input("input desired ending variable number (press enter for all): ")
if variableEnd is "":
    variableEnd = 2085
if not str(variableEnd).isnumeric():
    print('please input a number betwwen 1 and 2086')
    print('exiting...')
    exit()
variableEnd = int(variableEnd)
if variableEnd < variableStart:
    print('ending variable must be larger than starting variable')
    print('exiting...')
    exit()
numberOfParticipantsToRead = input("input desired participant samples (press enter for all): ")
if numberOfParticipantsToRead is "":
    numberOfParticipantsToRead = 1010101010101
if not str(numberOfParticipantsToRead).isnumeric():
    print('please input a number betwwen 1 and 2086')
    print('exiting...')
    exit()

if numberOfParticipantsToRead == 1010101010101:
    numberOfParticipantsToRead = -1

numberOfParticipantsToRead = int(numberOfParticipantsToRead)
csvFileName = 'survey_' + str(variableStart) + '_' + str(variableEnd) + '_' + str(numberOfParticipantsToRead) + '.csv'
if os.path.isfile(csvFileName):
    a = input('filename %s already exists, overwrite? (y/n)' %csvFileName)
    if a is 'y':
        print("rewriting file '%s'" %csvFileName)
    elif a is 'n':
        csvFileName = csvFileName[:-4] + '(1).csv'
        print('new filename will be %s', csvFileName)
    else:
        print("press 'y' for yes, 'n' for no next time, exiting...")
        exit()

vst = variableStart
#f = open('02598-0001-Data.txt', encoding='UTF-8')

f = open('02598-Codebook-3.txt', encoding='UTF-8')
#range = (33,34)
#print(l[range[0]-1:range[1]])
print("extracting variables '%s' through '%s'..." %('v'+str(variableStart), 'v'+str(variableEnd + 1)))
startLine = 4070
for j in range(startLine):
    f.readline()

l = f.readline()
while 'v'+str(variableStart) not in l.split():
    startLine += 1
    l = f.readline()
endLine = startLine + 1

while 'v'+str(variableEnd) not in l.split():
    endLine += 1
    l = f.readline()


codebook = []
codebookEntry = {}
f.seek(0)
for j in range(startLine):
    f.readline()
l = f.readline()
#print(l)
variableStart = 1
posStart = 1
posEnd = 1

print('data collection registered between lines %i - %i' %(startLine, endLine))
while startLine <= endLine:
    var = l

    if variableStart == 2041:
        if posStart < 5146:
            print('correcting error')
            variableStart = -2040
    if variableStart == -2040:
        position = (5132,5139)
        posEnd = 5139
        posStart = posEnd + 1
        variableStart = -2041
    if variableStart == -2041:
        position = (5140,5147)
        posEnd = 5147
        posStart = posEnd + 1
        variableStart = 2041
    #read until next variable is hit
    l = f.readline()

    if l.find("vv") > 0:
        l = l[:l.find("vv")] + l[l.find("vv")+1:]
    if l.find("v2040A") > 0:
        l = l[:l.find("v2040A")] + 'v-2039' + l[l.find("v2040A")+6:]
        print(l)
    if l.find("v2040B") > 0:
        l = l[:l.find("v2040B")] + 'v-2040' + l[l.find("v2040B")+6:]
        print(l)
    startLine += 1

    while 'v'+str(variableStart+1) not in l.split() and str(variableStart+1) not in l.split():
        var += l
        l = f.readline()
        if l.find("vv") > 0:
            l = l[:l.find("vv")] + l[l.find("vv")+1:]
        startLine += 1

    prefix = var[:var.find('v'+str(variableStart))]
    prefix = prefix.strip()
    if len(prefix) < 1:
        prefix = "n/a"
    if len(prefix) > 15:
        prefix = "n/a"
    dvar = [v.strip() for v in var.split()]
    dvar = list(filter(lambda x: x.isnumeric(), dvar))
    dvar = [int(v) for v in dvar]
    position = (None,None)

    if posStart in dvar:
        posEnd = dvar[dvar.index(posStart)+1]
        position = (posStart, posEnd)
        posStart = posEnd + 1
    if position == (None, None):
        print('unable to obtain position for v%i, looking in position %i' %(variableStart, posStart))
        print('line::', dvar)

    codebook.append({'name': 'v'+str(variableStart), 'position': position, 'prefix': prefix})
    variableStart += 1
    if variableStart ==  2040:
        variableStart = -2040
    if variableStart ==  -2041:
        variableStart =  2041
#    if(variableStart < 15):
#        print(var.encode())

#variable name->desc table
f.seek(0)
vj = 0
viq = 1

while vj < 1127:
    l = f.readline()
    vj += 1

while vj < 3414:
    l = f.readline()
    vj += 1
    if l.find('V' + str(viq)) > -1:
        #print('found V%s on line: %i'%(str(viq),vj))
        begin = l.find('V' + str(viq)) + len('V' + str(viq))
        end = l.find('\n', l.find('V' + str(viq)) + len('V' + str(viq)))
        desc = l[begin:end]
        if viq < len(codebook):
            codebook[viq - 1]["desc"] = desc.strip()
        viq += 1




from copy import deepcopy
f = open('02598-0001-Data.txt', encoding='UTF-8')
data = f.read()
data = data.split('\n')[:-2][:numberOfParticipantsToRead]
g = 0
survey = []
for part in data:
    g = g+1
    #vars is a container which holds the len(codebook) variables
    #for a participant in the survey in dict format
    vars = []
    for idx,v in enumerate(codebook):
        entry = codebook[idx]
        start = v['position'][0]-1
        end = v['position'][1]
        entry['value'] = part[start:end].strip()
        vars.append(entry)
    print('parsing participant %i/%i' %(g, len(data)))
    survey.append(deepcopy(vars))
    #print(len(vars))

#for j in range(20):
#    print(codebook[j])

#if (survey[2][11]['value'], survey[2][12]['value']) is (survey[4][11]['value'], survey[4][12]['value']):
#    print('w: age for survey members 2 and 4 are the same', (survey[2][11]['value'], survey[2][12]['value']))

with open(csvFileName, 'w') as csvfile:
     filewriter = csv.writer(csvfile, dialect='excel')
     vars = [v['name'] for v in codebook]
     vars.insert(0,'participant')
     filewriter.writerow(vars)

     for idx,part in enumerate(survey):
         row = []
         row.append(idx + 1)
         for var in part:
             row.append(var['value'])
         if len(row) != len(vars):
             print("length mismatch...")
             print(len(row), len(vars))
         filewriter.writerow(row)
print("----")
print("finished extracting variables 'v%i' through 'v%i' for participants [0 - %i] into file '%s'" %(vst, variableEnd, numberOfParticipantsToRead, csvFileName))
