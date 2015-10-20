import sys
import os
import xml.etree.ElementTree as ET
import printer
import setflags
import setparams

import atom
import bond
import angle
import dihedral
import ring
import fused
import molecule
import monomer
import rigid

import opls as op
import oplsatom
import oplsbond
import oplsangle
import oplsmolecule
import oplsdihedral

import babel
import write_nwchem
import write_qchem

import tester

RIGID = True

os.system('clear')

#set basic data names and get flags
moleculeboo,mname,dname,inname,debug,isfile,fname,help,length, UA = setflags.set_flags_new()

# split names for ease later on
dataname = dname.split('/')
dataname = dataname[len(dataname)-1]
lammpsinput = inname.split('/')
lammpsinput = inname.split('.')
lammpsinput = lammpsinput[len(lammpsinput)-1]

if help:
    setparams.set_help(lammpsin,dataname)
if isfile:
    setparams.change_data_from_filein(fname,dataname)

#import the cml file and read
tree = ET.parse(mname)
root = tree.getroot()

#get the oplsfile for later use
oplsname = 'oplsaa.prm.txt'
oplsfile = open(oplsname,'r')
oplslist = oplsfile.readlines()
oplslist2 = op.splitList(oplslist)
oplsfinal = [x for x in oplslist2 if x != []]

#create the list of atoms and bonds from the cml file
atomTree = root.findall('./atomArray/atom')
bondTree = root.findall('./bondArray/bond')

#create all the objects
atoms = atom.create_atoms(atomTree)
bonds = bond.create_bonds(bondTree,atoms)
angles = angle.create_angles(atoms,bonds)
dihedrals = dihedral.create_dihedrals(angles)
#baddihedrals = dihedral.create_dihedrals(angles,True)
dihedral.set_dft(dihedrals,bonds)
#cyclesdemo.get_edges(atoms)
rings = ring.create_rings(atoms)
fused_rings = fused.create_fused_rings(rings)
Rigid_List = rigid.Find_Rigid_Bodies(atoms, rings, fused_rings)
if RIGID == True:
    
    SC_Atoms = []
    for atomobj in atoms:
        if atomobj.SC ==True:
            print "adding", atomobj.atom_id, atomobj.atom_type
            SC_Atoms.append(atomobj)

    print len(SC_Atoms)
    
    
    SC_Bonds = []
    for bondobj in bonds:
        if bondobj.bond_master.SC == True or bondobj.bond_slave.SC == True:
            print "Found Bond", bondobj.bond_master.atom_id, bondobj.bond_slave.atom_id
            SC_Bonds.append(bondobj)

    print len(SC_Bonds)

    SC_Angles = angle.create_angles(SC_Atoms, SC_Bonds)
    SC_Dihedrals = dihedral.create_dihedrals(SC_Angles)


#get important OPLS info
opatom,van,partial,opbond,opangle,optorsion = op.getImportant(oplsfinal)

#deal with OPLS
opls_atoms = oplsatom.create_atoms(opatom,van,partial)
opls_bonds = oplsbond.create_bonds(opbond)
opls_angles = oplsangle.create_angles(opangle)
opls_dihedrals = oplsdihedral.create_dihedrals(optorsion)

#more OPLS fun

oplsmolecule.get_molecule(atoms,opls_atoms)

if RIGID == False:

    bond.set_opls(bonds,opls_bonds)
    angle.set_opls(angles,opls_angles)
    dihedral.set_opls(dihedrals,opls_dihedrals)
    #unique types
    unique_a = atom.uniq_types(atoms)
    unique_b = bond.uniq_types(bonds)
    unique_ang = angle.uniq_types(angles)
    unique_d = dihedral.uniq_types(dihedrals)
    
    #get type
    atom.get_type(atoms,unique_a)
    bond.get_type(bonds,unique_b)
    angle.get_type(angles,unique_ang)
    dihedral.get_type(dihedrals,unique_d)


if RIGID == True:
    
    bond.set_opls(SC_Bonds,opls_bonds)
    angle.set_opls(SC_Angles,opls_angles)
    dihedral.set_opls(SC_Dihedrals,opls_dihedrals)
    print "Adding Ghosts"
    rigid.Add_Ghost(Rigid_List, atoms, SC_Bonds, SC_Angles, SC_Dihedrals)

    #unique types
    unique_a = atom.uniq_types(atoms)
    unique_b = bond.uniq_types(SC_Bonds)
    unique_ang = angle.uniq_types(SC_Angles)
    unique_d = dihedral.uniq_types(SC_Dihedrals)

    #get type
    atom.get_type(atoms,unique_a)
    bond.get_type(SC_Bonds,unique_b)
    angle.get_type(SC_Angles,unique_ang)
    dihedral.get_type(SC_Dihedrals,unique_d)
    i = len(Rigid_List)
    
    # Set molecule IDs such that each rigid body is treated as an independent molecule
    for atomobj in atoms:
        if atomobj.Rigid_Body_ID == 0:
            atomobj.Mol_id = i
            i += 1
        if atomobj.Rigid_Body_ID != 0:
            atomobj.Mol_id = atomobj.Rigid_Body_ID + 1



#box size
xmin,ymin,zmin,xmax,ymax,zmax = atom.periodic_b_size(atoms)

sys.stdout = sys.__stdout__

#handling
if moleculeboo:
    molecule1 = molecule.create_molecule(atoms,bonds,angles,dihedrals,rings,fused_rings)
elif moleculeboo == False:
    print "You really shouldn't be running this. It doesn't fully work"
    print "If you are using it, I hope you can understand the modules below, some are confusing and unused\n"
    monomer1 = monomer.create_monomer(atoms,SC_bonds,angles,dihedrals,rings,fused_rings)
    thorings = monomer.mark_thio(monomer1)
    intermono = monomer.find_intermono(monomer1)
    halfmono = monomer.get_single_alist(monomer1)
    attach = monomer.find_attach(monomer1,halfmono)
    test2 = monomer.attach(halfmono,attach,monomer1,length)
    monomer.print_mono(test2,"outputs/test")
    #monomer.create_polymer_cml(mname,halfmono,attach,monomer1)
    sys.stdout = sys.__stdout__

#create babel and read to get better partials
#babel.read_babel_set(mname,atoms)
atom.adjust_partials(atoms)

#write different dft finders
#write_nwchem.dft(dihedrals)
#write_qchem.write(atoms,dihedrals)
sys.stdout = sys.__stdout__

if debug:
    printer.debug(atoms,bonds,angles,dihedrals,rings,fused_rings,opls_atoms,opls_bonds,opls_angles,opls_dihedrals)

#print all the output files
if RIGID == True:
    printer.print_data(dname,atoms,SC_Bonds,SC_Angles,SC_Dihedrals,unique_a,unique_b,unique_ang,unique_d,xmin,xmax,ymin,ymax,zmin,zmax)
else:
    printer.print_data(dname,atoms,bonds,angles,dihedrals,unique_a,unique_b,unique_ang,unique_d,xmin,xmax,ymin,ymax,zmin,zmax)



if help == False or isfile == False:
    printer.print_lammpsin(inname,dataname,lammpsinput)
sys.stdout = sys.__stdout__
printer.print_srun(lammpsinput)

#autorun
#os.system('sbatch run_%s' % lammpsinput)
