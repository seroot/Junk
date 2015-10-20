import dihedral
import ring
import sys
import bond
import atom
import copy

class Monomer(object):
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

def create_monomer(a,b,an,di,ri,fr):
    """ Creates a monomer object with all the data gathered and calculated from
        the input cml file

        Keyword Arguments:
        a - The list of atoms to add to the monomer
        b - The list of bonds to add to the monomer
        an - The list of angles to add to the monomer
        di - The list of dihedrals to add to the monomer
        ri - The list of rings to add to the monomer
        fr - The list of fused rings to add to the monomer
    """
    if len(ri) != 2:
        print "\nWARNING:"
        print "Not valid monomer for cmlparser"
        print "\nQuitting cmlparser. Check that there are exactly 2 rings.\n"
        quit()
    monomer = Monomer(a,b,an,di,ri,fr)
    return monomer

def mark_thio(monomer):
    """ Mark the thiophene rings in the the monomer by setting the boolean in
        each ring object as well as returning a list of thiophene rings just in
        case they need to be used later.

        Keyword Arguments:
        monomer - The monomer you want to set thiophene rings from. It contains
                  the ring data to set.
    """
    monolist = []
    for i in range(len(monomer.rings)):
        if monomer.rings[i].ring_type == 5:
            mlist = monomer.rings[i].list_type()
            for j in range(4):
                if "C" in mlist:
                    mlist.remove("C")
                else:
                    break
            if "S" in mlist:
                monomer.rings[i].thio = True
                monolist.append(monomer.rings[i])
        else:
            continue
    return monolist

def find_intermono(monomer):
    """ Find the intermonomer dihedral to get a vector from. It just takes a
        single monomer. Right now it just works for the initial one, but theoretically
        it should work for a polymer, just not tested yet.

        Keyword Arguments:
        monomer - The monomer you want to get the intermonomer dihedral
    """
    intermono = ""
    masterbond = ""
    slavebond = ""
    ringlist = monomer.rings[0].list()
    for i in range(len(ringlist)):
        for j in range(len(ringlist[i].atom_bonds)):
            if ringlist[i].atom_bonds[j].ring == True and ringlist[i].atom_bonds[j] not in ringlist:
                masterbond = ringlist[i]
                slavebond = ringlist[i].atom_bonds[j]
    intermono = dihedral.find_dihedral(masterbond,slavebond,monomer.dihedrals)
    return intermono

def get_single_alist(monomer):
    """ Gets a single instance of the monomer to continue to attach. It returns
        a new monomer object with all the relevant data, hopefully.

       Keyword Arguments:
       monomer - The monomer you want to get a single monomer from once you have
                 found the intermonomer dihedral.
    """
    atomlist = monomer.atoms
    bondlist = monomer.bonds
    rings = monomer.rings
    goodring = monomer.rings[len(rings)-2].list()
    badring = monomer.rings[len(rings)-1].list()
    partmono = []
    notgood = []
    checked = []
    for i in range(len(goodring)):
        partmono.append(goodring[i])
        checked.append(goodring[i])
    while len(partmono) != len(atomlist)/len(rings):
        for i in range(len(partmono)):
            for j in range(len(partmono[i].atom_bonds)):
                if partmono[i].atom_bonds[j] in partmono:
                    continue
                if partmono[i].atom_bonds[j] in badring:
                    continue
                else:
                    partmono.append(partmono[i].atom_bonds[j])
    return partmono

def find_attach(polymer,partmono):
    """ Given a monomer/polymer with 2 ends, find which atoms you can attach to. returns
        a list. Which one to add to will be added randomly.

        Keyword Arguments:
        monomer - The monomer/polymer you want to find where to attach the next monomer to
    """
    anglelist = polymer.angles
    for i in range(len(anglelist)):
        if anglelist[i].Angle_master.atom_type == "C" and anglelist[i].Angle_slave1.atom_type == "H" and anglelist[i].Angle_slave2.atom_type == "S" and anglelist[i].Angle_slave1 in partmono:
            return anglelist[i].Angle_master
        elif anglelist[i].Angle_master.atom_type == "C" and anglelist[i].Angle_slave1.atom_type == "S" and anglelist[i].Angle_slave2.atom_type == "H" and anglelist[i].Angle_slave2 in partmono:
            return anglelist[i].Angle_master
    print "No valid attachment point found"

def getpartblist(partmono,monomer,newatoms,add):
    partmonobonds = []
    for i in range(len(partmono)):
        for j in range(len(monomer.bonds)):
            if monomer.bonds[j].bond_master == partmono[i]:
                bondscopy = copy.deepcopy(monomer.bonds[j])
                newmast = atom.get_atombyid(newatoms,int(monomer.bonds[j].bond_master.atom_id) + add)
                newslave = atom.get_atombyid(newatoms,int(monomer.bonds[j].bond_slave.atom_id) + add)
                bondscopy.bond_master = newmast
                bondscopy.bond_slave = newslave
                partmonobonds.append(bondscopy)
    return partmonobonds

def attach(partmono,attach1,monomer,number): #needs more work, very specific right now
    monomernew = monomer
    num = int(number)
    for run in range(0,num):
        add = int(monomernew.atoms[-1].atom_id)
        newalist = []
        newblist = []
        #remove bonds in old attach and remove the hydrogen as well
        for i in range(len(attach1.atom_bonds)):
            if attach1.atom_bonds[i].atom_type == "H": #this has to do in a specific manner, may have to change
                oldh = attach1.atom_bonds[i]
                attachid = attach1.atom_id
        abond = bond.get_bond(attach1,oldh,monomernew.bonds)
        monomernew.bonds.remove(abond)
        monomernew.atoms.remove(oldh)

        #take partmono and offset all of its atoms to create a good atomlist
        for i in range(len(partmono)):
            newalist.append(copy.deepcopy(partmono[i]))
            newalist[i].atom_id = int(partmono[i].atom_id) + add
            newalist[i].x_pos = float(newalist[i].x_pos) + (run+1)*-4.000
            print (run+1)*5.000

        #generate new alist, put this kind of stuff into one big method or something
        for i in range(len(newalist)):
            for j in range(len(newalist[i].atom_bonds)):
                newalist[i].atom_bonds[j] = atom.get_atombyid(newalist,int(newalist[i].atom_bonds[j].atom_id)+add)


        #generate new blist
        newblist = getpartblist(partmono,monomer,newalist,add)
        for i in range(len(newblist)):
            if newblist[i].bond_slave == None:
                newblist.remove(newblist[i])
                break
        a5add = atom.get_atombyid(newalist,5+add)
        a37add = atom.get_atombyid(newalist,37+add)

        newblist.append(bond.Bond(1,a5add,a37add))

        #remove the nonetype from addloc so it doesnt fuck shit up
        #add this to newmonomer
        for i in range(len(newalist)):
            monomernew.atoms.append(newalist[i])
        for i in range(len(newblist)):
            monomernew.bonds.append(newblist[i])

        print newalist[0].atom_id
        print monomer.atoms[0].atom_id
        print newalist[0].atom_bonds[1].atom_id
        print newblist[0].bond_master.atom_id
        print newalist[0].x_pos
        print monomer.atoms[0].x_pos

        attach1 = atom.get_atombyid(newalist,int(attachid)+add)

    return monomernew

def print_mono(monomer,filename):
    cml = open('%s.cml' % filename,'w')
    sys.stdout = cml
    print "<molecule>"
    print " <atomArray>"
    for i in range(len(monomer.atoms)):
        print '  <atom id="a%s" elementType="%s" x3="%s" y3="%s" z3="%s"/>' % (monomer.atoms[i].atom_id,monomer.atoms[i].atom_type,monomer.atoms[i].x_pos,monomer.atoms[i].y_pos,monomer.atoms[i].z_pos)
    print " </atomArray>"
    print " <bondArray>"
    for i in range(len(monomer.bonds)):
        print '  <bond atomRefs2="a%s a%s" order="%s"/>' % (monomer.bonds[i].bond_master.atom_id,monomer.bonds[i].bond_slave.atom_id,monomer.bonds[i].bond_type)
    print " </bondArray>"
    print "</molecule>"
    cml.close()

def create_polymer_cml(filename,partmono,attach,monomer,number):
    """ Basically a test for writing a cml from data and creating a 3rd attach"""
    new_cml = open('%s_new.cml' % filename,'w')
    sys.stdout = new_cml
    usedbonds = []
    bondscopy = []
    for i in range(len(monomer.bonds)):
        bondscopy.append(monomer.bonds[i])
    for i in range(len(attach.atom_bonds)):
        if attach.atom_bonds[i].atom_type == "H":
            attach2 = attach.atom_bonds[i]
    abond = bond.get_bond(attach,attach2,monomer.bonds)
    monomer.bonds.remove(abond)
    monomer.atoms.remove(attach2) #find the hydrogen its attached to and remove instead
    add = len(monomer.atoms)+1
    newattach = ""
    anglelist = monomer.angles
    # THIS SHIT IS USELESS. DONT USE FOR ATTACH MODULE
    for i in range(len(anglelist)):
        if anglelist[i].Angle_master.atom_type == "C" and anglelist[i].Angle_slave1.atom_type == "C" and anglelist[i].Angle_slave2.atom_type == "S" and anglelist[i].Angle_master in partmono and anglelist[i].Angle_slave1 in partmono and anglelist[i].Angle_slave2 in partmono:
            newattach = anglelist[i].Angle_master
        elif anglelist[i].Angle_master.atom_type == "C" and anglelist[i].Angle_slave1.atom_type == "S" and anglelist[i].Angle_slave2.atom_type == "C" and anglelist[i].Angle_master in partmono and anglelist[i].Angle_slave1 in partmono and anglelist[i].Angle_slave2 in partmono:
            newattach = anglelist[i].Angle_master
    print "<molecule>"
    print " <atomArray>"
    for i in range(len(monomer.atoms)):
        print '  <atom id="a%s" elementType="%s" x3="%s" y3="%s" z3="%s"/>' % (monomer.atoms[i].atom_id,monomer.atoms[i].atom_type,monomer.atoms[i].x_pos,monomer.atoms[i].y_pos,monomer.atoms[i].z_pos)
    for i in range(len(partmono)):
        print '  <atom id="a%s" elementType="%s" x3="%s" y3="%s" z3="%s"/>' % (int(partmono[i].atom_id)+add,partmono[i].atom_type,float(partmono[i].x_pos)-5.00,float(partmono[i].y_pos),float(partmono[i].z_pos))
    print " </atomArray>"
    print " <bondArray>"
    for i in range(len(monomer.bonds)):
        print '  <bond atomRefs2="a%s a%s" order="%s"/>' % (monomer.bonds[i].bond_master.atom_id,monomer.bonds[i].bond_slave.atom_id,monomer.bonds[i].bond_type)
    for i in range(len(partmono)):
        for j in range(len(partmono[i].atom_bonds)):
            if partmono[i].atom_bonds[j] in partmono:
                bondid = bond.get_bond(partmono[i],partmono[i].atom_bonds[j],bondscopy)
                if bondid in usedbonds:
                    continue
                usedbonds.append(bondid)
                print '  <bond atomRefs2="a%s a%s" order="%s"/>' % (int(partmono[i].atom_id)+add,int(partmono[i].atom_bonds[j].atom_id)+add,bondid.bond_type)
            else:
                continue
    print '  <bond atomRefs2="a%s a%s" order="1"/>' % (attach.atom_id,int(newattach.atom_id)+add-2)
    print " </bondArray>"
    print "</molecule>"
    new_cml.close()
