#encoding: utf-8
#-------------------------------------------------------------------------------
# Name:        preprocessing
# Purpose:
# Author:      jack_mhdong
# Created:     02-Dec-2014
# Copyright:   (c) jack_mhdong 2014
#-------------------------------------------------------------------------------

import sys
sys.path.append("/home/jack/Workspaces/pubmedExtraction")
from config import config
from function import *



para = config.Parameter()

if para.__PUBMEDTEXTFLAG__ == True:
    (pubmedIdSet, pubmedInteractionProteinDict) = getAllPubmedIdAndPubmedId2Proteins(
                                                        para.humanDbAll201108, "\t", 4)
    saveAllSetValueIntoFname(pubmedIdSet,
                            para.uniquePubmedid_201108,
                            "# Pubmedid (%d)\n" % len(pubmedIdSet))
    print("Finish save unique pubmed id into file %s" % para.uniquePubmedid_201108)
    print("---------------------------------------------------\n")


if (para.__PUBMEDTEXTFLAG__ == True):
    uniquePubmedIdSet = getUniquePubmedIdText(pubmedIdSet, para.pubmedSrcTextData, para.pubmedDstTextData)
    saveAllSetValueIntoFname(uniquePubmedIdSet,
                                para.unfindedPubmedIdInSrcTextFname,
                                '# unfinded pubmedID (%d)\n' % len(uniquePubmedIdSet))
    saveAllDictValueIntoFname(pubmedInteractionProteinDict,
                                para.pubmedid2Protein_201108,
                                "# Pubmedid\tProt1|Prot2 (%d)\n" % len(pubmedInteractionProteinDict))
    print("Finish save pubmedid-protein into file %s" % para.pubmedid2Protein_201108)
    print("---------------------------------------------------\n")
    

if (para.__RESULTFLAG__ == True):
    Protein2GeneDict = getOfficialProteinGene(para.proteinGeneFile, "\t", 1, 3)
    saveAllDictValueIntoFname(Protein2GeneDict,
                                para.protein2Gene_201108,
                                "# Protein\tGene (%d)\n" % len(Protein2GeneDict))
    print("Finish save protein-gene into file %s" % para.protein2Gene_201108)
    print("---------------------------------------------------\n")
    
    (pubmedInteractionGeneDict, proteinHasnotGeneSet) = getPubmedId2GeneList(
                                                                pubmedInteractionProteinDict,
                                                                ",", Protein2GeneDict)
    saveAllDictValueIntoFname(pubmedInteractionGeneDict,
                                para.pubmedid2Gene_201108,
                                "# Pubmedid\tGene1|Gene2 (%d)\n" % len(pubmedInteractionGeneDict))
    print("Finish save proteinid-gene into file %s" % para.pubmedid2Gene_201108)
    print("---------------------------------------------------\n")
    
    saveAllSetValueIntoFname(proteinHasnotGeneSet, para.proteinHasNotGene, 
                                "# ProteinHasnotGene\n")
    print("Finish save proteinid which has not corresponding Gene. [%s]" % para.proteinHasNotGene)
    print("---------------------------------------------------\n")
    
if para.__GENEPROTEINSUM__ == True:
    GeneProteins_GeneSynonymsDict = getDictWithGeneAsKeyProteins_GeneSynonymsAdValues(
                                    para.proteinGeneFile,
                                    para.simpleGeneInfo_HomoSapiens)
    saveAllDictValueIntoFname(GeneProteins_GeneSynonymsDict,
                    para.geneProtein_mergeSummarize,
                    '# Gene_Official\tGene_Synonyms\tProteinList_ProteinAlternativeName (%d)\n' % len(GeneProteins_GeneSynonymsDict))
    print("Finish save Gene and Proteins. [%s]" % para.geneProtein_mergeSummarize)
    print("---------------------------------------------------\n")
    
if para.__RESULTFILE__ == True:
    geneSynonymsProtein2GeneDict = buildDictGeneOFFicialAsValues(para.geneProtein_mergeSummarize)
    
    saveAllDictValueIntoFname(geneSynonymsProtein2GeneDict,
                              para.dictOfAllGeneProteinFname,
                              "# ProteinGene\tGene (%d)\n" % len(geneSynonymsProtein2GeneDict))
    allKeysSet = set(geneSynonymsProtein2GeneDict.keys())
    saveAllSetValueIntoFname(allKeysSet,
                              para.keysOfAllGeneProteinFname, 
                              "# keyOfProteinAndGene (%d)\n" % len(allKeysSet))
    print("Finish preprocessing for Proteins and Gene (dict). [%s]" % para.dictOfAllGeneProteinFname)
    print("---------------------------------------------------\n")
    print("Finish preprocessing for Proteins and Gene (set). [%s]" % para.keysOfAllGeneProteinFname)
    print("---------------------------------------------------\n")
    
