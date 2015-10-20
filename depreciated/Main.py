import sys
import xml.etree.ElementTree as ET
import parse as p
import typeofmolecule as tm
import oplsparse as op
import time
import tester

start = time.time()
twoArg = False
hydrogen = False

if len(sys.argv) > 2:
    print "ran"
    old_stdout = sys.stdout
    log_file = open(sys.argv[2],"w")
    sys.stdout = log_file

if len(sys.argv) == 4:
    if sys.argv[3] == "aa":
        hydrogen = True
        p.hydrogen = True

#get filename from commandline
cmlfile = sys.argv[1]

#begin parsing
tree = ET.parse(cmlfile)
root = tree.getroot()

atomList = root.findall('./atomArray/atom')
bondList = root.findall('./bondArray/bond')

#create a bunch of atom and bond objects
atom = p.create_atomobj(atomList)
bond = p.create_bondobj(bondList)

#print the atom and bond objects
p.print_atoms(atom)
p.print_bonds(bond)

#get a list of angles formed by the bonds
for i in range(0,len(atom)):
    p.get_num_bonds(atom[i],bond)
AngleList = p.print_find_angles_new(atom,bond)
p.print_angles(AngleList)

#get the dihedrals and print them
dihedrals = p.find_dihedrals_new(AngleList)
p.print_dihedrals(dihedrals)

#get the rings and print them
ring = p.find_ring(dihedrals)
ring = p.clean_rings(ring)
p.print_ring(ring)

#get the fused rings and print them
#TODO
fused = p.find_fused(ring)
p.print_fused(fused)

#begin to parse the opls file
opls_file = 'oplsaa.prm.txt'
oplsfile = open(opls_file,'r')
oplslist = oplsfile.readlines()

oplsMatrix = op.splitList(oplslist)
oplsMatrix2 = [x for x in oplsMatrix if x != []]
opls_atom_ids = op.getAtoms(oplsMatrix2)
opls_van = op.getVan(oplsMatrix2)
opls_partial = op.getPartial(oplsMatrix2)
opls_bond = op.getBonds(oplsMatrix2)
opls_angle = op.getAngles(oplsMatrix2)

opls_atoms = op.create_opls_atom(opls_atom_ids,opls_van,opls_partial)
#op.print_opls_atoms(opls_atoms)

opls_bonds = op.create_opls_bond(opls_bond)
#op.print_opls_bonds(opls_bonds)

opls_angles = op.create_opls_angle(opls_angle)
#op.print_opls_angles(opls_angles)

#get opls molecules
for i in range(0,len(atom)):
    tm.get_molecule(atom[i],opls_atoms)

#get opls bonds
for i in range(0,len(bond)):
    if p.find_atom_by_id(bond[i].bond_master).atom_type == "H" or p.find_atom_by_id(bond[i].bond_slave).atom_type == "H":
        continue
    op.get_bond(bond[i],opls_bonds)

#get opls angles
for i in range(0,len(AngleList)):
    op.get_angles(AngleList[i],opls_angles)

#print again to see the opls changes, this time printing the extra info
#p.print_atoms(atom,True)
#p.print_bonds(bond,True)
#p.print_angles(AngleList,True)

#count the atoms found earlier by get_molecule
tester.count_atoms(opls_atoms,atom)

#print the time it takes to make sure it doesnt take too long
print("--- %s seconds ---" % (time.time() - start))

if twoArg:
    sys.stdout = old_stdout
    log_file.close()
