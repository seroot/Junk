import sys

def dft(dihedrals):
    """Writes dft calculations for nwchem. This is wrong. Uses dihedrals. Runs

       Keyword Arguments:
       dihedrals - The list of dihedrals to generate a nwchem output from. If the dihedral is marked as dft it will run
    """
    dftfile = open('outputs/dft.nw','w')
    sys.stdout = dftfile

    print 'title "SMDPPEH with displacement: 04.00 Angstroms"\n'
    counter = "A"
    for i in range(len(dihedrals)):
        if dihedrals[i].dft:
            print 'geometry mol%s units angstroms noautoz noautosym' % counter
            print "%s %s %s %s" % (dihedrals[i].dihedral_master1.atom_type,dihedrals[i].dihedral_master1.x_pos,dihedrals[i].dihedral_master1.y_pos,dihedrals[i].dihedral_master1.z_pos)
            print "%s %s %s %s" % (dihedrals[i].dihedral_master2.atom_type,dihedrals[i].dihedral_master2.x_pos,dihedrals[i].dihedral_master2.y_pos,dihedrals[i].dihedral_master2.z_pos)
            print "%s %s %s %s" % (dihedrals[i].dihedral_slave1.atom_type,dihedrals[i].dihedral_slave1.x_pos,dihedrals[i].dihedral_slave1.y_pos,dihedrals[i].dihedral_slave1.z_pos)
            print "%s %s %s %s" % (dihedrals[i].dihedral_slave2.atom_type,dihedrals[i].dihedral_slave2.x_pos,dihedrals[i].dihedral_slave2.y_pos,dihedrals[i].dihedral_slave2.z_pos)
            print "end\n"
            counter = chr(ord(counter)+1)

    print "basis"
    print " * library 6-31++G*"
    print "end\n"

    counter = "A"
    for i in range(len(dihedrals)):
        if dihedrals[i].dft:
            print "set geometry mol%s" % counter
            print "dft"
            print " cdft 1 60 charge -1"
            print "end\n"
            print "task dft ignore\n"
            counter = chr(ord(counter)+1)
    dftfile.close()
