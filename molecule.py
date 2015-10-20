class Molecule(object):
    """docstring for Molecule"""
    atoms = []
    bonds = []
    angles = []
    dihedrals = []
    rings = []
    fused_rings = []

    def __init__(self,a,b,an,di,ri,fr):
        self.atoms = a
        self.bonds = b
        self.angles = an
        self.dihedrals = di
        self.rings = ri
        self.fused_rings = fr

def create_molecule(a,b,an,di,ri,fr):
    """ Creates a molecule object with all the data gathered and calculated from
        the input cml file

        Keyword Arguments:
        a - The list of atoms to add to the molecule
        b - The list of bonds to add to the molecule
        an - The list of angles to add to the molecule
        di - The list of dihedrals to add to the molecule
        ri - The list of rings to add to the molecule
        fr - The list of fused rings to add to the monomer
    """
    molecule = Molecule(a,b,an,di,ri,fr)
    return molecule
