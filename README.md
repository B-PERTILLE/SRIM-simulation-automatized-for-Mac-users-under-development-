# SRIM simulation automatized for Mac users (under development)

## ATTENTION:

This work is under development and it is based on pysrim library: (https://github.com/costrouc/pysrim/tree/master)

It was necessary to do some changes in the original codes. 
This code is not complete either but it implements an automatization basen on an input file (.txt) provided by user. 

#### Table of Contents
1. [Introduction](#introduction)
2. [Installing SRIM in MacOS (or linux)](#installing-srim-in-macos-or-linux)
3. [Usage](#usage)
4. [License](#license)

   
## Installing SRIM in MacOS (or linux)

All steps from TUTORIAL are detailed below: ( https://www.youtube.com/watch?v=YsCMZK6bUDI ) 

(color code below)

  - Acess http://www.srim.org
  
  - Select > Download SRIM-2013 <
  
  - Select > SRIM-2013 (Professional) <
  
  - Rename extension : SRIM-2013-Pro **.e** =>   SRIM-2013-Pro **.exe**

  - Open terminal: > $\textcolor{teal}{\text{sudo apt install wine }}$ 

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


## Edits in original pysrim: 

### @ input.py:

@ _write_ion()

    self._trim.ion.energy / 1000.0, # eV

    became:
    self._trim.ion.energy
    
@ _write_bragg_correction()

    return (
        'Target Compound Corrections (Bragg)'
            ) + self.newline + 
            ' 1' * len(self._trim.target.layers) 
            + self.newline

    >> ' 1' * len(self._trim.target.layers) << became >> str(self._trim.settings.bragg_correction) <<

### @ output.py

@ _read_num_ions()

    return int(float(match.group(1)))

    became:
    return int(float(match.group(1).replace(b',', b'.')))

@ \__init__()

    # add:
    self._data = data

### @ elementdb.py

@ create_elementdb()

    return yaml.load(open(dbpath, "r"))

    became:
    return yaml.load(open(dbpath, "r"), Loader=yaml.FullLoader)


