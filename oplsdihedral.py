class OPLS_Dihedral(object):
    """Docstring for OPLS_Dihedral"""
    opls_master1 = ""
    opls_master2 = ""
    opls_slave1 = ""
    opls_slave2 = ""
    k1 = ""
    k2 = ""
    k3 = ""
    k4 = ""

    def __init__(self,m1,m2,s1,s2,k1,k2,k3):
        self.opls_master1 = m1
        self.opls_master2 = m2
        self.opls_slave1 = s1
        self.opls_slave2 = s2
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3
        self.k4 = 0.000

def create_dihedrals(dihedral):
    """ Creates an OPLS dihedral object which contains the relevant opls data. It returns
        a list of all OPLS dihedral objects

        Keyword Arguments:
        dihedral - The list of dihedral data from getImportant
    """
    opls_dihedrals = []
    for i in range(0,len(dihedral)):
        dList = dihedral[i]
        opls_dihedrals.append(OPLS_Dihedral(dList[2],dList[3],dList[1],dList[4],dList[5],dList[8],dList[11]))
    return opls_dihedrals
