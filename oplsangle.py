class OPLS_Angle(object):
    """Docstring for OPLS_Angle"""
    opls_master = ""
    opls_slave1 = ""
    opls_slave2 = ""
    fc = ""
    el = ""

    def __init__(self,opls_master,opls_slave1,opls_slave2,fc,el):
        self.opls_master = opls_master
        self.opls_slave1 = opls_slave1
        self.opls_slave2 = opls_slave2
        self.fc = fc
        self.el = el

def create_angles(angle):
    """ Creates an OPLS Angle object which contains the relevant opls data. It returns
        a list of all OPLS Angle objects

        Keyword Arguments:
        angle - The list of angle data from getImportant
    """
    opls_angles = []
    for i in range(0,len(angle)):
        aList = angle[i]
        opls_angles.append(OPLS_Angle(aList[2],aList[1],aList[3],aList[4],aList[5]))
    return opls_angles
