#encoding: utf-8
#!/usr/bin/env python
'''
Created on Dec 2, 2014

@author: jack
'''
import os
from config import config
from operator import delitem

"""
Check the sub proteins is in string with delimeter
"""
def issubStrin(allStr, delimeter, substr):
    allValue = allStr.split(delimeter)
    for value in allValue:
        value = value.strip()
        if (value == substr):
            return True
        pass
    return False

"""
Get Pubmed id from file, return a set contains pubmed id.

Input: file human.db.all.201108.intm
    contains the interaction of protein pair and it's corresponding pubmed id

return (set, dictionary):
    Set: contain of all pubmed id.
    Dictionary: (key: pubmedId, value: Protein interaction pair)
"""
def getAllPubmedIdAndPubmedId2Proteins(filename, delimeter, segLocation):
    if (os.path.exists(filename)):
        
        pubmedIdSet = set()
        pubmedInteractionProteinDict = {}
        para = config.Parameter()
        notExistedProteinSet = getSetNotExistedProtein(para.notExistedProteinFile)
        
        with open(filename, 'r') as f_rConn:
            AllLines = f_rConn.readlines()
            for line in AllLines:
                line = line.strip()
                if line[0] == "#" or line == '':
                    continue
                lineValues = line.split(delimeter)
                if (len(lineValues) < segLocation):
                    line = f_rConn.readline()
                    continue
                proteinPair = lineValues[1].strip()
                ## if protein in proteinPair is not existed, just escape
                if True == judgeProteinExisted(proteinPair, "|", notExistedProteinSet):
                    continue
                allPubmedIDStr = lineValues[segLocation-1].strip()
                
                pubmedList = allPubmedIDStr.split(",")
                for pubmedstr in pubmedList:
                    pubmedList = pubmedstr.split(':')
                    pubmedId = ""
                    if (len(pubmedList) >= 2):
                        pubmedId = pubmedList[1]
                    pubmedId = pubmedId.strip()
                    if (pubmedId in pubmedIdSet):
                        value = pubmedInteractionProteinDict.get(pubmedId)
                        if issubStrin(value, ",", proteinPair) == True:
                            continue
                        value += "," + proteinPair
                        pubmedInteractionProteinDict[pubmedId] = value
                        pass
                    else:
                        pubmedInteractionProteinDict[pubmedId] = proteinPair
                    pubmedIdSet.add(pubmedId)
                    pass
                pass
            pass
        return (pubmedIdSet, pubmedInteractionProteinDict)
    pass


"""
Get all official Protein and Gene

input: proteinGene_201108.intm (scrapy file with unique protein name)
        notExistedProteinSet (protein not existed)
return
    a dictionary (key: protein, value: Gene)
"""
def getOfficialProteinGene(filename, delimeter, proteinLoc, geneSegLoc):
    if (os.path.exists(filename)):
        pubmedProtein2GeneDict = {}
        with open(filename, 'r') as f_rConn:
            allLines = f_rConn.readlines()
            for line in allLines:
                line = line.strip()
                if line[0] == "#" or line == '':
                    continue
                AllValues = line.split(delimeter)
                protein = AllValues[proteinLoc-1].strip()
                if (len(AllValues) < 3 or pubmedProtein2GeneDict.has_key(protein)):
                    continue
                allGeneStr = AllValues[geneSegLoc-1].strip()
                geneList = allGeneStr.split("|")
                pubmedProtein2GeneDict[protein] = geneList[0].strip()
                pass
            pass
        return pubmedProtein2GeneDict
    return None

'''
Judge the protein is existed or not, with the formal as follows.
    Q9UM11|Q12834
'''
def judgeProteinExisted(proteins, delimeter, notExistedProteinSet):
    proteinList = proteins.split(delimeter)
    for protein in proteinList:
        protein = protein.strip()
        if (protein in notExistedProteinSet):
            return True
        pass
    return False

'''
Get protein not existed, return a set
'''
def getSetNotExistedProtein(notExistedFilename):
    if (os.path.exists(notExistedFilename)):
        with open(notExistedFilename, 'r') as f_rConn:
            notExistedProteinSet = set()
            #allLines = f_rConn.readLines()
            for line in f_rConn:
                line = line.strip()
                if (line[0] == '#' or line == ''):
                    continue
                notExistedProteinSet.add(line)
                pass
            return notExistedProteinSet
        pass
    else:
        print("file[%s] is not existed", notExistedFilename)

'''
Get protein gene dictionary, return a dict
'''
def getDictValeProteinGene(proteinGeneFile, delimeter='\t'):
    if (os.path.exists(proteinGeneFile)):
        with open(proteinGeneFile, 'r') as f_rConn:
            proteinGeneDict = {}
            allLines = f_rConn.readLines()
            for line in allLines:
                line = line.strip()
                if (line[0] == '#' or line == ''):
                    continue
                allValues = line.split(delimeter)
                key = allValues[0].strip()
                if not proteinGeneDict.has_key(key):
                    value = allValues[1].strip()
                    proteinGeneDict[key] = value
                pass
            return proteinGeneDict
        pass
    else:
        print("file [%s] is not existed." % proteinGeneFile)


"""
Input: Get all official Protein and Gene,
Return a dictionary: (key: pubmedid, value: Gene)
"""
def getPubmedId2GeneList(pubmedInteractionProteinDict, delimeter, Protein2GeneDict):
    if (len(pubmedInteractionProteinDict) > 0):
        proteinHasnotGeneSet = set()
        pubmedId2GeneDict = {}
        warnPubmedText = ""
        for (pubmedId, proteins) in pubmedInteractionProteinDict.items():
            allProteinList = proteins.split(delimeter)
            GeneValues = ''
            kElem = 1
            for proteinPair in allProteinList:
                proteinList = proteinPair.split('|')
                proteinA = proteinList[0].strip()
                if (len(proteinList) < 2):
                    continue
                proteinB = proteinList[1].strip()
                
                if Protein2GeneDict.has_key(proteinA) and Protein2GeneDict.has_key(proteinB):
                    if (kElem > 1):
                        GeneValues += ","
                    GeneValues += Protein2GeneDict[proteinA] + "|" + Protein2GeneDict[proteinB]
                else:
                    if not Protein2GeneDict.has_key(proteinA) and proteinA not in proteinHasnotGeneSet:
                        proteinHasnotGeneSet.add(proteinA)
                    if not Protein2GeneDict.has_key(proteinB) and proteinB not in proteinHasnotGeneSet:
                        proteinHasnotGeneSet.add(proteinB)
                    ## save into log file.
                    ## print("Protein [%s|%s] is not existed." % (proteinA, proteinB))
                kElem += 1
                pass
            if (GeneValues == ''):
                warnPubmedText += ("[%s, %s] hasn't corresponding Gene.\n" % (pubmedId, proteins)) 
                continue
            if not pubmedId2GeneDict.has_key(pubmedId):
                pubmedId2GeneDict[pubmedId] = GeneValues
            else:
                print("%s is already existed." % pubmedId)
            pass
        ## Write into log file
        if (warnPubmedText != ''):
            para = config.Parameter()
            with open(para.warnProteinHasNotGene, 'w') as f_wConn:
                f_wConn.write(warnPubmedText.strip())
        return (pubmedId2GeneDict, proteinHasnotGeneSet)
    else:
        print("Please check dict of pubmedid2ProteinDict, it's null in here.")
    pass

def getUniquePubmedIdText(uniquePubmedIdSet, srcPubmedIdTextDir, dstPubmedIdTextDir):
    if (len(uniquePubmedIdSet) > 0):
        print(len(uniquePubmedIdSet))
        filenameList = []
        for parent, dirname, filenames in os.walk(srcPubmedIdTextDir):
            for file in filenames:
                srcFullFname = srcPubmedIdTextDir + os.sep + file
                filenameList.append(srcFullFname)
        for fname in filenameList:
            print("Deal with file[%s]." % fname)
            with open(fname, 'r') as f_rConn:
                allLines = f_rConn.readlines()
                for line in allLines:
                    line = line.strip()
                    if (line[0] == '#' or line == ''):
                        continue
                    textValueList = line.split("\t")
                    if (len(textValueList) < 2):
                        continue
                    newPubmedText = ''
                    pubmedId = textValueList[0].strip()
                    if pubmedId in uniquePubmedIdSet:
                        ## Title and Abstract
                        newPubmedText += textValueList[1].strip() + '\n'
                        newPubmedText += textValueList[2].strip()
                        ## new filename
                        newFilename = dstPubmedIdTextDir + os.sep + pubmedId
                        saveValueIntoFile(newPubmedText, newFilename)
                        uniquePubmedIdSet.remove(pubmedId)
                        pass
            print("-------End Deal with file[%s]." % fname)
            print('--------------------------------------')
        return uniquePubmedIdSet
    pass

def saveValueIntoFile(textValue, filename):
    with open(filename, 'wb') as f_wConn:
        f_wConn.write(textValue.strip())

'''
Write a set into appointed file.
'''
def saveAllSetValueIntoFname(valueOfSet, filenameOfSet, headTitle):
    if (len(valueOfSet) > 0):
        allLines = headTitle
        with open(filenameOfSet, 'wb') as f_wConn:
            for pubmedid in valueOfSet:
                allLines += pubmedid + "\n"
                pass
            f_wConn.write(allLines.strip())
            pass
        pass
    else:
        print("Current set is None.")

'''
Write a set into appointed file.
'''
def saveAllDictValueIntoFname(valueOfDict, filenameOfDict, headTitle):
    if (len(valueOfDict) > 0):
        allLines = headTitle
        with open(filenameOfDict, 'wb') as f_wConn:
            for (key, value) in valueOfDict.items():
                allLines += key + "\t" + value + "\n"
                pass
            f_wConn.write(allLines.strip())
            pass
        pass
    else:
        print("Current Dict is None.")
        pass
    pass
'''
    Convert a list into string, with split char of delimeter
'''
def convertListToStr(ValueList, delimeter):
    num = len(ValueList)
    k = 1
    allValues = ''
    for value in ValueList:
        allValues += value
        if (k < num):
            allValues += delimeter
        k += 1
    return allValues

def stringOfProteinsAndGeneSynonyms(GeneSynonymList, ProteinValues):
    ValuesOfStr = ProteinValues + '\t-' ## if GeneSynonyms is null, return this values
    GeneSynonyms = convertListToStr(GeneSynonymList, '|')
    if (GeneSynonyms != ''):
        ValuesOfStr = ProteinValues + '\t' + GeneSynonyms
    return ValuesOfStr

'''
Input: proteinGene_201108.intm
        scrapy file from website. consists of protein, protein fullname, alternative names, short names
                    and corresponding gene, gene synonyms.
Return a dictionary: (key: Gene; Values: Proteins\tGene Synonms)
'''
def getDictKeyOfGeneValueOfGeneSynonymsProtein(proteinGeneFname):
    with open(proteinGeneFname, 'rb') as f_rConn:
        geneProteinsGeneSynonymsDict = {}
        allLines = f_rConn.readlines()
        for line in allLines:
            line = line.strip()
            if (line[0] == '#' or line == ''):
                continue
            GeneProteinsList = line.split('\t')
            if (len(GeneProteinsList) < 3):
                continue
            GeneAndItsSynonyms = GeneProteinsList[2].strip()
            ''' Get the official Gene name -- the first gene name '''
            Gene = GeneAndItsSynonyms.split('|')[0]
            '''Beginning from the second gene is the synonyns of official gene'''
            GeneSynonyms = GeneAndItsSynonyms.split('|')[1:]
            '''In this dict, (key: Gene, Values: protein and synonyns of official gene)'''
            Values = stringOfProteinsAndGeneSynonyms(GeneSynonyms, GeneProteinsList[1].strip())
            geneProteinsGeneSynonymsDict[Gene] = Values
            pass
        return geneProteinsGeneSynonymsDict                
    return None

'''
Input: proteinGene_201108.intm
        scrapy file from website. consists of protein, protein fullname, alternative names, short names
                    and corresponding gene, gene synonyms.
        simpleGeneInfo.HomoSapiens
            file contains of (GeneID, Gene, Gene Synonyms)
return: Dict (Gene, Gene Synonyms, Corresponding Proteins)
'''
def getDictWithGeneAsKeyProteins_GeneSynonymsAdValues(proteinGeneFname, geneAndItsSynonymsFname):
    if (os.path.exists(proteinGeneFname)):
        '''(key: Gene; Values: Proteins\tGene Synonms)'''
        geneProteinsGeneSynonymsDict = getDictKeyOfGeneValueOfGeneSynonymsProtein(proteinGeneFname)
        ## Get the all keys in the dict, saving it in a set()
        AllGeneKeysSet = set(geneProteinsGeneSynonymsDict.keys())
        newGeneProteins_GeneSynonymsDict = {}
        with open(geneAndItsSynonymsFname, 'rb') as f_rConn:
            allLines = f_rConn.readlines()
            for line in allLines:
                line = line.strip()
                if (line[0] == '#' or line == ''):
                    continue
                allValueList = line.split('\t')
                GeneAsKey = allValueList[1].strip()
                geneSynonyms = allValueList[2].strip()
                keyValues = geneSynonyms + '\t-'
                '''
                    check current key value in the keys dict.
                    if in it, we mush update the corrsponding keyValues
                '''
                if GeneAsKey in AllGeneKeysSet:
                    ''' Append the corrsponding key values
                            At first: Gain the key values with the geneKey
                    '''
                    valuesInDict = geneProteinsGeneSynonymsDict[GeneAsKey]
                    '''The first elem is proteins, the next is gene synonyms'''
                    valuesInDictList = valuesInDict.split('\t')
                    proteinsValues = valuesInDictList[0].strip()
                    otherGeneSynonyms = valuesInDictList[1].strip()
                    ## if the gene synonyms is '-'
                    if (geneSynonyms == '-'):
                        keyValues = otherGeneSynonyms + '\t' + proteinsValues
                    else:
                        if (otherGeneSynonyms == '-'):
                            keyValues = geneSynonyms + '\t' + proteinsValues
                        else:
                            allGeneSynList = otherGeneSynonyms.split('|')
                            newGeneValues = geneSynonyms
                            for gene in allGeneSynList:
                                gene = gene.strip()
                                if (0 == isGeneInSynonymsStr(gene, geneSynonyms, '|')):
                                    newGeneValues += "|" + gene
                                    pass
                            keyValues = newGeneValues + '\t' + proteinsValues
                            pass
                        pass
                    pass
                
                if (not newGeneProteins_GeneSynonymsDict.has_key(GeneAsKey)):
                    newGeneProteins_GeneSynonymsDict[GeneAsKey] = keyValues
                else:
                    value = newGeneProteins_GeneSynonymsDict[GeneAsKey]
                    if (value == '-s\t-' and value != keyValues):
                        newGeneProteins_GeneSynonymsDict[GeneAsKey] = keyValues
                        print GeneAsKey, keyValues
                    #print GeneAsKey, newGeneProteins_GeneSynonymsDict[GeneAsKey]
                pass
        return newGeneProteins_GeneSynonymsDict
    else:
        print("file: [%s] isn't existed." % proteinGeneFname)
    return None

'''
    Whether the gene is in the string list geneSynonyms(split with delimeter) or not?
'''
def isGeneInSynonymsStr(gene, geneSynonyms, delimeter):
    allSynonymList = geneSynonyms.split(delimeter)
    synSet = set()
    ## Case insensitive | Case ignorable
    for aSyn in allSynonymList:
        synSet.add(aSyn.lower())
    if gene.lower() in synSet:
        return 1
    return 0

'''
input: geneProtein_HomoSapines.mergeSummarize (self.geneProtein_mergeSummarize)
        which contains a dict with (key: Gene, Value: Gene Synonyms, proteins)
return a dict: (key: gene or gene synonyms or proteins; value: gene official name)
'''
def buildDictGeneOFFicialAsValues(geneProteinFname):
    if (os.path.exists(geneProteinFname)):
        geneSynonymsProtein2GeneDict = {}
        with open(geneProteinFname, 'rb') as f_rConn:
            allLines = f_rConn.readlines()
            for line in allLines:
                line = line.strip()
                if (line[0] == '#' or line == ''):
                    continue
                allValueList = line.split('\t')
                keyValue = allValueList[0].strip()
                key = keyValue.lower()
                if (key not in geneSynonymsProtein2GeneDict.keys()):
                    geneSynonymsProtein2GeneDict[key] = keyValue
                geneSynonyms = allValueList[1]
                if (geneSynonyms != '-'):
                    insertGeneSynonmsIntoDict(geneSynonyms, '|', keyValue, geneSynonymsProtein2GeneDict)
                proteins = allValueList[2]
                if (proteins != '-'):
                    insertProteinIntoDict(proteins, '|', keyValue, geneSynonymsProtein2GeneDict)
        pass
    return geneSynonymsProtein2GeneDict

def insertGeneSynonmsIntoDict(geneSynonyms, delimeter, keyValue, geneSynonymsProtein2GeneDict):
    GeneList = geneSynonyms.split(delimeter)
    for gene in GeneList:
        key = gene.lower()
        if (key not in geneSynonymsProtein2GeneDict.keys()):
            geneSynonymsProtein2GeneDict[key] = keyValue
            pass
        pass
    pass

def insertProteinIntoDict(proteins, delimeter, keyValue, geneSynonymsProtein2GeneDict):
    proteinList = proteins.split(delimeter)
    curProteinSet = set()
    for proteinAndShortname in proteinList:
        ## Get the proteinName and corresponding shortName
        proteinAndShortname = proteinAndShortname.strip()
        proteinShortnameList = proteinAndShortname.split('#')
        for protein in proteinShortnameList:
            ## Get the first half elems if the full protein too long
            ## halfProtein = GetHalfLenOfProtein(protein, ' ')
            halfProtein = protein.strip()
            curProteinSet.add(halfProtein)
            pass
        pass
    for elem in curProteinSet:
        elem = elem.strip()
        key = elem.lower()
        if (key not in geneSynonymsProtein2GeneDict.keys()):
            geneSynonymsProtein2GeneDict[key] = keyValue
            pass
        pass
    pass

## Get the half length of fullProtein name with split char FS
def GetHalfLenOfProtein(FullProteinName, FS):                                                             
    newHalfProteinName = ''
    proteinList = FullProteinName.split(FS)
    ## if the length is 1 or 2, the new string is the original string
    ## else, the return string is half length of the original string
    numOfElem = (len(proteinList) + 1)/2
    if (numOfElem == 1): 
        newHalfProteinName = FullProteinName
    else:
        k = 1 
        while (k <= numOfElem):
            newHalfProteinName += proteinList[k-1] + ' ' 
            k += 1
    return newHalfProteinName.strip()
