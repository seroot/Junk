import os

def read_babel_set(filename,atom):
    #os.system('babel -i cml %s -o mol2 %s.mol2' % (filename,filename))

    newfile = '%s.mol2' % filename
    run_antechamber(newfile,atom)

def run_antechamber(filename,atom):
    #os.system('module load amber')
    #os.system('antechamber -i %s -fi mol2 -o %s -fo mol2 -c bcc' % (filename,filename))

    bfile = open(filename)
    blist = bfile.readlines()

    partials = []
    for i in range(len(blist)):
        split1 = blist[i].split()
        if blist[i] == "@<TRIPOS>ATOM\n":
            for j in range(i+1,len(blist)):
                if blist[j] == "@<TRIPOS>BOND\n":
                    break
                else:
                    split = blist[j].split()
                    partials.append(split[8])
    for i in range(len(atom)):
        atom[i].opls_partial = partials[i]
