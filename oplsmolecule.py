def get_molecule(atom,opls):
    """ Basically runs a bunch of methods to check what kind of atom it is
        Keyword Arguments:
        Same as everything else in this file
        """
    for i in range(0,len(atom)):
        assign_h(atom[i],opls)
        is10(atom[i],opls)
        is13(atom[i],opls)
        is15(atom[i],opls)
        is17(atom[i],opls)
        is26(atom[i],opls)
        is90(atom[i],opls)
        is144(atom[i],opls)
        is177(atom[i],opls)
        is178(atom[i],opls)
        is181(atom[i],opls)
        is660(atom[i],opls)
        is748(atom[i],opls)
        is790(atom[i],opls)
        is866(atom[i],opls)
        is873(atom[i],opls)
        is874(atom[i],opls)

def assign_atom_vars(atom,number,opls):
    """ Assigns the atom object its opls values
        Keyword Arguments:
        atom - The atom object to assin
        number - The opls number to assign it
        opls - The opls object list to use to assign data
        """
    atom.opls_id = opls[number].opls_id
    atom.opls_sigma = opls[number].sigma
    atom.opls_epsilon = opls[number].epsilon
    atom.opls_partial = opls[number].pc #DONT ASSIGN PARTIALS IN OPLS. DO IT IN ANTECHAMBER
    atom.opls_bondid = opls[number].opls_bondid
    atom.opls_mass = opls[number].amass

def gen_bondlist(atom):
    """ A helper method to generate the atom types for use in each ISxxx method
        Keyword Arguments:
        atom - The single atom to generate the bondlist from
        """
    bondlist = []
    for i in range(0,atom.numbonds):
        bondlist.append(atom.atom_bonds[i].atom_type)
    return bondlist

def assign_h(atom,opls):
    """ Assigns hydrogen OPLS ids
        Keyword Arguments:
        atom - The single atom to assign a hydrogen value to
        """
    if atom.atom_type == "H" and atom.numbonds == 1:
        bondlist = atom.atom_bonds
        if bondlist[0].opls_id == "80":
            assign_atom_vars(atom,84,opls)
        elif bondlist[0].opls_id == "81":
            assign_atom_vars(atom,84,opls)
        elif bondlist[0].opls_id == "90":
            assign_atom_vars(atom,90,opls)
        elif bondlist[0].opls_id == "82":
            assign_atom_vars(atom,84,opls)
        elif bondlist[0].opls_id == "874":
            assign_atom_vars(atom,84,opls)

"""
    ----------------------------------------------------
    NOT DOCUMENTING ANYTHING BELOW.
    IGNORING OPLS-UA
    ----------------------------------------------------
    """

def is10(atom,opls): #this is really a 80
    number = 79
    if atom.atom_type == "C" and atom.numbonds == 4:
        bondlist = gen_bondlist(atom)
        if "C" in bondlist:
            bondlist.remove("C")
            if "H" in bondlist:
                bondlist.remove("H")
                if "H" in bondlist:
                    bondlist.remove("H")
                    if "H" in bondlist:
                        assign_atom_vars(atom,number,opls)

def is13(atom,opls): # this is really 81
    number = 80
    if atom.atom_type == "C" and atom.numbonds == 4:
        bondList = gen_bondlist(atom)
        if "H" in bondList:
            bondList.remove("H")
            if "H" in bondList:
                bondList.remove("H")
                if "C" in bondList:
                    bondList.remove("C")
                    if "N" in bondList or "C" in bondList:
                        assign_atom_vars(atom,number,opls)

def is15(atom,opls):
    number = 81
    if atom.atom_type == "C" and atom.numbonds == 4:
        bondList = gen_bondlist(atom)
        if "C" in bondList:
            bondList.remove("C")
            if "C" in bondList:
                bondList.remove("C")
                if "C" in bondList and "H" in bondList:
                    assign_atom_vars(atom,number,opls)

def is17(atom,opls): #this is really a 90
    number = 89
    if atom.atom_type == "C" and atom.numbonds == 3:
        bondList = gen_bondlist(atom)
        if "C" in bondList:
            bondList.remove("C")
            if "C" in bondList and "H" in bondList:
                assign_atom_vars(atom,number,opls)

def is26(atom,opls):
    number = 25
    if atom.atom_type == "S" and atom.numbonds == 2:
        if atom.atom_bonds[0].atom_type == "C" and atom.atom_bonds[1].atom_type == "C":
            assign_atom_vars(atom,number,opls)

def is90(atom,opls):
    number = 89
    if atom.atom_type == "C" and atom.numbonds == 3:
        bondList = gen_bondlist(atom)
        if "C" in bondList:
            bondList.remove("C")
            if "C" in bondList:
                bondList.remove("C")
                if "C" in bondList or "S" in bondList or "N" in bondList:
                    assign_atom_vars(atom,number,opls)

def is144(atom,opls):
    number = 143
    if atom.atom_type == "S" and atom.numbonds == 2:
        print "ran"
        if atom.atom_bonds[0].atom_type == "N" and atom.atom_bonds[1].atom_type == "N":
            assign_atom_vars(atom,number,opls)

def is177(atom,opls):
    number = 176
    if atom.atom_type == "C" and atom.numbonds == 3:
        bondList = gen_bondlist(atom)
        if "C" in bondList and "N" in bondList and "O" in bondList:
            assign_atom_vars(atom,number,opls)

def is178(atom,opls):
    number = 177
    if atom.atom_type == "O" and atom.numbonds == 1:
        if atom.atom_bonds[0].atom_type == "C":
            assign_atom_vars(atom,number,opls)

def is181(atom,opls):
    number = 180
    if atom.atom_type == "N" and atom.numbonds == 3:
        if atom.atom_bonds[0].atom_type == "C" and atom.atom_bonds[1].atom_type == "C" and atom.atom_bonds[2].atom_type == "C":
            assign_atom_vars(atom,number,opls)

def is660(atom,opls):
    number = 659
    if atom.atom_type == "F" and atom.numbonds == 1:
        if atom.atom_bonds[0].atom_type == "C":
            assign_atom_vars(atom,number,opls)

def is748(atom,opls):
    number = 747
    if atom.atom_type == "N" and atom.numbonds == 2:
        bondlist = gen_bondlist(atom)
        if "S" in bondlist:
            bondlist.remove("S")
            if "C" in bondlist:
                assign_atom_vars(atom,number,opls)

def is790(atom,opls):
    number = 789
    if atom.atom_type == "C" and atom.numbonds == 3:
        bondlist = gen_bondlist(atom)
        if "C" in bondlist:
            bondlist.remove("C")
            if "C" in bondlist:
                bondlist.remove("C")
                if "F" in bondlist:
                    assign_atom_vars(atom,number,opls)

def is866(atom,opls):
    number = 865
    if atom.atom_type == "Si" and atom.numbonds == 4:
        # C really should be 'R' random
        if atom.atom_bonds[0].atom_type == "C" and atom.atom_bonds[1].atom_type == "C" and atom.atom_bonds[2].atom_type == "C" and atom.atom_bonds[3].atom_type == "C":
            assign_atom_vars(atom,number,opls)

def is873(atom,opls):
    number = 872
    if atom.atom_type == "C" and atom.numbonds == 3:
        bondlist = gen_bondlist(atom)
        if "C" in bondlist:
            bondlist.remove("C")
            if "C" in bondlist:
                bondlist.remove("C")
                if "Si" in bondlist:
                    assign_atom_vars(atom,number,opls)

def is874(atom,opls):
    number = 873
    if atom.atom_type == "C" and atom.numbonds == 4:
        bondlist = gen_bondlist(atom)
        if "C" in bondlist:
            bondlist.remove("C")
            if "C" in bondlist:
                bondlist.remove("C")
                if "H" in bondlist:
                    bondlist.remove("H")
                    if "Si" in bondlist:
                        assign_atom_vars(atom,number,opls)
        bondlist = gen_bondlist(atom)
        if "C" in bondlist:
            bondlist.remove("C")
            if "H" in bondlist:
                bondlist.remove("H")
                if "H" in bondlist:
                    bondlist.remove("H")
                    if "Si" in bondlist:
                        assign_atom_vars(atom,number,opls)







