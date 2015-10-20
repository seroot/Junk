class OPLS_Atom(object):
    """Docstring for OPLS_Atom"""
    opls_id = ""
    opls_bondid = ""
    opls_type = ""
    pc = ""
    sigma = ""
    epsilon = ""
    amass = ""

    def __init__(self,opls_id,opls_bondid,opls_type,pc,sigma,epsilon,amass):
        self.opls_id = opls_id
        self.opls_bondid = opls_bondid
        self.opls_type = opls_type
        self.pc = pc
        self.sigma = sigma
        self.epsilon = epsilon
        self.amass = amass

def create_atoms(atom,van,partial):
    """ Creates an OPLS Angle object which contains the relevant opls data. It returns
        a list of all OPLS Angle objects

        Keyword Arguments:
        atom - The list of atom data from getImportant
        van - The list of vanderwalls data from getImportant
        partial - The list of partial charges from getImportant
    """
    opls_atoms = []
    for i in range(0,len(atom)):
        a = atom[i]
        v = van[i]
        p = partial[i]
        opls_atoms.append(OPLS_Atom(a[1],a[2],a[3],p[2],v[2],v[3],a[7]))
    return opls_atoms
