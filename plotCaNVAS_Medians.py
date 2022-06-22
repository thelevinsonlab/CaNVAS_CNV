#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import getopt
import os
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import argparse

def createPlots(outputpath):
	print("Generating Plots")
	files = [f for f in os.listdir(outputpath) if os.path.isfile(os.path.join(outputpath, f))]
	#with os.scandir(outputpath) as entries:
	for f in files:
		print(f)
		dat=pd.read_csv(outputpath+"/"+f, delim_whitespace=True)
		x=dat["medianLRRIn"]
		y1 = dat["medianLRROutleft"]
		y2 = dat["medianLRROutright"]
		y3 = (dat["medianLRROutleft"] +dat["medianLRROutright"])/2
		y4 = dat["BAFHomozygote"]
		y5 = dat["BAFTrisomic"]
		y6 = dat["BAFDisomic"]
		fig=make_subplots(rows=3, cols=2)
		fig.add_trace(go.Scatter(x=x, y=y1, mode="markers",text=dat.SubjectID,hoverinfo='text'), row=1, col=1)
		fig.add_trace(go.Scatter(x=x, y=y2, mode="markers",text=dat.SubjectID,hoverinfo='text'), row=1, col=2)
		fig.add_trace(go.Scatter(x=x, y=y3, mode="markers",text=dat.SubjectID,hoverinfo='text'), row=2, col=1)
		fig.add_trace(go.Scatter(x=x, y=y4, mode="markers",text=dat.SubjectID,hoverinfo='text'), row=2, col=2)
		fig.add_trace(go.Scatter(x=x, y=y5, mode="markers",text=dat.SubjectID,hoverinfo='text'), row=3, col=1)
		fig.add_trace(go.Scatter(x=x, y=y6, mode="markers",text=dat.SubjectID,hoverinfo='text'), row=3, col=2)
		fig.update_xaxes(title_text="MedianLRRIn", row=1, col=1)
		fig.update_xaxes(title_text="MedianLRRIn", row=1, col=2)
		fig.update_xaxes(title_text="MedianLRRIn",  row=2, col=1)
		fig.update_xaxes(title_text="MedianLRRIn", row=2, col=2)
		fig.update_xaxes(title_text="MedianLRRIn",  row=3, col=1)
		fig.update_xaxes(title_text="MedianLRRIn", row=3, col=2)
		fig.update_yaxes(title_text="MedianLRROutLeft", row=1, col=1)
		fig.update_yaxes(title_text="MedianLRROutRight", row=1, col=2)
		fig.update_yaxes(title_text="AverageMedianLRROut", row=2, col=1)
		fig.update_yaxes(title_text="BAF Homozygote", row=2, col=2)
		fig.update_yaxes(title_text="BAF Trisomic", row=3, col=1)
		fig.update_yaxes(title_text="BAF Disomic", row=3, col=2)
		fig.update_layout(height=1000, width=2000, title_text=f)	
		fig.update_annotations(clicktoshow='onoff')		
		fig.write_html(outputpath+"/plots/median_plots/"+f+"plot.html")

def main(argv):
	parser = argparse.ArgumentParser()
	parser.add_argument('-path', type=str)
	args = parser.parse_args()
	outputpath = args.path
	if not os.path.exists(outputpath+'/plots/median_plots/'):
		os.makedirs(str(outputpath+'/plots/median_plots/'))
	createPlots(outputpath)



if __name__ == "__main__":
   main(sys.argv[1:])