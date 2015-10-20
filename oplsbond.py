class OPLS_Bond(object):
    """Docstring for OPLS_Bond"""
    opls_master = ""
    opls_slave = ""
    fc = ""
    el = ""
    id = 0

    def __init__(self,opls_master,opls_slave,fc,el,id):
        self.opls_master = opls_master
        self.opls_slave = opls_slave
        self.fc = fc
        self.el = el
        self.id = id

def create_bonds(bond):
    """ Creates an OPLS bond object which contains the relevant opls data. It returns
        a list of all OPLS bond objects

        Keyword Arguments:
        bond - The list of bond data from getImportant
    """
    opls_bonds = []
    for i in range(0,len(bond)):
        bList = bond[i]
        opls_bonds.append(OPLS_Bond(bList[1],bList[2],bList[3],bList[4],i))
    return opls_bonds
