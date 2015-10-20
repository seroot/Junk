import sys

#DEPRECIATED
def write():
    """ Assists the user in writing an input for the supercomputer comet"""

    sfile = raw_input("What would you like your sbatch filename to be?: ")
    nodes = raw_input("How many nodes would you like to use?: ")
    time = raw_input("How long do you expect it to run (HH:MM:SS)?: ")
    account = raw_input("What account would you like this to run under?: ")
    location = raw_input("Where is the cmlparser_py file directory located?: ")
    cores = raw_input("How many cores would you like the simulation to run on?: ")
    molecule = raw_input("Where is the molecule you would like to run?: ")
    dataname = raw_input("What lammps data filename would you like to use?: ")
    lammpsin = raw_input("What lammps input filename would you like to use?: ")

    infile = open(sfile,'w')
    sys.stdout = infile

    print "#!/bin/bash"
    print '#SBATCH --job-name="%s"' % sfile
    print '#SBATCH --output="job.%j.%N.out"'
    print '#SBATCH --partition=compute'
    print "#SBATCH --nodes=%s" % nodes
    print "#SBATCH --ntasks-per-node=24"
    print "#SBATCH -t %s" % time
    print "#SBATCH -A %s" % account
    print "module load python lammps"
    print "cd %s" % location
    print "ibrun -np %s python cml.py %s %s %s" % (cores,molecule,dataname,lammpsin)

    infile.close()
