import bond

class Dihedral(object):
    """Docstring for Dihedral"""
    dihedral_eqib_len = ""
    dihedral_force_const = ""
    dihedral_master1 = ""
    dihedral_master2 = ""
    dihedral_slave1 = ""
    dihedral_slave2 = ""
    k1 = ""
    k2 = ""
    k3 = ""
    k4 = ""
    print_type = 0
    dft = False
    intermono = False

    def __init__(self, dihedral_master1, dihedral_master2, dihedral_slave1, dihedral_slave2):
        self.dihedral_master1 = dihedral_master1
        self.dihedral_master2 = dihedral_master2
        self.dihedral_slave1 = dihedral_slave1
        self.dihedral_slave2 = dihedral_slave2

def get_unique(dihedrals):
    """ Remove duplicate dihedrals

        Keyword Arguments:
        dihedrals - List of dihedrals to remove duplicates from
    """
    dihedrals_new = []
    for i in range(0,len(dihedrals)):
        for j in range(0,len(dihedrals)):
            if dihedrals[i] == dihedrals[j]:
                continue
            if dihedrals[i].dihedral_master1 == dihedrals[j].dihedral_master2 and dihedrals[i].dihedral_master2 == dihedrals[j].dihedral_master1:
                if dihedrals[i].dihedral_slave1 == dihedrals[j].dihedral_slave2 and dihedrals[i].dihedral_slave2 == dihedrals[j].dihedral_slave1:
                    dihedrals_new.append(dihedrals[j])
    dihedrals_new = remove_duplicates(dihedrals_new)
    for i in range(0,len(dihedrals_new)):
        dihedrals.remove(dihedrals_new[i])
    return dihedrals

def remove_duplicates(l):
    """ Given any list remove the duplicates from it

        Keyword Arguments:
        l - Any list that you want to remove duplicates from
    """
    return list(set(l))

def create_dihedrals(dihedral,all=False):
    """ Creates the dihedral objects

        Keyword Arguments:
        dihedral - A list of angles to create dihedral from
    """
    dihedrals = []
    for i in range(0,len(dihedral)):
        outlist = [dihedral[i].Angle_master,dihedral[i].Angle_slave1,dihedral[i].Angle_slave2]
        for j in range(0,len(dihedral)):
            if dihedral[i] == dihedral[j]:
                continue
            inF = [dihedral[j].Angle_master,dihedral[j].Angle_slave1]
            inS = [dihedral[j].Angle_slave1,dihedral[j].Angle_slave2]
            inFL = [dihedral[j].Angle_master,dihedral[j].Angle_slave2]
            if outlist[0] in inF and outlist[1] in inF:
                dihedrals.append(Dihedral(outlist[0],outlist[1],outlist[2],inS[1]))
                outlist[0].dihedral = True
                outlist[1].dihedral = True
            elif outlist[0] in inS and outlist[1] in inS:
                dihedrals.append(Dihedral(outlist[0],outlist[1],outlist[2],inF[0]))
                outlist[0].dihedral = True
                outlist[1].dihedral = True
            elif outlist[0] in inFL and outlist[1] in inFL:
                dihedrals.append(Dihedral(outlist[0],outlist[1],outlist[2],inS[0]))
                outlist[0].dihedral = True
                outlist[1].dihedral = True
    dihedrals = get_unique(dihedrals)
    return dihedrals

def find_dihedral(master,slave,dihedrals):
    """ Given a master and slave atom finds the dihedral that they master together.

        Keyword Arguments:
        master - The atom master you want to use in conjunction with the slave master to find the dihedral
        slave - The slave master you want to using in conjunction with the master to find the dihedral
        dihedrals - The list of dihedrals you want to check for this pair of masters
    """
    for i in range(len(dihedrals)):
        if dihedrals[i].dihedral_master1 == master and dihedrals[i].dihedral_master2 == slave:
            return dihedrals[i]
        if dihedrals[i].dihedral_master1 == slave and dihedrals[i].dihedral_master2 == master:
            return dihedrals[i]

def set_opls(dihedrals,opls_dihedrals):
    """ Sets the opls data into the dihedral object

        Keyword Arguments:
        dihedrals - The list of dihedral objects to set opls data into
        opls_dihedrals - The list of opls data to scan
    """
    for i in range(len(dihedrals)):
        masters = [int(dihedrals[i].dihedral_master1.opls_bondid),int(dihedrals[i].dihedral_master2.opls_bondid)]
        slaves = [int(dihedrals[i].dihedral_slave1.opls_bondid),int(dihedrals[i].dihedral_slave2.opls_bondid)]
        masters.sort()
        slaves.sort()
        both = [str(slaves[0]),str(masters[0]),str(masters[1]),str(slaves[1])]
        for j in range(len(opls_dihedrals)):
            if both[0] == opls_dihedrals[j].opls_slave1 and both[1] == opls_dihedrals[j].opls_master1 and both[2] == opls_dihedrals[j].opls_master2 and both[3] == opls_dihedrals[j].opls_slave2:
                dihedrals[i].k1 = opls_dihedrals[j].k1
                dihedrals[i].k2 = opls_dihedrals[j].k2
                dihedrals[i].k3 = opls_dihedrals[j].k3
                dihedrals[i].k4 = opls_dihedrals[j].k4

def uniq_types(dihedrals):
    """ Gets the unique type of dihedrals for lammps output

        Keyword Arguments:
        dihedrals - The list of dihedral objects to get unique types from
    """
    uniq = []
    uniqadd = []
    for i in range(len(dihedrals)):
        if [dihedrals[i].k1,dihedrals[i].k2,dihedrals[i].k3,dihedrals[i].k4] in uniqadd:
            continue
        if dihedrals[i].k1 == "":
            continue
        uniqadd.append([dihedrals[i].k1,dihedrals[i].k2,dihedrals[i].k3,dihedrals[i].k4])
        uniq.append(dihedrals[i])
    return uniq

def get_type(dihedral,type):
    """ Gets the type of unique dihedral it is for lammps output

        Keyword Arguments:
        dihedral - The list of dihedral objects
        type - The list of unique types
    """
    for i in range(len(dihedral)):
        for j in range(len(type)):
            if dihedral[i].k1 == type[j].k1 and dihedral[i].k2 == type[j].k2 and dihedral[i].k3 == type[j].k3 and dihedral[i].k4 == type[j].k4:
                dihedral[i].print_type = j+1

def set_dft(dihedral,bonds):
    """ Given a list of dihedrals find if you should set dft values for those dihedrals or not.
        Sets a boolean on the list of dihedrals that need dft calculations done to them.

        Probably should return a list instead for speed optimization

        Keyword Arguments:
        dihedral - The list of dihedrals you want to check
        bonds - The list of bonds you want to check
    """
    for i in range(len(dihedral)):
        mb1 = bond.get_bond(dihedral[i].dihedral_master1,dihedral[i].dihedral_master2,bonds)
        if mb1.bond_type == '1':
            ob1 = bond.get_bond(dihedral[i].dihedral_master1,dihedral[i].dihedral_slave1,bonds)
            ob2 = bond.get_bond(dihedral[i].dihedral_master2,dihedral[i].dihedral_slave2,bonds)
            if ob1 == None or ob2 == None:
                continue
            if ob1.bond_type == '2' and ob2.bond_type == '2':
                dihedral[i].dft = True
