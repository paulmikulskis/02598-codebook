# 02598-codebook

This is a Python3 script that will read the data from the [Survey of Inmates in State and Federal Correctional Facilities, 1997](https://www.icpsr.umich.edu/icpsrweb/ICPSR/studies/2598).  

##### What This Script is Good For
* Exporting data from the 02958 survey into a csv format for use with R or any other data program
* If you are using Python, this script stores the processed data in a dictionary structure, which is easy to use.

##### Usage Notes
* To use the script, download the data in text file format from the survey link, and put it into a folder with this script and the codebook text file.  To run the script, open up a terminal and run the command `./sort.py`.
* If permission is denied when you try to run the file, run the command `sudo chmod 777 sort.py` before running the file to fix.
* When the script is run, it will prompt some questions about what variables in what areas to extract into CSV format for the sake of saving space.  If you want to extract all data, press enter on each step.
* This script only extracts the first 2,085 variables that have numerical answers.
