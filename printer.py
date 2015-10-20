import atom
import bond
import sys
import os
import tester

def debug(atoms,bonds,angles,dihedrals,rings,fused_rings,opls_atoms,opls_bonds,opls_angles,opls_dihedrals):
    """ Prints any debugging info. Uncomment lines to print
    """
    print "Debugger Ran\n"
    pctotal = 0
    for i in range(len(atoms)):
        pctotal += float(atoms[i].opls_partial)
    print pctotal
    #print basic info
    #print_atoms(atoms)
    #print_bonds(bonds)
    #print_angles(angles)
    #print_dihedrals(dihedrals)
    print_ring(rings)
    print_fused(fused_rings)

    #print opls info (not very useful)
    #print_opls_atoms(opls_atoms)
    #print_opls_bonds(opls_bonds)
    #print_opls_angles(opls_angles)
    #print_opls_dihedrals(opls_dihedrals)

    #reprint for opls add
    #print_atoms(atoms,True)
    #print_bonds(bonds,True)
    #print_angles(angles,True)
    #print_dihedrals(dihedrals)
    #print_all_dft(dihedrals)
    #tester.count_atoms(opls_atoms,atoms)
    #tester.find_missing_opls(opls_atoms,atoms)


def print_atoms(atom,extra = False):
    """ Prints a list of atom objects

    Keyword Arguments:
    bond -- The list of atom objects to pass in and print
    """
    for k in range(0,len(atom)):
       print "Atom id: %s" % atom[k].atom_id
       print "Atom type: %s" % atom[k].atom_type
       print "X position: %s" % atom[k].x_pos
       print "Y position: %s" % atom[k].y_pos
       print "Z position: %s" % atom[k].z_pos
       print "Atoms bonded to %s" % atom[k].atom_bonds
       print "Number of bonds %s" % atom[k].numbonds
       if extra:
           print "OPLS id %s" % atom[k].opls_id
           print "OPLS bond id %s" % atom[k].opls_bondid
           print "OPLS sigma %s" % atom[k].opls_sigma
           print "OPLS epsilon %s" % atom[k].opls_epsilon
           print "OPLS partial charge %s" % atom[k].opls_partial
           print "OPLS atomic mass %s" % atom[k].opls_mass
           print "Ring %s" % atom[k].ring
       print ""

def print_bonds(bond,boo = False):
    """ Prints a list of bond objects created by create_bondobj

    Keyword Arguments:
    bond -- The list of bond objects to pass in and print
    """
    print "   BONDS   "
    print "-----------"
    for z in range(0, len(bond)):
       print "Bond Type: %s" % bond[z].bond_type
       print "Bond Master(bonded from): %s" % bond[z].bond_master.atom_id
       print "Bond Slave(bonded to): %s" % bond[z].bond_slave.atom_id
       print "Bond Master Type: %s" % bond[z].bond_master.atom_type
       print "Bond Slave Type: %s" % bond[z].bond_slave.atom_type
       print "Bond Number %s" % z
       if boo:
           print "OPLS Force Constant: %s" % bond[z].bond_force_const
           print "OPLS Equilibrium Length: %s" % bond[z].bond_equib_len
       print ""

def print_angles(AngleList,boo = False):
    """
    Given a list of angles, print the angle id's

    Keyword Arguments:
    AngleList -- The list of angles to print
    """
    for x in range(0,len(AngleList)):
        print "Angle number %s" % x
        print "Angle Type: %s" % AngleList[x].Angle_type
        print "Master Angle: %s" % AngleList[x].Angle_master.atom_id
        print "Slave angle 1: %s" % AngleList[x].Angle_slave1.atom_id
        print "Slave angle 2: %s" % AngleList[x].Angle_slave2.atom_id
        if boo:
            print "Master Angle Bond: %s" % AngleList[x].Angle_master.opls_bondid
            print "Slave Angle Bond: %s" % AngleList[x].Angle_slave1.opls_bondid
            print "Slave Angle2 Bond: %s" % AngleList[x].Angle_slave2.opls_bondid
            if AngleList[x].Angle_equib_len == "":
                print "no good data"
                continue
            print "Equilibrium length %s" % AngleList[x].Angle_equib_len
            print "Force Constant: %s" % AngleList[x].Angle_force_const
        print ""

def print_dihedrals(dihedrals):
    """ Print the atom id's of a list of dihedrals

    Keyword Arguments:
    dihedrals -- the list of dihedrals to print
    """
    print "DIHEDRALS"
    print "---------"
    for i in range(0,len(dihedrals)):
        print "Dihedral %s: %s" % (i,dihedrals[i])
        print "Dihedral Master1 %s" % (dihedrals[i].dihedral_master1.atom_id)
        print "Dihedral Master2 %s" % (dihedrals[i].dihedral_master2.atom_id)
        print "Dihedral Slave1 %s" % (dihedrals[i].dihedral_slave1.atom_id)
        print "Dihedral Slave2 %s" % (dihedrals[i].dihedral_slave2.atom_id)

def print_ring(rings):
    """ Prints the atom id's from what is contained in the Ring list.

    Keyword Arguments:
    rings -- The list of rings to print and get atom id's from
    """
    print "----------RINGS----------"
    for k in range(0,len(rings)):
        print ""
        print "ring number %d" % k
        print rings[k]
        print rings[k].atom1.atom_id
        print rings[k].atom2.atom_id
        print rings[k].atom3.atom_id
        print rings[k].atom4.atom_id
        print rings[k].atom5.atom_id
        if rings[k].ring_type == 6:
            print rings[k].atom6.atom_id

def print_fused(fused):
    """ Prints the fused rings found by the find_fused method. Is void.

        Keyword Arguments:
        fused - The list of fused rings generated by find_fused
    """
    print "----------FUSED RINGS---------"
    for i in range(0,len(fused)):
        for j in range(0,len(fused[i].ring1)):
            print "fused 1: %s" % fused[i].ring1[j].atom_id
        print ""
        for j in range(0,len(fused[i].ring2)):
            print "fused 2: %s" % fused[i].ring2[j].atom_id

def print_opls_atoms(opls_atoms):
    """ Prints the list of opls atoms created earlier in this file

        Keyword Arguments:
        opls_atoms - The list of opls atoms to print
    """
    print "----------OPLS ATOMS----------"
    for i in range(0,len(opls_atoms)):
        print ""
        print opls_atoms[i].opls_id
        print opls_atoms[i].opls_bondid
        print opls_atoms[i].opls_type
        print opls_atoms[i].pc
        print opls_atoms[i].sigma
        print opls_atoms[i].epsilon
        print opls_atoms[i].amass

def print_opls_bonds(opls_bonds):
    """ Prints the list of opls bonds created earlier in this file

        Keyword Arguments:
        opls_bonds - The list of opls bond to print
    """
    print "----------OPLS BONDS----------"
    for i in range(0,len(opls_bonds)):
        print ""
        print opls_bonds[i].opls_master
        print opls_bonds[i].opls_slave
        print opls_bonds[i].fc
        print opls_bonds[i].el

def print_opls_angles(opls_angles):
    """ Prints the list of opls angles created earlier in this file

        Keyword Arguments:
        opls_angles - The list of opls angles to print
    """
    print "----------OPLS ANGLES----------"
    for i in range(0,len(opls_angles)):
        print ""
        print opls_angles[i].opls_master
        print opls_angles[i].opls_slave1
        print opls_angles[i].opls_slave2
        print opls_angles[i].fc
        print opls_angles[i].el

def print_opls_dihedrals(opls_dihedrals):
    """ Prints the list of opls dihedrals created earlier in this file

        Keyword Arguments:
        opls_dihedrals - The list of opls dihedrals to print
    """
    print "----------OPLS DIHEDRALS----------"
    for i in range(len(opls_dihedrals)):
        print ""
        print opls_dihedrals[i].opls_master1
        print opls_dihedrals[i].opls_master2
        print opls_dihedrals[i].opls_slave1
        print opls_dihedrals[i].opls_slave2
        print opls_dihedrals[i].k1
        print opls_dihedrals[i].k2
        print opls_dihedrals[i].k3
        print opls_dihedrals[i].k4

def print_all_dft(dihedrals):
    counter = 0
    for i in range(len(dihedrals)):
        if dihedrals[i].dft:
            counter += 1
    print counter

def print_data(outname,atoms,bonds,angles,dihedrals,unique_a,unique_b,unique_ang,unique_d,xmin,xmax,ymin,ymax,zmin,zmax):
    data = open(outname,"w")
    sys.stdout = data

    #writes out to lammps, this really should be done in a method, but it takes a assload of inputs
    print "Written by CMLParser\n"
    print "\t%s atoms" % len(atoms)
    print "\t%s bonds" % len(bonds)
    print "\t%s angles" % len(angles)
    print "\t%s dihedrals\n" % len(dihedrals)
    print "\t%s atom types" % len(unique_a)
    print "\t%s bond types" % (len(unique_b)+1)
    print "\t%s angle types" % len(unique_ang)
    print "\t%s dihedral types\n" % (len(unique_d)+1)
    print "\t%s %s xlo xhi" % (xmin,xmax)
    print "\t%s %s ylo yhi" % (ymin,ymax)
    print "\t%s %s zlo zhi\n" % (zmin,zmax)
    print "Masses\n"
    for i in range(len(unique_a)):
        print "%s %s" % (i+1,unique_a[i].opls_mass)
    print "\nBond Coeffs\n"
    for i in range(len(unique_b)):
        print "%s %s %s" % (i+1,unique_b[i].bond_force_const,unique_b[i].bond_equib_len)
    print "%s 450.00 1.5000" % (len(unique_b)+1)

    print "\nAngle Coeffs\n"
    for i in range(len(unique_ang)):
        print "%s %s %s" % (i+1,unique_ang[i].Angle_force_const,unique_ang[i].Angle_equib_len)

    print "\nDihedral Coeffs\n"
    for i in range(len(unique_d)):
        print "%s %s %s %s %s" % (i+1,unique_d[i].k1,unique_d[i].k2,unique_d[i].k3,unique_d[i].k4)
    print "%s 0.000 0.000 0.000 0.0" % (len(unique_d)+1) # why does it do this?

    print "\nPair Coeffs\n"
    for i in range(len(unique_a)):
        print "%s %s %s" % (i+1,unique_a[i].opls_epsilon,unique_a[i].opls_sigma)


    print "\nAtoms\n"
    for i in range(len(atoms)):
        if atoms[i].print_type == 0:
            atoms[i].print_type = 6
        print "%s %d %s %s %s %s %s" % (i+1,atoms[i].Mol_id, atoms[i].print_type,atoms[i].opls_partial,atoms[i].x_pos,atoms[i].y_pos,atoms[i].z_pos)



    print "\nBonds\n"
    for i in range(len(bonds)):
        if bonds[i].print_type == 0:
            bonds[i].print_type = (len(unique_b)+1)
        print "%s %s %s %s" % (i+1,bonds[i].print_type,bonds[i].bond_master.atom_id,bonds[i].bond_slave.atom_id)
    print "\nAngles\n"
    for i in range(len(angles)):
        print "%s %s %s %s %s" % (i+1,angles[i].print_type,angles[i].Angle_master.atom_id,angles[i].Angle_slave1.atom_id,angles[i].Angle_slave2.atom_id)
    print "\nDihedrals\n"
    for i in range(len(dihedrals)):
        #hack smdppeh specific TODO
        if dihedrals[i].print_type == 0:
            dihedrals[i].print_type = (len(unique_d)+1)
        print "%s %s %s %s %s %s" % (i+1,dihedrals[i].print_type,dihedrals[i].dihedral_master1.atom_id,dihedrals[i].dihedral_master2.atom_id,dihedrals[i].dihedral_slave1.atom_id,dihedrals[i].dihedral_slave2.atom_id)
    data.close()

def print_lammpsin(lammpsin,dataname,lammpsinput):
    lammps = open(lammpsin,"w")
    sys.stdout = lammps

    print "# created by CMLParser\n"
    print "units real"
    print "atom_style full"
    print "boundary p p p"
    print "bond_style harmonic"
    print "dielectric 4.81"
    print "pair_style lj/cut/coul/long 20.0"
    print "angle_style harmonic"
    print "dihedral_style opls"
    print "special_bonds lj 0 1 1"
    print "improper_style none"
    print "kspace_style ewald 10"
    print "read_data %s" % dataname
    print "thermo_style custom step temp press ke pe etotal density"
    print "dump 1 all custom 200 %s.lammpstrj id type mol xs ys zs vx vy vz" % lammpsinput
    print "neighbor 10.0 bin"
    print "neigh_modify every 1 delay 0 one 10000"
    print "fix 3 ring rigid molecule iso 1 1 1000"
    print "fix 0 all langevin 300 300 100 43294"
    print "fix 1 all nph iso 1 1 1000 drag 2"
    print "fix 2 all momentum 1 linear 1 1 1"
    print "velocity all create 100.00000 1223"
    print "timestep 1"
    print "thermo 100"
    print "run 10000"
    print "unfix 0"
    print "unfix 1"
    print "unfix 2"
    print "unfix 3"
    print "write_restart restart.%s\n\n" % lammpsinput
    print "replicate 5 5 5"
    print "undump 1"
    print "fix 3 test rigid/nph/small molecule iso 1 1 1000"
    print "fix 0 all langevin 300 300 100 43294"
    print "fix 1 chain nph iso 1 1 1000 drag 2     # note the chain group"
    print "fix 2 chain momentum 1 linear 1 1 1"
    print "velocity all create 100.00000 1223"
    print "dump 2 all custom 1000 %s.lammpstrj id type mol xs ys zs vx vy vz" % ("%s_final" % lammpsinput)
    print "run 500000"
    print "write_restart restart.%s" % ("%s_final" % lammpsinput)
    print "unfix 0"
    print "unfix 1"
    print "unfix 2"
    print "unfix 3"

    lammps.close()

def print_srun(lammpsinput):
    nodes = raw_input('How many nodes do you want to run on (24 cores each): ')
    time = raw_input('How much time would you like to run for (HH:MM:SS): ')
    cores = raw_input('How many CPUs would you like to run on: ')

    os.chdir('outputs')
    cometrun = open('run_%s' % lammpsinput,'w')
    sys.stdout = cometrun

    print "#!/bin/bash"
    print '#SBATCH --job-name="cmlparser_run"' #add shit here
    print '#SBATCH --output="job.%j.%N.out"'
    print '#SBATCH --partition=compute'

    print '#SBATCH --nodes=%s' % nodes
    print '#SBATCH --ntasks-per-node=24'

    print '#SBATCH -t %s' % time

    print '#SBATCH -A csd459'

    print 'module load python lammps openbabel qchem'

    print 'cd /oasis/scratch/comet/cjpais/temp_project/cmlparser_py/outputs'
    print 'export OMP_NUM_THREADS=1'

    print 'ibrun -np %s lammps < in.%s' % (cores,lammpsinput) #add shit here
    cometrun.close()
