#-------------------------------------------------------------------------------
# Name:        scrapy
# Purpose:
# Author:      jack_mhdong
# Created:     07-09-2014
# Copyright:   (c) jack_mhdong 2014
#-------------------------------------------------------------------------------
# -- coding: utf-8 --

import requests, time
from bs4 import BeautifulSoup

BaseDir = u'/home/jack/'

class scrapyProteinGene:
    def __init__(self):
        self.CODE = u'utf-8'
        self.user_agent = u'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
        self.headers = {u'User-Agent': self.user_agent}
        self.ProteinUrl = ''
        self.timeout= 15
        self.proxies = {}
        self.errorLogFile = BaseDir + u'Workspaces/expPPI/log/errorOfScrapyProteinGene.log'

    def setProteinName(self, proteinName):
        self.proteinName = proteinName
        baseUrl = u'http://www.uniprot.org/uniprot/%s'
        self.ProteinUrl = baseUrl % self.proteinName
        pass

    def getProteinGeneFromURL(self):
        ## KeyWrod: Official proteinName
        ## get FullProtein Name, short names/GeneName Official Name, alias name/Organism
        soup = self.getProteinDetails()
        if soup is None:
            warnInfo = '[%s]. requests is not Existed.\n' % (self.proteinName)
            self.writeErrorMsgIntoLog(warnInfo)
            return None
        names_and_taxonomy = soup.find('div', class_='section', id="names_and_taxonomy")
        ##################################################
        # Protein Official Name
        SummaryProteinInfo = self.proteinName
        if names_and_taxonomy is not None:
            table = names_and_taxonomy.find('table', {'class': 'databaseTable'})
            ####################################################################
            ## The first tr: including recommended name and responding short name
            TrCurContents = table.find('tr')
            ## print table.prettify()
            divProteinNames = TrCurContents.find(name='div')
            if ((table is not None) and (divProteinNames is not None)):
                ##################################################
                ## recommended name
                recommended_nameSpan = divProteinNames.find('span', class_="recommended-name")
                if (recommended_nameSpan.contents != None):
                    recommended_name = recommended_nameSpan.contents[0].get_text()
                    ## print divProteinNames.prettify()
                    ## print("\n\n")
                    SummaryProteinInfo += "\t" + recommended_name
                    ##################################################
                    ## changed to next 'div' Tag
                    curAlternativeTag = recommended_nameSpan
                    while (curAlternativeTag != None and curAlternativeTag.name != 'div'):
                        curAlternativeTag = curAlternativeTag.nextSibling
                        pass
                    ## Get recommended name's short name, as Q9UKV8 (if existed)
                    recommendedShortName = ''
                    if (curAlternativeTag != None):
                        spanText = curAlternativeTag.get_text()
                        spanText = spanText.strip()
                        while ((curAlternativeTag != None) and cmp(spanText, 'Short name:') == 0):
                            curAlternativeTag = curAlternativeTag.nextSibling
                            recommendedShortName += '#' + curAlternativeTag.contents[0]
                            curAlternativeTag = curAlternativeTag.nextSibling
                            if (curAlternativeTag != None):
                                spanText = curAlternativeTag.get_text()
                                spanText = spanText.strip()
                            pass
                    if (recommended_name != ''):
                        SummaryProteinInfo += recommendedShortName
                        pass
                    pass
                ##########################################################################
                ## Alternative names(s) and corresponding short name
                ## need to improve (Q9UKV8)
                AlterNativeNames = divProteinNames.findAll('div', {"class": "listify"})
                AlterNative_ShortNames = ''
                for curAlterNativeName in AlterNativeNames:
                    alterNms = curAlterNativeName.contents
                    ## Add Alternative names into summary
                    AlterNative_ShortNames +=  '|' + alterNms[0].string
                    ## if has short name
                    if (len(alterNms) > 2):
                        curShortNameTag = alterNms[1]
                        curTagText = curShortNameTag.get_text().strip()
                        ## find the location of 'short name:'
                        while (curShortNameTag != None and curShortNameTag.name != 'div' and cmp(curTagText, 'Short name:') != 0):
                            curShortNameTag = curShortNameTag.nextSibling
                            if (curShortNameTag == None):
                                break;
                            curTagText = curShortNameTag.get_text().strip()
                        ## keeping save the short names
                        while (curShortNameTag != None and cmp(curTagText, 'Short name:') == 0):
                            curShortNameTag = curShortNameTag.nextSibling
                            divContents = curShortNameTag.contents
                            AlterNative_ShortNames += '#' + divContents[0]
                            if (curShortNameTag != None and curShortNameTag.nextSibling != None):
                                curShortNameTag = curShortNameTag.nextSibling
                                curTagText = curShortNameTag.get_text().strip()
                            else:
                                break
                    curAlterNativeName = curAlterNativeName.nextSibling
                    pass
                if (AlterNative_ShortNames != ''):
                    SummaryProteinInfo += AlterNative_ShortNames
                pass
            ##################################################
            ## Gene Official names and corresponding Synonyms
            TrCurContents = TrCurContents.nextSibling
            geneTD = TrCurContents.find('td', class_="noBorders")
            ## print geneTD.prettify()
            if (geneTD is not None):
                geneOfficialName = geneTD.find('strong', {"property": "schema:name"})
                ## whether the structure has label a or not
                if (geneOfficialName.a is not None):
                    SummaryProteinInfo += "\t" + geneOfficialName.a.get_text()
                else:
                    SummaryProteinInfo += "\t" + geneOfficialName.get_text()
                curGeneSynonymsNames = geneTD.findAll('span', {"property": "schema:alternativeName"})

                for curGene in curGeneSynonymsNames:
                    SummaryProteinInfo += "|" + curGene.get_text()
                    pass

            ##################################################
            SummaryProteinInfo += "\n"
        else:
            warnInfo = '[%s]. Warn Message. Non Existed.\n' % (self.proteinName)
            self.writeErrorMsgIntoLog(warnInfo)
            return None
        return SummaryProteinInfo
    
    def writeErrorMsgIntoLog(self, errorInfo):
        error_msg_c = open(self.errorLogFile, 'a')
        error_msg_c.write(errorInfo)
        error_msg_c.close()
        pass
    
    def getProteinDetails(self):
        openUrlCount = 1
        RequestFlag = True
        while RequestFlag:
            try:
                response = requests.get(self.ProteinUrl,
                                headers = self.headers,
                                timeout=self.timeout)
            except requests.exceptions.Timeout as e:
                # Maybe set up for a retry, or continue in a retry loop
                time.sleep(3)
                errorInfo = '[%s]. Error Message[%s]\n' % (self.ProteinUrl, e)
                if (openUrlCount <= 5):
                    print("[%d times]Try again. [%s]" % (openUrlCount, errorInfo))
                    openUrlCount += 1
                    continue
                self.writeErrorMsgIntoLog(errorInfo)
                # ---------------------
                # raise ConnectionError(e) ConnectionError: Write into log file
                # ---------------------
                RequestFlag = False
                pass
            except requests.exceptions.TooManyRedirects as e:
                # Tell the user their URL was bad and try a different one
                errorInfo = '[%s]. Error Message[%s]\n' % (self.ProteinUrl, e)
                if (openUrlCount <= 5):
                    print("[%d times]Try again. [%s]" % (openUrlCount, errorInfo))
                    openUrlCount += 1
                    continue
                self.writeErrorMsgIntoLog(errorInfo)
                # ---------------------
                # raise ConnectionError(e) ConnectionError: Write into log file
                # ---------------------
                RequestFlag = False
                pass
            except requests.exceptions.RequestException as e:
                errorInfo = '[%s]. Error Message[%s]\n' % (self.ProteinUrl, e)
                if (openUrlCount <= 5):
                    print("[%d times]Try again. [%s]" % (openUrlCount, errorInfo))
                    openUrlCount += 1
                    continue
                self.writeErrorMsgIntoLog(errorInfo)
                # ---------------------
                # raise ConnectionError(e) ConnectionError: Write into log file
                # ---------------------
                RequestFlag = False
                pass
            else:
                soup = BeautifulSoup(response.content)
                return soup
            pass
        return None
    
    def getProteinName(self):
        return self.proteinName
    
    def getProteinAndGene(self, proteinName):
        self.setProteinName(proteinName)
        tryConnTimes = 1
        proteinAllInfo = self.getProteinGeneFromURL()
        while (proteinAllInfo is None and tryConnTimes <= 3):
            proteinAllInfo = self.getProteinGeneFromURL()
            tryConnTimes += 1
            pass
        # ---------------------
        ### unicode exchange
        # ---------------------
        return proteinAllInfo.encode('utf-8')

def getAllProtein(srcFile, dstFile):
    HeadLine = "# ProteinName\tFullName|Alternative Name(s)|Short Name\tGene Name|Gene Synonyns\n"

    ReadConn = open(srcFile, 'r')
    outLine = ReadConn.readline()
    scrapyPG = scrapyProteinGene()

    WriteConn = open(dstFile, 'w')
    WriteConn.write(HeadLine)
    resetProteinSet = set()
    while (outLine):
        ProteinName = outLine.strip()
        if (ProteinName[0] == '#'):
            outLine = ReadConn.readline()
            continue
        proteinAllInfo = scrapyPG.getProteinAndGene(ProteinName)
        if proteinAllInfo is not None:
            # ---------------------
            ### unicode exchange
            # ---------------------
            WriteConn.write(proteinAllInfo)
            print("Finish deal with protein %s." % ProteinName)
        else:
            resetProteinSet.add(ProteinName)
            print("Error in Deal with protein %s!!!" % ProteinName)
        outLine = ReadConn.readline()
        pass
    
    ## Try another chance.
    tryResetProteinTimes = 0
    while (len(resetProteinSet) > 0 and tryResetProteinTimes <= 3):
        for ProteinName in resetProteinSet:
            proteinAllInfo = scrapyPG.getProteinAndGene(ProteinName)
            if proteinAllInfo is not None:
                WriteConn.write(proteinAllInfo.encode('utf-8'))
                resetProteinSet.remove(ProteinName)
                print("Finish deal with protein %s." % ProteinName)
            else:
                print("Error in Deal with protein %s!!!" % ProteinName)
            pass
        tryResetProteinTimes += 1
        pass
    WriteConn.close()
    ReadConn.close()
    
    AllInvalidProteins = "# ProteinName"
    for ProteinName in resetProteinSet:
        AllInvalidProteins += "\n" + ProteinName
        pass
    warnLogFile = BaseDir + u'Workspaces/expPPI/data/warningOfscrapyProteinGene.log'
    WriteConn = open(warnLogFile, 'w')
    WriteConn.write(AllInvalidProteins)
    WriteConn.close()
    pass

def main():
    srcProteinFile = BaseDir + u'Workspaces/expPPI/data/UniqueProteinName_201108.intm'
    writeLogFile = BaseDir + u'Workspaces/expPPI/data/proteinGene_201108.intm'
    #getAllProtein(srcProteinFile, writeLogFile)

    scrapyPG = scrapyProteinGene()
    proteinName = scrapyPG.getProteinAndGene("P30085") ## P62988 P30085 P03897 Q9UKV8 O95232
    print(proteinName)

if __name__ == '__main__':
    main()