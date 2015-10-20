# lammps parameters explained
#### If there are missing types for any parameter, read the lammps documentation. I am just listing some common ones here that I have used. Most of this is taken from the lammps documentation. Some of it is simplified. Credit to lammps documentation

Note a star next to parentheses notes it may not apply to all types

**units (type)**
* type
 * real - Uses real units, look at lammps documentation. This is recommended.

**atom_style (type)**
* type
 * molecular - bonds, angles, dihedrals, and impropers
 * full - molecular but adds in charge (recommended)
 * atomic - default

**boundary (x) (y) (z)**
* x,y,z (all have same flags)
 * p - Periodic boundary (interact across boundary)
 * f - Non-Periodic boundary that is fixed (if particle moves outside, gets deleted)
 * s - Non-Periodic boundary that is shrink-wrapped (encompasses all atoms no matter how far they move)

**bond_style (type)**
* type
 * harmonic - harmonic bonds
 * none - Turn off bonded interactions

**dielectric (const)**
* const
 * Sets a dielectric constant for colombic interactions. Applies when using certain pair_style

**pair_style (type) *(const)**
* type
 * lj/cut - cutoff Lennard-Jones potential with no Coulomb.
 * lj/cut/coul/cut - lj potential for use with Coulomb interactions.
 * lj/cut/coul/long - lj potential for use with Coulomb interactions
* const
 * The cutoff distance

**angle_style (type)**
* type
 * harmonic - Harmonic angles
 * table - A table containing tabulated values. This has two additional flags. Look at lammps documentation

**dihedral_style (type)**
* I believe you should always use opls due to the program.

**special_bonds (type) (flag1) (flag2) (flag3) (etc)**
* type 

**improper_style (type)**

**kspace_style (type) *()**

**read_data (filename)**
* filename
 * Dont touch this flag

**thermo_style () () () () () () () ()**

**dump () () () () () () () () () () () () () () ()**

**neighbor () ()**

**neigh_modify () () () () () () ()**

**fix () () () () () () () () () ()**

**velocity () () () ()**

**timestep (time)**

**thermo ()**

**run (time)**

**write_restart (name)**

**replicate () () ()**
