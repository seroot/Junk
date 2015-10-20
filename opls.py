def splitList(oplslist):
    """ Splits the opls file to make it easier to read and process in other methods.
        Returns a list of all the data in the opls file

        Keyword Arguments:
        oplslist - The original opls file to process
    """
    bigList = []
    for i in range(0,len(oplslist)):
        split = oplslist[i].split()
        bigList.append(split)
    return bigList

def getImportant(oplslist):
    """ Gets the lines from the opls data file and seperates them by category

        Keyword Arguments:
        oplslist - The list of opls data to get the lines from
    """
    atomList = []
    vanList = []
    partialList = []
    bondList = []
    angleList = []
    torsionList = []
    for i in range(0,len(oplslist)):
        curline = oplslist[i]
        if curline[0] == "atom":
            atomList.append(curline)
        elif curline[0] == "vdw":
            vanList.append(curline)
        elif curline[0] == "charge":
            partialList.append(curline)
        elif curline[0] == "bond":
            bondList.append(curline)
        elif curline[0] == "angle":
            angleList.append(curline)
        elif curline[0] == "torsion":
            torsionList.append(curline)
    return atomList,vanList,partialList,bondList,angleList,torsionList

def count_atoms(opls_atoms,atoms):
    """ Counts the type of atoms found in the opls file for the molecule

        Keyword Arguments:
        opls_atoms - The list of Opls Atoms created in the oplsparse file
        atoms - The list of atoms that get values assigned to them and used throughout
    """
    for i in range(0,len(opls_atoms)):
        counter = 0
        for j in range(0,len(atoms)):
            if atoms[j].opls_id == opls_atoms[i].opls_id:
                counter += 1
        if counter != 0:
            print "There are %s of opls_id #%s" % (counter,opls_atoms[i].opls_id)
