import sys

def set_help(input_write,dataname):
    """ When using the help flag. It assists in writing all your files for you"""
    
    print "\nIf you dont know parameters for these inputs, please refer to https://github.com/sipjca/cmlparser_py/blob/master/lammps_params.md\n"
    print "Input the whole string you intend on using for each lammps parameter, without the type"
    print "For example when prompted 'Enter Lammps units: ', enter real for the real style"
    print "For a full example refer to the above link\n"

    units = raw_input("Enter Lammps units: ")
    atom_style = raw_input("Enter Lammps atom_style: ")
    boundary = raw_input("Enter Lammps boundary: ")
    bond_style = raw_input("Enter Lammps bond_style: ")
    dielectric = raw_input("Enter Lammps dielectric: ")
    pair_style = raw_input("Enter Lammps pair_style: ")
    angle_style = raw_input("Enter Lammps angle_style: ")
    special_bonds = raw_input("Enter Lammps special_bonds: ")
    improper_style = raw_input("Enter Lammps improper_style: ")
    kspace_style = raw_input("Enter Lammps kspace_style: ")
    thermo_style = raw_input("Enter Lammps thermo_style: ")
    dump1 = raw_input("Enter Lammps dump: ")
    neighbor = raw_input("Enter Lammps neighbor: ")
    neigh_modify = raw_input("Enter Lammps neigh_modify: ")
    fix1 = raw_input("Enter fix 1: ")
    fix2 = raw_input("Enter fix 2: ")
    velocity = raw_input("Enter velocity: ")
    timestep = raw_input("Enter timestep: ")
    thermo = raw_input("Enter thermo: ")
    run = raw_input("Enter run time: ")
    restart1 = raw_input("Enter write_restart: ")
    replicate = raw_input("Enter how many times to replicate: ")
    fix3 = raw_input("Enter fix1 after replication: ")
    fix4 = raw_input("Enter fix2 after replication: ")
    velocity2 = raw_input("Enter velocity post replication: ")
    dump2 = raw_input("Enter Lammps dump for replicate: ")
    run2 = raw_input("Enter run time after replication: ")
    restart2 = raw_input("Enter restart after replication: ")

    #ADD IN HELP FOR HELP
    print "units %s " % units
    print "atom_style %s " % atom_style
    print "boundary %s " % boundary
    print "bond_style %s " % bond_style
    print "dielectric %s " % dielectric
    print "pair_style %s " % pair_style
    print "angle_style %s " % angle_style
    print "special_bonds %s " % special_bonds
    print "improper_style %s " % improper_style
    print "kspace_style %s " % kspace_style
    print "thermo_style %s " % thermo_style
    print "dump 1 %s " % dump1
    print "neighbor %s " % neighbor
    print "neigh_modify %s " % neigh_modify
    print "fix1 %s " % fix1
    print "fix2 %s " % fix2
    print "velocity %s " % velocity
    print "timestep %s " % timestep
    print "thermo %s " % thermo
    print "run %s " % run
    print "write_restart %s " % restart1
    print "replicate %s " % replicate
    print "fix1 %s " % fix3
    print "fix2 %s " % fix4
    print "velocity %s " % velocity2
    print "dump 2 %s " % dump2
    print "run %s " % run2
    print "write_restart %s " % restart2

    correct = raw_input("Your file will be printed out almost exactly as above. Is this correct? (y/n)")
    if correct == "n":
        set()
    else: #write output
        lammps = open(input_write,"w")
        sys.stdout = lammps

        print "# created by CMLParser\n"
        print "units %s " % units
        print "atom_style %s " % atom_style
        print "boundary %s " % boundary
        print "bond_style %s " % bond_style
        print "dielectric %s " % dielectric
        print "pair_style %s " % pair_style
        print "angle_style %s " % angle_style
        print "dihedral_style opls"
        print "special_bonds %s " % special_bonds
        print "improper_style %s " % improper_style
        print "kspace_style %s " % kspace_style
        print "read_data %s" % dataname
        print "thermo_style %s " % thermo_style
        print "dump %s " % dump1
        print "neighbor %s " % neighbor
        print "neigh_modify %s " % neigh_modify
        print "fix1 %s " % fix1
        print "fix2 %s " % fix2
        print "velocity %s " % velocity
        print "timestep %s " % timestep
        print "thermo %s " % thermo
        print "run %s " % run
        print "unfix 1"
        print "unfix 2"
        print "write_restart %s " % restart1
        print "replicate %s " % replicate
        print "undump 1"
        print "fix1 %s " % fix3
        print "fix2 %s " % fix4
        print "velocity %s " % velocity2
        print "dump 2 %s " % dump2
        print "run %s " % run2
        print "write_restart %s " % restart2
        print "unfix 1"
        print "unfix 2"

        lammps.close()

def change_data_from_filein(file,dataname):
    fileread = open(file,'r')
    read = fileread.readlines()
    for i in range(len(read)):
        split = read[i].split()
        for j in range(len(split)):
            if split[0] == "read_data":
                line = i
    fileread.close()
    filewrite = open(file,'w')
    for i in range(len(read)):
        if read == line:
            filewrite.write('read_data %s' % dataname)
        else:
            filewrite.write(read[i])

    filewrite.close()
