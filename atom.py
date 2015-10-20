import os

class Atom(object):
    """Docstring for Atom"""
    atom_id = ""
    atom_type = ""
    x_pos = 0.0000
    y_pos = 0.0000
    z_pos = 0.0000
    numbonds = 0
    atom_bonds = []
    ring = False
    opls_id = 0
    opls_bondid = 0
    opls_partial = 0
    opls_sigma = 0
    opls_epsilon = 0
    opls_mass = 0
    mass = 0
    print_type = 0
    dihedral = False
    fixed = False
    ring = False
    Rigid_Body_ID = 0
    SC = False
    UA = False
    Mol_id = 0

    def __init__(self,atom_id,atom_type,x_pos,y_pos,z_pos):
        self.atom_id = atom_id
        self.atom_type = atom_type
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos
        if atom_type == "C":
            self.mass = 12.011
        elif atom_type == "H":
            self.mass = 1.008
        elif atom_type == "S":
            self.mass = 32.022
        elif atom_type == "G":
            self.mass = 0.0
            self.opls_epsilon = 0.0
            self.opls_sigma = 0.0
            self.opls_mass = 0.0
            self.opls_id = -1

        

def create_atoms(atom):
    """ Creates the atom objects

        Keyword Arguments:
        atom - A list of atom data
    """
    atoms = []
    for i in range(0,len(atom)):
        curratom = str(atom[i].attrib).split()
        x = curratom[1].replace(',','').replace("'","")
        y = curratom[3].replace(',','').replace("'","")
        z = curratom[9].replace('}','').replace("'","")
        id = curratom[7].replace('a','').replace(',','').replace("'","")
        type = curratom[5].replace(',','').replace("'","")
        atoms.append(Atom(id,type,x,y,z))
    return atoms

def get_atombyid(atoms,id):
    """ Find an atom by its id in a list of atoms
        Returns the correct atom

        Keyword Arguments:
        atoms - The list of atoms you want to search for a particular id
        id - The id for the atom you want to find
    """
    for i in range(len(atoms)):
        if atoms[i].atom_id == id:
            return atoms[i]

def uniq_types(atom):
    """ Gets the unique type of atoms for lammps output

        Keyword Arguments:
        atom - The list of atom objects to get unique types from
    """
    uniq = []
    uniqadd = []
    for i in range(0,len(atom)):
        if atom[i].opls_id in uniqadd:
            continue
        if atom[i].opls_id == 0:
            continue
        uniq.append(atom[i])
        uniqadd.append(atom[i].opls_id)
    return uniq

def periodic_b_size(atom):
    """ Finds a good periodic boundary size for lammps output. Finds min and max
        for x,y,z data from the atoms

        Keyword Arguments:
        atom - The list of atom objects to get x,y,z positional data from.
    """
    minx = 0
    miny = 0
    minz = 0
    maxx = 0
    maxy = 0
    maxz = 0
    for i in range(0,len(atom)):
        if float(atom[i].x_pos) > float(maxx):
            maxx = atom[i].x_pos
        elif float(atom[i].x_pos) < float(minx):
            minx = atom[i].x_pos
        if float(atom[i].y_pos) > float(maxy):
            maxy = atom[i].y_pos
        elif float(atom[i].y_pos) < float(miny):
            miny = atom[i].y_pos
        if float(atom[i].z_pos) > float(maxz):
            maxz = atom[i].z_pos
        elif float(atom[i].z_pos) < float(minz):
            minz = atom[i].z_pos
    totalmin = float(minx)
    totalmax = float(maxx)
    if float(miny) < totalmin:
        totalmin = float(miny)
    if float(minz) < totalmin:
        totalmin = float(minz)
    if float(maxy) > totalmax:
        totalmax = float(maxy)
    if float(maxz) > totalmax:
        totalmax = float(maxz)
    totalmax += 2
    totalmin -+ 2
    return totalmin,totalmin,totalmin,totalmax,totalmax,totalmax

def get_type(atom,type):
    """ Gets the type of unique atoms it is for lammps output

        Keyword Arguments:
        atom - The list of atom objects
        type - The list of unique types
    """
    for i in range(len(atom)):
        for j in range(len(type)):
            if atom[i].opls_id == type[j].opls_id:
                atom[i].print_type = j+1

def adjust_partials(atoms):
    pctotal = 0
    for i in range(len(atoms)):
        pctotal += float(atoms[i].opls_partial)
    if -.005 < pctotal < .005:
        return
    if pctotal == 0:
        return
    each = pctotal/len(atoms)
    if pctotal > 0:
        for i in range(len(atoms)):
            new = float(atoms[i].opls_partial) - each
            atoms[i].opls_partial = new
    elif pctotal < 0:
        for i in range(len(atoms)):
            new = float(atoms[i].opls_partial) + each
            atoms[i].opls_partial = new
