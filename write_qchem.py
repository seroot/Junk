import sys
import os

def write(atoms,dihedrals):
    """Writes a bunch of qchem files (named qchem1,qchem2,etc) to run and analyze the outputs from.
       Partial charges and setting dft calculations

       Keyword Arguments:
       atoms - The list of atoms to print out at somepoint
       dihedrals - The list of dihedrals to print out at somepoint
    """
    counter = 1
    os.system('rm outputs/qchem/qchem*')
    for j in range(len(dihedrals)):
        if dihedrals[j].dft == False:
            continue
        write = open(('outputs/qchem/qchem%s.in') % counter,'w')
        sys.stdout = write

        print "$rem"
        print "JOBTYPE OPT"
        print "EXCHANGE B3LYP"
        print "BASIS 6-31+G**"
        print "MAX_SCF_CYCLES 200"
        print "$end\n"
        print "$opt"
        print "CONSTRAINT"
        print "tors %s %s %s %s 0.0" % (dihedrals[j].dihedral_master1.atom_id,dihedrals[j].dihedral_master2.atom_id,dihedrals[j].dihedral_slave1.atom_id,dihedrals[j].dihedral_slave2.atom_id)
        print "ENDCONSTRAINT"
        print "$end\n"
        print "$molecule"
        print "#charge spinmultiplicity"
        print "0 1"
        for i in range(len(atoms)):
            print " %s %s %s %s" % (atoms[i].atom_type,atoms[i].x_pos,atoms[i].y_pos,atoms[i].z_pos)
        print "$end"

        counter += 1

        write.close()
