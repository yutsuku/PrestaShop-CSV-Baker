PrestaShop CSV Baker
====================
![Preview](https://gist.githubusercontent.com/yutsuku/53d7eed9ad7bc8158063a394c02fa552/raw/220b35157f73d01f06ac985bac1e05a92481105f/preview.png)

This is a helper tool for bulk importing images into PrestaShop using CSVs. 
Use ";" delimiter and "|" as multiple values delimiter.

Preparations
============
You will need few things to make use of this tool:
- a directory with your images (can contains subdirectories) - jpeg, gif, png
- CSV template

In the template you can use following variables that will be 
replaced by this tool:
- "$ID" - current row
- "$zdjęcie" - relative generated path to currenly processing image

Usage
=====
1. "CSV Wzór" - select CSV template file
2. "CSV Wyjściowy" - output file (will be splitted if neccessary)
2.1 "Limit wierszy" - limit number of rows per file(s)
3. "Obrazki" - select directory with images
4. "Generuj" - Generate CSV(s)
5. "Przejdź do plików" - Open Explorer in the output directory


Building
========
On Windows you will need to change locations of TCL and TK libraries in setup.py