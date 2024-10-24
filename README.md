# SRIM simulation automatized for Mac users (under development)

## ATTENTION:

This work is under development and it is based on pysrim library: (https://github.com/costrouc/pysrim/tree/master)

It was necessary to do some changes in the original codes. 
This code is not complete either but it implements an automatization basen on an input file (.txt) provided by user. 

#### Table of Contents
1. [Introduction](#ATTENTION)
2. [Installing SRIM in MacOS (or linux)](#installing-srim-in-macos-or-linux)
3. [Edits in original pysrim (edited files found inside "srim" folder)](#Edits-in-original-pysrim-(edited-files-found-inside-"srim"-folder))
4. [License](#license)

   
## Installing SRIM in MacOS (or linux)

All steps from TUTORIAL are detailed below: ( https://www.youtube.com/watch?v=YsCMZK6bUDI ) 

(color code below)

  - Acess http://www.srim.org
  
  - Select > Download SRIM-2013 <
  
  - Select > SRIM-2013 (Professional) <
  
  - Rename extension : SRIM-2013-Pro **.e** =>   SRIM-2013-Pro **.exe**

__

Install wine on mac: 
https://github.com/Gcenx/wine-on-mac
  - Open terminal: > $\textcolor{teal}{\text{brew tap gcenx/wine
brew install --cask --no-quarantine wine-crossover}}$

__

  - Open SRIM folder in terminal: >  $\textcolor{purple}{\text{SRIM/}}$ : $\textcolor{teal}{\text{wineconsole SRIM-2013-Pro.exe}}$ 

  - A pop-up window should open. Select " Extract " button. 

  - Once it is complete: press "ok" and "done"

  - Acess " SRIM-Setup " folder > $\textcolor{purple}{\text{SRIM/SRIM}}$ _ $\textcolor{purple}{\text{Setup/}}$ : $\textcolor{teal}{\text{wineconsole\ " }}$ _ $\textcolor{teal}{\text{SRIM.Setup (Right-Click).bat\ "}}$ 

  - Press any key. (Repeat this step if necessary, following terminal instructions)

  - Open "Linedraw.ttf" and select "install"

  - Go back to "SRIM" folder : $\textcolor{purple}{\text{SRIM/}}$ : $\textcolor{teal}{\text{wineconsole SRIM.exe}}$  

A pop-up window should open with SRIM Main Menu !
  
  **INSTALLATION COMPLETE**

Color code: 

 [ $\textcolor{teal}{\text{this color text represents terminal commands}}$ $\textcolor{teal}{\text{commands}}$ ]

 [ $\textcolor{purple}{\text{this color text represents terminal directory}}$ $\textcolor{purple}{\text{directory}}$ ]


## Edits in original pysrim (edited files found inside "srim" folder): 

### @ input.py:

@ _write_ion()

    self._trim.ion.energy / 1000.0, # eV

    #became:
    self._trim.ion.energy
    
@ _write_bragg_correction()

    return (
        'Target Compound Corrections (Bragg)'
            ) + self.newline + 
            ' 1' * len(self._trim.target.layers)   #before
            + self.newline

   #became:
   
   return (
        'Target Compound Corrections (Bragg)'
            ) + self.newline + 
            str(self._trim.settings.bragg_correction)    #after
            + self.newline

### @ output.py

@ _read_num_ions()

    return int(float(match.group(1)))

    #became:
    return int(float(match.group(1).replace(b',', b'.')))

@ \__init__()

    # add:
    self._data = data

### @ elementdb.py

@ create_elementdb()

    return yaml.load(open(dbpath, "r"))

    #became:
    return yaml.load(open(dbpath, "r"), Loader=yaml.FullLoader)


# How to use:

You can use the srim folder to replace the srim (pysrim) folder you have installed in your computer 

or 

you can locate that folder and replace the few changes listed above @ " Edits in original pysrim "

__________________________________

To run the automatized python code: 

You can clone the repository in vscode with the GitHub link (for example)

or

you can download the files (SRIM_simulation.ipynb , aux_functions.py , simulation_lib.py , ...) in your SRIM directory where you find SRIM.exe / TRIM.exe .
If you decide to create a new folder, remember to edit the directory paths in your SRIM_simulation.ipynb notebook.


Open the Jupyter notebook script (SRIM_simulation.ipynb) using vscode with Jupyter extension or with anaconda navigator.

Get familiarized with the code structure.

Create your input_list.txt based on the example or edit the code accordingly to accept your customized input format. 

To execute the code: 
Run all cells ("__Run all__" button or __shift + enter__ to run individual cells)

__ATTENTION:__ if you need to edit anything in the auxilary functions files ( aux_functions.py , simulation_lib.py ), you should save the edits and reload the libraries by running a cell with the following script on top: 

      reload(simulation_lib); from simulation_lib import *  
      reload(aux_functions); from aux_functions import *



