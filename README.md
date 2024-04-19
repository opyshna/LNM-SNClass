![alt text](https://github.com/opyshna/LNM-SNClass/blob/main/Logo.png)
# LNM-SNClass
Large Number of Models Supernova Classifier based on SNCosmo models[^1]

- Method development: opyshna

- Code development: vlad2305m

[^1]: DOI 10.5281/zenodo.592747

## Installation
```fish
pip install redback sncosmo bilby selenium lxml nestle iminuit progress openpyxl
```
## Usage
Need an excel with SN names (ZTF) in first column, starting at 2nd row
```sh
python ./Lasair_type_getter.py ./ztfs.xlsx
```
Inside folder for the results:
```sh
python ./analysis.py ./ztfs.xlsx
```
```sh
python ./visualization.py ./ZTF23aamanim_z_guessed_SN\ Ib.csv
```
In a folder that contains results (searched recursively):
```sh
python ./mass_visualization.py ./ztfs.xlsx
```
