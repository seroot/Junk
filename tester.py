def count_atoms(opls_atoms,atoms):
    """ Counts the type of atoms found in the opls file for the molecule

        Keyword Arguments:
        opls_atoms - The list of Opls Atoms created in the oplsparse file
        atoms - The list of atoms that get values assigned to them and used throughout
    """
    for i in range(0,len(opls_atoms)):
        counter = 0
        for j in range(0,len(atoms)):
            if atoms[j].opls_id == opls_atoms[i].opls_id:
                counter += 1
        if counter != 0:
            print "There are %s of opls_id #%s" % (counter,opls_atoms[i].opls_id)

def find_missing_opls(opls_atoms,atoms):
    for j in range(0,len(atoms)):
        if atoms[j].opls_id == 0:
            print "atom %s is missing opls" % atoms[j].atom_id

def find_specifc_angles(angles):
    for i in range(len(angles)):
        if angles[i].Angle_master.atom_type == "C" and angles[i].Angle_slave1.atom_type == "S" and angles[i].Angle_slave2.atom_type == "H":
            print "some angle here"
        elif angles[i].Angle_master.atom_type == "C" and angles[i].Angle_slave2.atom_type == "S" and angles[i].Angle_slave1.atom_type == "H":
            print "some other angle here"
