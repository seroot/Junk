import sys

def set_flags_new():
    """ Sets the various flags specified by a user. Reads from sys.argv """

    # All the variables
    molecule = True
    debug = False
    help = False
    isfile = False
    test = True
    bad = True
    mname = ""
    dataname = ""
    inname = ""
    fname = ""
    length = ""
    UA = False

    # get Molecule or Monomer
    if '-imol' in sys.argv or '-imono' in sys.argv:
        bad = False
    if bad:
        print "You need to specify a cml file to read"
    if '-imol' in sys.argv and '-imono' in sys.argv:
        print "You cannot specify two different kinds of .cml files"
        quit()
    else:
        if '-imol' in sys.argv:
            molecule = True
            mname = sys.argv[get_flag("-imol")]
        elif '-imono' in sys.argv:
            molecule = False
            mname = sys.argv[get_flag("-imono")]

    # Get output data name
    if '-od' not in sys.argv:
        print "You need to specify a lammps data file"
        quit()
    else:
        dataname = sys.argv[get_flag('-od')]

    # Get input lammps name
    if '-oi' not in sys.argv:
        print "You need to specify a lammps input file"
        quit()
    else:
        inname = sys.argv[get_flag('-oi')]

    if '-d' in sys.argv:
        debug = True

    if '-h' in sys.argv:
        help = True
    if '-UA' in sys.argv:
        UA = True

    if '-f' in sys.argv:
        isfile = True
        fname = sys.argv[get_flag('-f')]

    if '-l' in sys.argv:
        length = sys.argv[get_flag('-l')]

    return molecule,mname,dataname,inname,debug,isfile,fname,help,length, UA

def get_flag(string):
    index = 0
    for i in range(len(sys.argv)):
        if sys.argv[i] == string:
            index = i+1
    return index
