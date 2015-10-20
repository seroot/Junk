
import os
import atom
import bond
import angle
import dihedral

class Rigid_Body(object):

    def __init__(self, R_ID):
        self.R_ID = R_ID
        self.Atom_List = []
        self.N = 0
        self.COM = [0.0, 0.0, 0.0]
        self.Side_Carbon = []
        self.numSC = 0
        self.endgroup = False
        return


    def add_atom(self, atom):
        self.Atom_List.append(atom)
        self.N += 1
        return

    def add_SC(self, atom):
        self.Side_Carbon.append(atom)
        self.numSC += 1
        return


    def calculate_COM(self):
        Pos_X = 0.0
        Pos_Y = 0.0
        Pos_Z = 0.0
        Mass = 0.0
        for atomobj in self.Atom_List:
            Pos_X += float(atomobj.mass)*float(atomobj.x_pos)
            Pos_Y += float(atomobj.mass)*float(atomobj.y_pos)
            Pos_Z += float(atomobj.mass)*float(atomobj.z_pos)
            Mass += float(atomobj.mass)

        Pos_X = Pos_X/Mass
        Pos_Y = Pos_Y/Mass
        Pos_Z = Pos_Z/Mass
        self.COM = [ Pos_X, Pos_Y, Pos_Z]
        return
    

    def printinfo(self):
        print self.R_ID, self.N, self.COM, self.numSC




def Find_Rigid_Bodies(Atom_List, Ring_List, Fused_List):

    i = 1
    for Fused_Ring in Fused_List:
        Rings = [Fused_Ring.ring1, Fused_Ring.ring2]
        for ring in Rings:
            if ring.ring_type == 5:
                ring.atom1.Rigid_Body_ID = i
                ring.atom2.Rigid_Body_ID = i
                ring.atom3.Rigid_Body_ID = i
                ring.atom4.Rigid_Body_ID = i
                ring.atom5.Rigid_Body_ID = i
            elif ring.ring_type == 6:
                ring.atom1.Rigid_Body_ID = i
                ring.atom2.Rigid_Body_ID = i
                ring.atom3.Rigid_Body_ID = i
                ring.atom4.Rigid_Body_ID = i
                ring.atom5.Rigid_Body_ID = i
                ring.atom6.Rigid_Body_ID = i
    i += 1
    Rigid_List = []
    i=0
    for ring in Ring_List:
        if ring.fused == False:
            if ring.ring_type == 5:
                ring.atom1.Rigid_Body_ID = i
                ring.atom2.Rigid_Body_ID = i
                ring.atom3.Rigid_Body_ID = i
                ring.atom4.Rigid_Body_ID = i
                ring.atom5.Rigid_Body_ID = i
                
                Rigid_List.append(Rigid_Body(i))
                Rigid_List[i].add_atom(ring.atom1)
                Rigid_List[i].add_atom(ring.atom2)
                Rigid_List[i].add_atom(ring.atom3)
                Rigid_List[i].add_atom(ring.atom4)
                Rigid_List[i].add_atom(ring.atom5)
                
                
                ring.atom1.fixed= True
                ring.atom2.fixed= True
                ring.atom3.fixed= True
                ring.atom4.fixed= True
                ring.atom5.fixed= True
            elif ring.ring_type == 6:
                ring.atom1.Rigid_Body_ID = i
                ring.atom2.Rigid_Body_ID = i
                ring.atom3.Rigid_Body_ID = i
                ring.atom4.Rigid_Body_ID = i
                ring.atom5.Rigid_Body_ID = i
                ring.atom6.Rigid_Body_ID = i
                
                Rigid_List.append(Rigid_Body(i))
                Rigid_List[i].add_atom(ring.atom1)
                Rigid_List[i].add_atom(ring.atom2)
                Rigid_List[i].add_atom(ring.atom3)
                Rigid_List[i].add_atom(ring.atom4)
                Rigid_List[i].add_atom(ring.atom5)
                Rigid_List[i].add_atom(ring.atom6)
            
                ring.atom1.fixed= True
                ring.atom2.fixed= True
                ring.atom3.fixed= True
                ring.atom4.fixed= True
                ring.atom5.fixed= True
                ring.atom6.fixed= True
            
            i += 1
    print "Found a total of %d rigid bodies in the molecule" % i
    print "Adding hydrogens"
    j = 0

    for atom in Atom_List:
        if atom.atom_type == 'H' and atom.fixed == False:
            for bond in atom.atom_bonds:
                if bond.ring == True:
                    atom.fixed = True
                    atom.Rigid_Body_ID = bond.Rigid_Body_ID
                    Rigid_List[bond.Rigid_Body_ID].add_atom(atom)
                    print "Found an aromatic hydrogen"
                    j +=1

    print "found %d aromatic hydrog-ends" % j
    j =0
    k = 0

    for atom in Atom_List:
        if atom.fixed == False and atom.atom_type == 'C':
            for bond in atom.atom_bonds:
                if bond.ring == True and atom.SC == False:
                    atom.fixed = True
                    atom.Rigid_Body_ID = bond.Rigid_Body_ID
                    atom.SC = True
                    Rigid_List[bond.Rigid_Body_ID].add_SC(atom)
                    print "found carbon", atom.Rigid_Body_ID, atom.atom_id
                    j += 1
                    for bond in atom.atom_bonds:
                        if bond.atom_type == 'H':
                            bond.SC = True
                            bond.fixed = True
                            bond.Rigid_Body_ID = atom.Rigid_Body_ID
                            print "found Hydrogen", atom.Rigid_Body_ID, atom.atom_id
                        if bond.atom_type == 'C' and bond.fixed == False:
                            bond.SC = True
                            print "found floppy carbon",  bond.atom_id
                            k+=1

    for atom in Atom_List:
        if atom.fixed == False:
            atom.SC = True
            print "Found floppy atom", atom.atom_id, atom.atom_type
            k+= 1




    print "found %d sidechains" % j
    print "found %d floppy carbons" % k
    
    for Rigidobj in Rigid_List:
        Rigidobj.calculate_COM()
        Rigidobj.printinfo()




    return Rigid_List



def Add_Ghost(Rigid_List, Atom_List, Bond_List, Angle_List, Dihedral_List):
    Ghost_ID =  len(Atom_List) + 1
    print Ghost_ID
    Nend = max(rigidobj.N for rigidobj in Rigid_List)
    print "Number of atoms in a rigid endgroup", Nend
    i = 0
    for Rigidobj in Rigid_List:
        i += 1
        Temp_Atom = atom.Atom(str(Ghost_ID), "G", str(Rigidobj.COM[0]), str(Rigidobj.COM[1]), str(Rigidobj.COM[2]))
        Atom_List.append(Temp_Atom)
        Rigidobj.add_atom(Temp_Atom)
        print Rigidobj.N
        print len(Atom_List)
        print Ghost_ID
        print "Added Ghost", Ghost_ID
        if i > 1:
            print "Adding Bond"
            Bond_List.append(bond.Bond("G", Atom_List[-1], Atom_List[-2]))
        if i > 2:
            Angle_List.append(angle.Angle("G", Atom_List[-1], Atom_List[-2], Atom_List[-3]))
        if i > 3:
            Temp_Dihedral = dihedral.Dihedral(Atom_List[-1], Atom_List[-2], Atom_List[-3], Atom_List[-4])
            Temp_Dihedral.k1 ="Huang"
            Temp_Dihedral.k2 = "1.0"
            Temp_Dihedral.k3 = "1.0"
            Temp_Dihedral.k4 = "1.0"
            Dihedral_List.append(Temp_Dihedral)
        Ghost_ID += 1
    



    return
        
            
        



