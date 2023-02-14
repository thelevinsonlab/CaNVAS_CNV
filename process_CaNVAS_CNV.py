#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'cd
import argparse

def renameColumns(columnHeader):
    if "Log R Ratio" in columnHeader:
        return  "logRratio"
    elif "B Allele Freq" in columnHeader:
        return "BAF"
    elif "GType" in columnHeader:
        return "Genotype"
    else:
        return columnHeader

def process_CNVs(inputfile, inputpath, outputfile, outputpath):
	cnvInputFile=pd.read_csv(inputfile, delim_whitespace=True, dtype={"Chr": object, "CNVStart":int,"CNVEnd":int,"LeftStart":int,"LeftEnd":int,"RightStart":int,"RightEnd":int,})
	cnvInputFile['CNVID']=cnvInputFile['Chr'].map(str)+"_"+cnvInputFile['CNVStart'].map(str)+"_"+cnvInputFile['CNVEnd'].map(str)
	outDF= pd.DataFrame()
	print("Processing CNVs")
	with os.scandir(inputpath) as entries:
	   for entry in entries:
	    	print(entry)
	    	genotypeInput=pd.read_csv(entry, sep='\t', low_memory=False)
	    	genotypeInput.rename(mapper = renameColumns, axis = 'columns', inplace = True)
	    	genotypeInput[["Position","BAF","logRratio"]] = genotypeInput[["Position","BAF","logRratio"]].apply(pd.to_numeric, errors='coerce')
	    	bothInput=pd.merge(genotypeInput,cnvInputFile,on='Chr')
	    	if "Genotype" in bothInput.columns:
	    		bothInput= bothInput.loc[bothInput['Genotype'] != "NC"]
	    	inCNV=bothInput[bothInput["Position"].between(bothInput["CNVStart"], bothInput["CNVEnd"])]
	    	leftCNV=bothInput[bothInput["Position"].between(bothInput["LeftStart"], bothInput["LeftEnd"])]
	    	rightCNV=bothInput[bothInput["Position"].between(bothInput["RightStart"], bothInput["RightEnd"])]
	    	SNPin_size=inCNV.groupby(['CNVID']).size()
	    	SNPleft_size=leftCNV.groupby(['CNVID']).size()
	    	SNPright_size=rightCNV.groupby(['CNVID']).size()
	    	inCNV_sum=inCNV.groupby(['CNVID'])['logRratio'].median()
	    	leftCNV_sum=leftCNV.groupby(['CNVID'])['logRratio'].median()
	    	leftCNV_sum.rename("medLRROutleft", inplace=True)
	    	rightCNV_sum=rightCNV.groupby(['CNVID'])['logRratio'].median()
	    	rightCNV_sum.rename("medLRROutright", inplace=True)
	    	inCNV_mean=inCNV.groupby(['CNVID'])['logRratio'].mean()
	    	inCNV_mean.rename("meanLRRIn", inplace=True)
	    	leftCNV_mean=leftCNV.groupby(['CNVID'])['logRratio'].mean()
	    	leftCNV_mean.rename("meanLRROutleft", inplace=True)
	    	rightCNV_mean=rightCNV.groupby(['CNVID'])['logRratio'].mean()
	    	rightCNV_mean.rename("meanLRROutright", inplace=True)
	    	inCNV['BAF_bins']=pd.cut(inCNV.BAF,[0,0.005,0.29,0.37,0.47,0.53,0.63,0.71,0.995,1], include_lowest=True, ordered=False, labels=pd.Categorical(['Homozygote',"None","Trisomic","None","Disomic","None","Trisomic","None","Homozygote"]))
	    	BAFbin_size=inCNV.groupby(['CNVID',"BAF_bins"], as_index=False).count()
	    	relBAFbin_size=BAFbin_size[['CNVID', 'BAF_bins',"Name"]]
	    	relBAFbin_size2=relBAFbin_size.pivot(index='CNVID', columns='BAF_bins', values='Name')
	    	aggregate_df=pd.concat([SNPin_size, SNPleft_size, SNPright_size, inCNV_sum, leftCNV_sum, rightCNV_sum, inCNV_mean, leftCNV_mean, rightCNV_mean,relBAFbin_size2], axis=1)
	    	aggregate_df.columns=["SNPsIn","SNPsOutleft","SNPsOutright","medianLRRIn","medianLRROutleft","medianLRROutright","meanLRRIn","meanLRROutleft","meanLRROutright","BAFDisomic","BAFHomozygote","None","BAFTrisomic"]
	    	aggregate_df["SubjectID"]=str(entry).replace("<DirEntry '", "").replace("'>","")
	    	outDF=outDF.append(aggregate_df)
	    	for cnv in outDF.index.unique():
	    		outpath=outputpath+"/"+cnv+"_"+outputfile+".txt"
	    		rel = outDF[outDF.index ==cnv]
	    		rel.index.name = 'CNVID'
	    		rel.reset_index(inplace=True)
	    		rel[["CNVID","SubjectID","meanLRRIn","meanLRROutleft","meanLRROutright","medianLRRIn","medianLRROutleft","medianLRROutright","BAFHomozygote","BAFTrisomic","BAFDisomic","SNPsIn", "SNPsOutleft","SNPsOutright"]].to_csv(outpath, sep="\t", index=False)
	   outDF.index.name = 'CNVID'
	   outDF.reset_index(inplace=True)
	   outDF.rename(columns={outDF.columns[1]: "SNPsIn",outDF.columns[2]: "SNPsOutleft",outDF.columns[3]: "SNPsOutright",outDF.columns[4]:"medianLRRIn", outDF.columns[5]:"medianLRROutleft", outDF.columns[6]:"medianLRROutright",outDF.columns[7]:"meanLRRIn", outDF.columns[8]:"meanLRROutleft", outDF.columns[9]:"meanLRROutright", outDF.columns[10]: "BAFDisomic",outDF.columns[11]: "BAFHomozygote",outDF.columns[12]: "None",outDF.columns[13]: "BAFTrisomic",outDF.columns[14]: "SubjectID"}, inplace=True)
	print("Finished CNV Processing")
	return outDF

def main(argv):
	parser = argparse.ArgumentParser()
	parser.add_argument('-infile', type=str)
	parser.add_argument('-inpath', type=str)
	parser.add_argument('-outfile', type=str)
	parser.add_argument('-outpath', type=str)
	args = parser.parse_args()
	inputfile = args.infile
	inputpath = args.inpath
	outputfile = args.outfile
	outputpath = args.outpath
	outDF=[]
	print('Input file is "'+inputfile+'"')
	print('Input path is "'+inputpath+'"')
	print('Output files will be written to "'+outputpath+'/'+outputfile+'"')
	if not os.path.exists(outputpath):
		os.makedirs(outputpath)
	if not os.path.exists(outputpath+'/plots/'):
		os.makedirs(str(outputpath+'/plots/'))
	process_CNVs(inputfile, inputpath, outputfile, outputpath)
	



if __name__ == "__main__":
   main(sys.argv[1:])