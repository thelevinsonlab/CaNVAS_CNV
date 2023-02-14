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
		#below enter the name of the variable you wish to plot on the X axis
		x1=dat["medianLRRIn"]
		x2 = dat["medianLRROutleft"]
		x3 = dat["medianLRROutright"]
		y1 = dat["BAFHomozygote"]
		y2 = dat["BAFTrisomic"]
		y3 = dat["BAFDisomic"]
		x4 = x1-x2
		x5 = x1-x3
		fig=make_subplots(rows=4, cols=3)
#here is where we add the subplots to the plot
		fig.add_trace(go.Scatter(x=dat["SubjectID"], y=x1, mode="markers",text=dat.SubjectID,hoverinfo='text'), row=1, col=1)
		fig.add_trace(go.Scatter(x=dat["SubjectID"], y=x2, mode="markers",text=dat.SubjectID,hoverinfo='text'), row=1, col=2)
		fig.add_trace(go.Scatter(x=dat["SubjectID"], y=x3, mode="markers",text=dat.SubjectID,hoverinfo='text'), row=1, col=3)
		fig.add_trace(go.Scatter(x=x1, y=x2, mode="markers",text=dat.SubjectID,hoverinfo='text'), row=2, col=1)
		fig.add_trace(go.Scatter(x=x1, y=x3, mode="markers",text=dat.SubjectID,hoverinfo='text'), row=2, col=2)
		fig.add_trace(go.Scatter(x=x1-x2, y=y1, mode="markers",text=dat.SubjectID,hoverinfo='text'), row=3, col=1)
		fig.add_trace(go.Scatter(x=x1-x2, y=y2, mode="markers",text=dat.SubjectID,hoverinfo='text'), row=3, col=2)
		fig.add_trace(go.Scatter(x=x1-x2, y=y3, mode="markers",text=dat.SubjectID,hoverinfo='text'), row=3, col=3)
		fig.add_trace(go.Scatter(x=x1-x3, y=y1, mode="markers",text=dat.SubjectID,hoverinfo='text'), row=4, col=1)
		fig.add_trace(go.Scatter(x=x1-x3, y=y2, mode="markers",text=dat.SubjectID,hoverinfo='text'), row=4, col=2)
		fig.add_trace(go.Scatter(x=x1-x3, y=y3, mode="markers",text=dat.SubjectID,hoverinfo='text'), row=4, col=3)
#here is where you can update the x axis title and labels
		fig.update_xaxes(title_text="Samples", showticklabels=False, row=1, col=1)
		fig.update_xaxes(title_text="Samples", showticklabels=False, row=1, col=2)
		fig.update_xaxes(title_text="Samples", showticklabels=False, row=1, col=3)
		fig.update_xaxes(title_text="MedianLRRIn", row=2, col=1)
		fig.update_xaxes(title_text="MedianLRRIn", row=2, col=2)
		fig.update_xaxes(title_text="MedianLRRIn-MedianLRROutLeft", row=3, col=1)
		fig.update_xaxes(title_text="MedianLRRIn-MedianLRROutLeft", row=3, col=2)
		fig.update_xaxes(title_text="MedianLRRIn-MedianLRROutLeft", row=3, col=3)
		fig.update_xaxes(title_text="MedianLRRIn-MedianLRROutRight", row=4, col=1)
		fig.update_xaxes(title_text="MedianLRRIn-MedianLRROutRight", row=4, col=2)
		fig.update_xaxes(title_text="MedianLRRIn-MedianLRROutRight", row=4, col=3)
#here is where you can update the y axis title and labels
		fig.update_yaxes(title_text="MedianLRRIn", row=1, col=1)
		fig.update_yaxes(title_text="MedianLRROutLeft", row=1, col=2)
		fig.update_yaxes(title_text="MedianLRROutRight", row=1, col=3)
		fig.update_yaxes(title_text="MedianLRROutLeft", row=2, col=1)
		fig.update_yaxes(title_text="MedianLRROutRight", row=2, col=2)
		fig.update_yaxes(title_text="BAFHomozygote", row=3, col=1)
		fig.update_yaxes(title_text="BAFTrisomic", row=3, col=2)
		fig.update_yaxes(title_text="BAFDisomic", row=3, col=3)
		fig.update_yaxes(title_text="BAFHomozygote", row=4, col=1)
		fig.update_yaxes(title_text="BAFTrisomic", row=4, col=2)
		fig.update_yaxes(title_text="BAFDisomic", row=4, col=3)
#here is where you can update the title appearing at the top of the window
		fig.update_layout(height=900, width=1800, title_text="Median Normalized "+f)	
		fig.update_annotations(clicktoshow='onoff')		
		fig.write_html(outputpath+"/plots/median_normalized/"+f+"median_normalized_plot.html")

def main(argv):
	parser = argparse.ArgumentParser()
	parser.add_argument('-path', type=str)
	args = parser.parse_args()
	outputpath = args.path
	if not os.path.exists(outputpath+'/plots/median_normalized/'):
		os.makedirs(str(outputpath+'/plots/median_normalized/'))
	createPlots(outputpath)



if __name__ == "__main__":
   main(sys.argv[1:])