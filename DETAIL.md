# In-Depth Look Into cmlparser_py

## Outline
Our example input here will be `python cml.py molecules/smdppeh.cml outputs/data.first outputs/in.rewriteout d`

There are a few important things to note about the input:
* `cml.py` is the main class where every module is run from. This is the 'main'
* `molecules/smdppeh.cml` is the file path to where the molecule to run simulations on is located
* `outputs/data.first` is your chosen name for a lammps data file
* `outputs/in.rewriteout` is your chosen name for a lammps input file
* `d` specifies that you want debugging output to be displayed to the terminal

Lets dive into cml.py to see how the program runs.


### `cml.py`
 1. Runs `setflag.py` which gets the flags from the terminal input and creates variables
 * Begins to read the .cml file specified, this is `molecules/smdppeh.cml` and stores the lines in a list
 * Reads the static OPLS-AA file called `oplsaa.prm.txt` and stores the lines in a list
 * From the lines of the .cml file, we get a list of atom info and bonding info from it and store it into variables called `atomTree` and `bondTree` respectfully
 * Now we create 'atom objects' defined in `atom.py` from the `atomTree` variable. Basically we just parse the tree to get relevant data. These are stored as a list
 * Similarly for bonds we create bond objects defined in `bond.py` from the `bondTree` variable. These are stored as a list.
 * From these atom and bond objects we created, we now create Angle objects, as defined in `angle.py` and stores angles as a list as well
 * From the angles we not create a list of dihedral objects as defined in `dihedral.py`
 * From the dihedrals we create a list of ring objects as defined in 'ring.py'
 * From these rings we create a list of fused rings as defined in `fused.py`
 * From the earlier OPLS-AA file we get the relevant information from it.
 * In respective classes we get atom, bond, angle, and dihedral data from the OPLS file and store them in each respective object.
 * In order to generate a lammps data file we need to find the unique number of atoms, bonds, angles, and dihedrals. Each respective class have a module called `uniq_types` which finds the number of unique types of objects.
 * Now we have to set what unique type each atom, bond, angle, or dihedral is. So each respective class has a module called `get_type` which does exactly this.
 * To generate this lammps data file we also need to define a periodic boundary size. We get the minimum and maximum x, y, and z positions of all the atoms to generate this box size.
 * After all this data is crunched we create monomer and molecule objects depending on the flag. Which just contain all the atom, bond, angle, dihedral, ring, and fused ring data
 * Depending which flag different things happen:
  * For Monomers:
    * It runs the `mark_thio` module, to mark the thiophene rings
    * It then gets the intermonomer dihedral.
    * From here we then get the whole single monomer to attach
  * For molecules:
    * We run the openbabel program to set partial charges and read the .mol2 file it outputs to get the partial charges.
     * We write qchem files to get better partial charges and get dihedral dft information (this is actually for monomer but not fully implemented or tested yet)
    * After this basically everything gets printed out to the specified output files


## Classes/Modules
#### We are going to run through `cml.py` line by line and explain each class it runs, as well as all the variables.

As `cml.py` is ran, it imports all the files from the program

The first important line is: `textout,aa,outname,lammpsin,help,isfile,fname,moleculen = setflags.set_flags()`
* textout - The variable corresponding to 
