# cmlparser_py
#### For a more indepth look at cmlparser_py look at DETAIL.md
Parses avogadro created .cml files

Uses a command line argument specifying the location of the file to parse.
It doesn't check the filename for the extention cml, so be sure it is a cml
file otherwise there may be issues.

There are a few command line flags to be aware of (show in parens):

python cml.py (cml-filename) (output-filename) (d)
* `cml-filename` - The name and location of the cml file you would like to parse
* `output-filename` - The file name and location for a lammps output
* `d` or `debug` - Used for debugging output, lines in cml.py will help print out debugging info can be specified anywhere in the input
* `h` or `help` - Used when you are unsure on how to write a lammps file
* `-f (file)` - Specifies there is an lammps input file that just needs read_data changed. File is the input file

An example of use would be:

`python cml.py -imol molecules/smdppeh.cml -od outputs/data.molecule_smdppeh -oi outputs/in.molecule_smdppeh -d` for molecules

or `python cml.py -imono monomers/p3htn.cml -od outputs/data.monomer_p3ht -oi outputs/data.monomer_p3ht -d` for monomers

This would effectively run the program, using the `molecules/smdppeh.cml` molecule as its input.
The flag `outputs/data.first` is the data file to output and for lammps to read.
It also states `outputs/in.rewriteout` as the file to input into lammps
The final `d` at the end is to get some debugging output.
