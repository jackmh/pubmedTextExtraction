#encoding: utf-8
'''
Created on Dec 2, 2014
@author: jack
'''

class Parameter:
    def __init__(self):
        
        self.__DEBUG__ = False
        self.__TESTDEBUG__ = False
        
        self.BaseDir = u'/home/jack/'
        self.TestDir = u'/home/jack/Workspaces/expPPI/test/'
        
        ##########################################################################################
        self.srcFileDir = self.BaseDir + u'Workspaces/expPPI/data/'
        ''' 所有人类蛋白质数据库中相互作用的蛋白质以及对应的 pubmedID '''
        self.humanDbAll201108 = self.srcFileDir + u'human.db.all.201108.intm'
        ''' 从上文件中抽取出相互作用对的所有蛋白质 '''
        self.uniqueProteinFile = self.srcFileDir + u'UniqueProteinName_201108.intm'
        ''' 由相互作用对的蛋白质, 爬取出此蛋白质对应的全称、别名、缩写以及对应的基因名 '''
        self.proteinGeneFile = self.srcFileDir + u'proteinGene_201108.intm'
        if (self.__TESTDEBUG__ == True):
            self.proteinGeneFile = self.TestDir + u'proteinGene_201108.intm'
        ''' 失效的蛋白质 '''
        self.notExistedProteinFile = self.srcFileDir + u'notExistedProteinName_201108.intm'
        
        ##########################################################################################
        self.logFileDir = self.BaseDir + u'Workspaces/expPPI/log/'
        ''' 爬取蛋白质出现的错误日志文件 '''
        self.errorLogFile = self.logFileDir + u'errorOfScrapyProteinGene.log'
        '''此蛋白质没有对应的基因日志文件'''
        self.warnProteinHasNotGene = self.logFileDir + u'proteinHasnotCorrespondingGene.log'
        
        ##########################################################################################
        self.__RESULTFLAG__ = False
        self.preliminaryResultDir = self.BaseDir + u'Workspaces/expPPI/resultData/'
        ''' 蛋白质对应的基因文件，相当于字典(key: Protein, value: Gene) '''
        self.protein2Gene_201108 = self.preliminaryResultDir + u'protein2Gene_201108.intm'
        ''' 包含相互作用的蛋白质的pubmed id '''
        self.uniquePubmedid_201108 = self.preliminaryResultDir + u'uniquePubmedId_201108.intm'
        ''' 包含pubmed id中对应的蛋白质相互作用对，字典(key: pubmedid, value: protein interaction pair) '''
        self.pubmedid2Protein_201108 = self.preliminaryResultDir + u'pubmedId2Protein_201108.intm'
        ''' 包含pubmed id中对应的基因相互作用对，字典(key: pubmedid, value: Gene interaction pair) '''
        ''' 也即由蛋白质和基因对转换成如下文件 '''
        self.pubmedid2Gene_201108 = self.preliminaryResultDir + u'pubmedId2Gene_201108.intm'
        '''保存蛋白质列表，此蛋白质没有对应的基因'''
        self.proteinHasNotGene = self.preliminaryResultDir + u'proteinHasnotCorrespondingGene.intm'
        
        ############################################################################################\
        self.__PUBMEDTEXTFLAG__ = False
        '''包含所有pubmed text的源文件'''
        self.pubmedSrcTextData = u'/home/jack/keTiInHIT_FROM2014_08/srcData'
        # self.pubmedSrcTextData = '/home/jack/Workspaces/expPPI/test'
        ''' 此文件夹中存放包含所有存在相互作用蛋白质对的pubmedid对应的摘要 '''
        self.pubmedDstTextData = self.BaseDir + u'Workspaces/expPPI/pubmedtextData'
        '''保存在srcTextData目录文件下不存在的文件'''
        self.unfindedPubmedIdInSrcTextFname = self.preliminaryResultDir + u'unFindedPubmedIdTextFromSrcData.intm'
        ############################################################################################
        
        self.__GENEPROTEINSUM__ = False
        '''汇总所有的基因和对应的蛋白质， 输入包含两个文件
            proteinGene_201108.intm: 包含所有的蛋白质，全称，缩写和对应的Gene (scrapy) (self.proteinGeneFile)
            simpleGeneInfo.HomoSapiens: 包含人类所有的GeneID, Symbol, Gene Synonyms
            存入文件: geneProtein_HomoSapines.mergeSummarize (self.geneProtein_mergeSummarize)
        '''
        self.simpleGeneInfo_HomoSapiens = self.srcFileDir + u'simpleGeneInfo.HomoSapiens'
        self.geneProtein_mergeSummarize = self.preliminaryResultDir + u'geneProtein_HomoSapines.mergeSummarize'
        if (self.__TESTDEBUG__ == True):
            self.simpleGeneInfo_HomoSapiens = self.TestDir + u'simpleGeneInfo.HomoSapiens'
            self.geneProtein_mergeSummarize = self.TestDir + u'geneProtein_HomoSapines.mergeSummarize'
        ############################################################################################
        
        ### Result File
        self.__RESULTFILE__ = True
        self.keysOfAllGeneProteinFname = self.preliminaryResultDir + 'keysOfAllMergeGeneProteins.name'
        self.dictOfAllGeneProteinFname = self.preliminaryResultDir + 'dictOfAllMergeGeneProtein.name'
        
        
        
        
        
        
        
        
        
        
        