# CaNVAS_CNV
This folder contains the scripts for processing and plotting of the CaNVAS CNV files. 

---
**Installation and Set-up**

To create and acivate a conda environment in which to run the scripts use the following command. If you do not want to use conda, skip to the section labeled installing packages without conda. 

```console
conda create -n CaNVAS_CNV python=3.9
activate CaNVAS_CNV
```

Then, install the following packages needed for the scripts. 

```console
conda install -c plotly plotly
conda install pandas
conda install numpy
```

To install python packages without the use of conda, use the following commands:

```console
pip install plotly
pip install pandas
pip install numpy
```

**Running CaNVAS_CNV**

To run the CaNVAS CNV processing script use the following syntax:

```console
./process_CaNVAS_CNV.py -infile list_CNV_areas -inpath path_to_genetic_data -outfile output_filename -outpath output_path
```

The CaNVAS CNV script will create one output file for each CNV with the relevant information listed fore each individual for that CNV. The script will also create a folder within the output path that can be used for plotting later. The script has run properly if you see a list of individual names slowly writing to the screen and the output path is created and filled. 

**Plotting output data**

After running the process_CaNVAS_CNV.py script, you may want to plot your data. To do so use the plotCaNVAS.py script. To run the script use the following syntax:
```console
./plotCaNVAS.py -path output_path_containing_CNV_files
```

This script should automatically generate a set of interactive HTML plots for each CNV. 

The default plotting script uses Mean as the independent and dependent variable by default. If you would like to plot Medians, please use the script plotCaNVAS_Medians.py. Syntax is the same as listed above. 
