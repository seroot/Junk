import bond
import time

class Ring(object):
    """Docstring for Ring"""
    ring_type = 0
    improper = False
    fused = False
    thio = False
    atom1 = ""
    atom2 = ""
    atom3 = ""
    atom4 = ""
    atom5 = ""
    atom6 = ""

    def __init__(self,a1,a2,a3,a4,a5,a6=None):
        self.atom1 = a1
        self.atom2 = a2
        self.atom3 = a3
        self.atom4 = a4
        self.atom5 = a5
        self.atom6 = a6

        a1.ring = True
        a2.ring = True
        a3.ring = True
        a4.ring = True
        a5.ring = True

        self.ring_type = 5
        if a6 != None:
            self.ring_type = 6
            a6.ring = True

    def list(self):
        rList = []
        rList.append(self.atom1)
        rList.append(self.atom2)
        rList.append(self.atom3)
        rList.append(self.atom4)
        rList.append(self.atom5)
        if self.atom6 != None:
            rList.append(self.atom6)
        return rList

    def list_type(self):
        rList = []
        rList.append(self.atom1.atom_type)
        rList.append(self.atom2.atom_type)
        rList.append(self.atom3.atom_type)
        rList.append(self.atom4.atom_type)
        rList.append(self.atom5.atom_type)
        if self.atom6 != None:
            rList.append(self.atom6.atom_type)
        return rList

def create_rings(atoms):
    """ Creates Ring object through the use of following each atom's bonds

        Keyword Arguments:
        atoms - The list of atom objects to find the rings
    """
    ring = []
    ringlist = []
    for i in range(len(atoms)):
        layer1 = atoms[i]
        if layer1.ring:
            continue
        path = []
        path.append(layer1)
        for j in range(len(layer1.atom_bonds)):
            layer2 = layer1.atom_bonds[j]
            if layer2 in path:
                continue
            path.append(layer2)
            for k in range(len(layer2.atom_bonds)):
                layer3 = layer2.atom_bonds[k]
                if layer3 in path:
                    continue
                path.append(layer3)
                for l in range(len(layer3.atom_bonds)):
                    layer4 = layer3.atom_bonds[l]
                    if layer4 in path:
                        continue
                    path.append(layer4)
                    for m in range(len(layer4.atom_bonds)):
                        layer5 = layer4.atom_bonds[m]
                        if layer5 in path:
                            continue
                        for n in range(len(layer5.atom_bonds)):
                            layer6 = layer5.atom_bonds[n]
                            if layer6 == path[0]:
                                ringlist.append(Ring(layer1,layer2,layer3,layer4,layer5))
                                layer1.ring = True
                                layer2.ring = True
                                layer3.ring = True
                                layer4.ring = True
                                layer5.ring = True
                            if layer6 in path:
                                continue
                            path.append(layer6)
                            for o in range(len(layer6.atom_bonds)):
                                layer7 = layer6.atom_bonds[o]
                                if layer7 == path[0]:
                                    ringlist.append(Ring(layer1,layer2,layer3,layer4,layer5,layer6))
                                    layer1.ring = True
                                    layer2.ring = True
                                    layer3.ring = True
                                    layer4.ring = True
                                    layer5.ring = True
                                    layer6.ring = True

    return ringlist
