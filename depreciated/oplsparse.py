import parse as p

class OPLS_Atom(object):
    atom_id = ""
    bond_id = ""
    atom_type = ""
    partial_charge = ""
    sigma = ""
    epsilon = ""

    #constructor
    def __init__(self, atom_id, bond_id, atom_type, partial_charge, sigma, epsilon):
        self.atom_id = atom_id
        self.bond_id = bond_id
        self.atom_type = atom_type
        self.partial_charge = partial_charge
        self.sigma = sigma
        self.epsilon = epsilon

class OPLS_Bond(object):
    bond_master = ""
    bond_slave = ""
    force_const = ""
    equib_len = ""

    #constructor for OPLS_Bond
    def __init__(self, bond_master, bond_slave, force_const, equib_len):
        self.bond_master = bond_master
        self.bond_slave = bond_slave
        self.force_const = force_const
        self.equib_len = equib_len

class OPLS_Angle(object):
    angle_master = ""
    angle_slave1 = ""
    angle_slave2 = ""
    force_const = ""
    equib_len = ""

    def __init__(self, angle_slave1, angle_master, angle_slave2, force_const, equib_len):
        self.angle_master = angle_master
        self.angle_slave1 = angle_slave1
        self.angle_slave2 = angle_slave2
        self.force_const = force_const
        self.equib_len = equib_len

def getAtoms(oplslist):
    """ Reads in oplsaa file and gets the values and ids for the different kinds
        of atoms. Returns a list of all the ids and values associated with the atoms

        Keyword Arguments:
        oplslist - the oplsaa file
    """
    atomList = []
    for i in range(0,len(oplslist)):
        curLine = oplslist[i]
        if curLine[0] == "atom":
            atomList.append(curLine)
    return atomList

def getBonds(oplslist):
    """ Reads in oplsaa file and gets the values and ids for the different kinds
        of bonds. Returns a list of all the ids and values associated with the bonds

        Keyword Arguments:
        oplslist - the oplsaa file
    """
    bondList = []
    for i in range(0,len(oplslist)):
        curLine = oplslist[i]
        if curLine[0] == "bond":
            bondList.append(curLine)
    return bondList

def get_bond(aBond,opls):
    """ Sets the equil_len and force constant for each bond. No returns, is void.

    Keyword Arguments:
    aBond - The list of bonds to set the opls values
    opls - The list of opls bond values created by getBonds
    """
    master_id = p.find_atom_by_id(aBond.bond_master).bond_id
    slave_id = p.find_atom_by_id(aBond.bond_slave).bond_id
    if slave_id == "":
        return
    for i in range(0,len(opls)):
        if master_id == opls[i].bond_master and slave_id == opls[i].bond_slave:
            aBond.bond_force_const = opls[i].force_const
            aBond.bond_equib_len = opls[i].equib_len
        elif master_id == opls[i].bond_slave and slave_id == opls[i].bond_master:
            aBond.bond_force_const = opls[i].force_const
            aBond.bond_equib_len = opls[i].equib_len

def getAngles(oplslist):
    """ Reads in oplsaa file and gets the values and ids for the different kinds
        of angles. Returns a list of all the ids and values associated with the angles

        Keyword Arguments:
        oplslist - the oplsaa file
    """
    bondList = []
    for i in range(0,len(oplslist)):
        curLine = oplslist[i]
        if curLine[0] == "angle":
            bondList.append(curLine)
    return bondList

def get_angles(angle,opls):
    """ Gets the angles from a given opls file and assigns them to the relevant
        angle objects from the parse file. Is a void method

        Keyword Arguments:
        angle - The list of angle objects to add attributes to
        opls - The opls angle objects from the opls file
    """
    #PROBABLY SLIGHTLY INCORRECT TODO
    a_master = p.find_atom_by_id(angle.Angle_master).bond_id
    a_slave1 = p.find_atom_by_id(angle.Angle_slave1).bond_id
    a_slave2 = p.find_atom_by_id(angle.Angle_slave2).bond_id
    if a_slave1 == "" or a_slave2 == "":
        return
    for i in range(0,len(opls)):
        if a_slave1 <= a_slave2:
            oplsList = [a_slave1,a_master,a_slave2]
            if oplsList[0] == opls[i].angle_slave1 and oplsList[1] == opls[i].angle_master and oplsList[2] == opls[i].angle_slave2:
                angle.Angle_equib_len = opls[i].equib_len
                angle.Angle_force_const = opls[i].force_const
        elif a_slave2 < a_slave1:
            oplsList = [a_slave2,a_master,a_slave1]
            if oplsList[0] == opls[i].angle_slave2 and oplsList[1] == opls[i].angle_master and oplsList[2] == opls[i].angle_slave1:
                angle.Angle_equib_len = opls[i].equib_len
                angle.Angle_force_const = opls[i].force_const

def getVan(oplslist):
    """ Gets the van der waals information from the split opls file. Returns a
        list of the relevant van der waals information

        Keyword Arguments:
        oplslist - The split opls file
    """
    vanList = []
    for i in range(0,len(oplslist)):
        curLine = oplslist[i]
        if curLine[0] == "vdw":
            vanList.append(curLine)
    return vanList

def getPartial(oplslist):
    """ Gets the partial charges from the split opls file
        Returns a list of the relevant partial charge information

        Keyword Arguments:
        oplslist - The split opls file
    """
    partialList = []
    for i in range(0,len(oplslist)):
        curLine = oplslist[i]
        if curLine[0] == "charge":
            partialList.append(curLine)
    return partialList

def splitList(oplslist):
    """ Splits the opls file to make it easier to read and process in other methods.
        Returns a list of all the data in the opls file

        Keyword Arguments:
        oplslist - The original opls file to process
    """
    bigList = []
    for i in range(0,len(oplslist)):
        split = oplslist[i].split()
        bigList.append(split)
    return bigList

def create_opls_atom(atom,van,partial):
    """ Creates and OPLS_Atom object from a the list of opls data found earlier
        Returns a list of all the important opls atom data

        Keyword Arguments:
        atom - The atoms from the opls file to take in and proccess
        van - The van der waals information to take in and proccess from the opls file
        partial - The partial charge information to take in and proccess from the opls file
    """
    opls_atoms = []
    for i in range(0,len(atom)):
        aList =  atom[i]
        vList = van[i]
        pList = partial[i]
        opls_atoms.append(OPLS_Atom(aList[1],aList[2],aList[3],pList[2],vList[2],vList[3]))
    return opls_atoms

def print_opls_atoms(opls_atoms):
    """ Prints the list of opls atoms created earlier in this file

        Keyword Arguments:
        opls_atoms - The list of opls atoms to print
    """
    print "----------OPLS ATOMS----------"
    for i in range(0,len(opls_atoms)):
        print ""
        print opls_atoms[i].atom_type
        print opls_atoms[i].atom_id
        print opls_atoms[i].bond_id
        print opls_atoms[i].sigma
        print opls_atoms[i].epsilon
        print opls_atoms[i].partial_charge

def create_opls_bond(bond):
    """ Creates and OPLS_Bond object from a the list of opls data found earlier
        Returns a list of all the important opls bond data

        Keyword Arguments:
        bond - The bonds from the opls file to take in and proccess
    """
    opls_bonds = []
    for i in range(0,len(bond)):
        bList = bond[i]
        opls_bonds.append(OPLS_Bond(bList[1],bList[2],bList[3],bList[4]))
    return opls_bonds

def print_opls_bonds(opls_bonds):
    """ Prints the list of opls bonds created earlier in this file

        Keyword Arguments:
        opls_bonds - The list of opls bond to print
    """
    print "----------OPLS BONDS----------"
    for i in range(0,len(opls_bonds)):
        print ""
        print opls_bonds[i].bond_master
        print opls_bonds[i].bond_slave
        print opls_bonds[i].force_const
        print opls_bonds[i].equib_len

def create_opls_angle(angle):
    """ Creates and OPLS_Angle object from a the list of opls data found earlier
        Returns a list of all the important opls angle data

        Keyword Arguments:
        angle - The angles from the opls file to take in and proccess
    """
    opls_angles = []
    for i in range(0,len(angle)):
        anList = angle[i]
        opls_angles.append(OPLS_Angle(anList[1],anList[2],anList[3],anList[4],anList[5]))
    return opls_angles

def print_opls_angles(opls_angles):
    """ Prints the list of opls angles created earlier in this file

        Keyword Arguments:
        opls_angles - The list of opls angles to print
    """
    print "----------OPLS ANGLES----------"
    for i in range(0,len(opls_angles)):
        print ""
        print opls_angles[i].angle_master
        print opls_angles[i].angle_slave1
        print opls_angles[i].angle_slave2
        print opls_angles[i].force_const
        print opls_angles[i].equib_len
