class Fused_Ring(object):
    """Docstring for Fused_Ring

       Attributes:
       ring1 - The first ring object in the fused ring
       ring2 - The second ring object in the fused ring
    """
    ring1 = ""
    ring2 = ""

    def __init__(self,ring1,ring2):
        self.ring1 = ring1
        self.ring2 = ring2

    def set_fused():
        self.fused = True

def create_fused_rings(rings):
    """ Finds which rings are fused given a list of rings. Returns a list of the
        fused rings

        Keyword Arguments:
        rings - The list of rings to check if there are any fused rings
    """
    fused_rings = []
    for i in range(0,len(rings)):
        outRing = rings[i].list()
        for j in range(0,len(rings)):
            inRing = rings[j].list()
            if outRing == inRing:
                continue
            if rings[i].fused:
                continue
            if rings[j].fused:
                continue
            counter = 0
            for k in range(0,len(outRing)):
                for j in range(0,len(inRing)):
                    if outRing[k] == inRing[j]:
                        counter += 1
                        if counter == 2:
                            fused_rings.append(Fused_Ring(inRing,outRing))
                            rings[i].fused = True
                        continue
    markfused(fused_rings)
    return fused_rings

def markfused(fused):
    for i in range(len(fused)):
        for j in range(len(fused[i].ring1)):
            fused[i].ring1[j].fixed = True
        for j in range(len(fused[i].ring2)):
            fused[i].ring2[j].fixed = True
