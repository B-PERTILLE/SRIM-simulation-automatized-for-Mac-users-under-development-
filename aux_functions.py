import os, shutil, inspect, importlib, math

def print_available_functions(module_name, show_help=True):
    """
        Print all available functions in the specified module.
        
        Args:
            module_name (str): The name of the module to inspect.
            show_help (bool): Whether to display the docstrings of the functions.
    """
    # Import the specified module
    module = importlib.import_module(module_name)

    # Get all functions from the module
    available_functions = [func for func in dir(module) if inspect.isfunction(getattr(module, func))]
    print("\n\n##################################################################\n")
    print(f"Available functions in the module '{module_name}':")
    for func in available_functions:
        # Print the function name
        print("\n\n____________________________________________________________________")
        print(f"\nFUNCTION:   {func}() \n")
        if show_help:
            # Retrieve the function object using its name
            func_object = getattr(module, func)
            # Print the docstring (help)
            print(inspect.getdoc(func_object) or "   >>> No docstring available.")

def round_according_uncertainty(x,ux):
    order_of_magnitude = -int(math.floor(math.log10(abs(ux))))
    ux_rounded = round(ux, order_of_magnitude)

    # Step 2: Round x to match the number of decimal places in ux_rounded
    x_rounded = round(x, order_of_magnitude)
    return x_rounded, ux_rounded

def display_post_installation_message():
    
    message = """

        REWRITE : 
        
        IMPORTANT: Post-installation Edits Required for PySRIM Compatibility

        After installing PySRIM, please follow these two steps to manually edit the PySRIM code.
        The files are likely located at:
        `anaconda3/lib/python3.11/site-packages/srim/`

        1. **File: `output.py` (SRIMOutput._read_num_ions)**
        - Modify the `_read_num_ions()` method.
        - Replace the following line:
                return int(float(match.group(1)))
        - With:
                return int(float(match.group(1).replace(b',', b'.')))
        - This change ensures proper handling of numbers with commas as decimal separators.

        2. **File: `input.py` (TRIMInput._write_ion)**
        - Modify the `_write_ion()` method.
        - Replace the following line:
                self._trim.ion.energy / 1000
        - With:
                self._trim.ion.energy
        - This ensures that ion energies are input directly in keV, avoiding incompatibility 
            issues with ion energies higher than 100 MeV.

        Please make these changes before running any SRIM simulations with PySRIM to ensure 
        compatibility and correct energy handling.
    """
    print(message)

def read_range(directory="", filename="LATERAL.txt", encoding="utf-8"):
    """
        Reads the SRIM output file (LATERAL.txt) and extracts ion range information.

        Parameters:
        -----------
        directory : str, optional
            The directory path where the file is located. Default is the current directory.
        filename : str, optional
            The name of the file to read. Default is 'LATERAL.txt'.
        encoding : str, optional
            The encoding of the file. Default is 'utf-8'. You can change it to 'ISO-8859-1' if there are encoding issues.

        Returns:
        --------
        dict
            A dictionary containing the following values extracted from the file:
            - 'Ion Average Range': The average range of ions in Angstroms (float).
            - 'Ion Average Straggling': The straggling associated with the ion average range in Angstroms (float).
            - 'Ion Lateral Range': The lateral range of ions in Angstroms (float).
            - 'Ion Lateral Straggling': The straggling associated with the lateral range in Angstroms (float).
            - 'Ion Radial Range': The radial range of ions in Angstroms (float).
            - 'Ion Radial Straggling': The straggling associated with the radial range in Angstroms (float).

        Example:
        --------
        range_data = read_range(directory="/path/to/files", filename="LATERAL.txt")
        print(range_data["Ion Average Range"])  # Outputs the average ion range in Angstroms
    """
    file_path = os.path.join(directory, filename)
    
    # Initialize the dictionary to store the extracted values
    ranges = {
        "Ion Average Range": None,
        "Ion Average Straggling": None,
        "Ion Lateral Range": None,
        "Ion Lateral Straggling": None,
        "Ion Radial  Range": None, #double space on purpose
        "Ion Radial  Straggling": None, #double space on purpose
    }

    try:
        # Open the file with specified encoding and handle invalid characters if needed
        with open(file_path, 'r', encoding=encoding, errors='replace') as file:
            for line in file:
                if any(key in line for key in ranges.keys()):
                    parts = line.split()
                    if(parts[1]=="Radial"): parts[1]="Radial "
                    if len(parts) >= 8:  # Ensure there are enough parts
                        key_prefix = " ".join(parts[:3])  # Get the relevant key prefix
                        if key_prefix in ranges:
                            ranges[key_prefix] = float(parts[4].replace(',', '.'))
                            ranges[key_prefix.replace("Range", "Straggling")] = float(parts[8].replace(',', '.'))

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found in directory '{directory}'.")
    except ValueError as ve:
        print(f"Value conversion error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return ranges


def subdirectories(base_dir="OUTPUTS"):
    """
    Returns list of subdirectories in a directory.

    Args:
        base_dir (str): The base directory where all output subfolders are located.
    """
    # Get all subdirectories inside the base OUTPUTS directory
    subdirectories = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]

    return subdirectories

def read_ioniz(directory="", filename="IONIZ.txt"):
    """
        Reads the SRIM output file (IONIZ.txt) and extracts the values for TARGET DEPTH, 
        IONIZ. by IONS, and IONIZ. by RECOILS into separate arrays.

        Parameters:
        -----------
        directory : str, optional
            The directory path where the file is located. Default is the current directory.
        filename : str, optional
            The name of the file to read. Default is 'IONIZ.txt'.

        Returns:
        --------
        tuple
            A tuple containing three lists:
            - depths (list of floats): The depth values in Angstroms.
            - ioniz_by_ions (list of floats): The ionization values by ions.
            - ioniz_by_recoils (list of floats): The ionization values by recoils.

        Example:
        --------
        depths, ioniz_ions, ioniz_recoils = read_ioniz(directory="/path/to/files", filename="IONIZ.txt")
        print(depths)  # Outputs the depth values
    """
    depths = []
    ioniz_by_ions = []
    ioniz_by_recoils = []

    try:
        with open(f"{directory}/{filename}", "r") as file:
            # Use a generator expression to find the start of the data section
            data_start_line = next(
                (line for line in file if "TARGET" in line), None
            )
            if data_start_line is None:
                print("No data section found.")
                return depths, ioniz_by_ions, ioniz_by_recoils
            
            # Read remaining lines and extract data
            for line in file:
                if line.strip():  # Ignore empty lines
                    # Split the line into columns and convert to float
                    parts = line.split()
                    if len(parts) >= 3:
                        try:
                            depths.append(float(parts[0].replace(',', '')))
                            ioniz_by_ions.append(float(parts[1].replace(',', '')))
                            ioniz_by_recoils.append(float(parts[2].replace(',', '')))
                        except ValueError:
                            continue  # Skip lines that can't be converted

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found in directory '{directory}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return depths, ioniz_by_ions, ioniz_by_recoils


def move_files(Zi,isotope,
               files_to_move = ["IONIZ.txt","LATERAL.txt","VACANCY.txt","NOVAC.txt","E2RECOIL.txt","PHONON.txt","RANGE.txt","TDATA.txt",],
               files_to_copy = ["TRIM.IN","TRIMAUTO"]):

    """
        Move specified files related to a given isotope to an output directory.

        Parameters:
        - Zi (int or str): The atomic number or identifier for the isotope.
        - isotope (str): The name or designation of the isotope.

        Returns:
        - None
    """
        
    outputdir = str(Zi) +isotope
    if not os.path.exists("OUTPUTS/"+outputdir) : os.makedirs("OUTPUTS/"+outputdir)
    outputdir = "OUTPUTS/"+outputdir
    #+"OUTPUTS/"+outputdir

    print("\nStart moving files...")
        # Move each file to the output folder
    for file in files_to_move:
        if os.path.exists(file):
            shutil.move(file, os.path.join(outputdir, file))
            print(f"   __ moved {file} to {outputdir}")
        else:
            print(f"{file} not found")
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy(file, os.path.join(outputdir, file))
            print(f"   __ copied {file} to {outputdir}")
        else:
            print(f"{file} not found")

    print("All files processed.\n")
    
    return


def print_line():
    print("\n------------------------------------------\n")
    return