#!usr/bin/python
import sys
import matplotlib.pyplot as plt
import glob
import numpy
from scipy.optimize import curve_fit
import pylab

def extract_Temp_Dens( Filename ):
	File = open(Filename)
	Temp = []
	Density = []
	Volume = []
	Enthalpy = []

	for line in File:
		line = line.split()
		try:
			if (float(line[0]>0.0)):
				Temp.append(float(line[0]))
				Density.append(float(line[2]))
				Volume.append(float(line[1]))
				Enthalpy.append(float(line[4]))
		except:
			continue
	Temp = numpy.asarray(Temp)
	Density = numpy.asarray(Density)
	Volume = numpy.asarray(Volume)
	Enthalpy = numpy.asarray(Enthalpy)
	return Temp, Density, Volume, Enthalpy

def Convert_Data(Density):
    Temp = [275.,300., 325., 350., 375., 400., 425., 450., 475., 500., 525., 550.]
    DENS = []
    k = 10000
    P = 2500
    for i in range(len(Temp)):
        DENS.append(numpy.mean(Density[k:(P+k)]))
        k+= 10000
    Temp = numpy.asarray(Temp)
    DENS = numpy.asarray(DENS)
    return Temp, DENS

def linear(x, a, b):
    return a*x + b

Temp, Density, Volume, Enthalpy = extract_Temp_Dens(sys.argv[1])

Temp = Temp - 273.15
T,D = Convert_Data(Density)

snr = []

Tg = T[6:10]
Dg = D[6:10]
Tm = T[0:5]
Dm = D[0:5]

ymax = D[0] + .05
ymin = D[len(D)-1] - .05

m,b = pylab.polyfit(Tg,Dg,1)
m1, b1 = pylab.polyfit(Tm,Dm,1)

print "P3HT", m, b, m1, b1
print T, D

plt.subplot(121)
plt.xlim([5000,150000])
plt.ylim([ymin,ymax])
plt.xlabel('Time Step', fontsize = 30)
plt.ylabel('Density (g/cm^3)', fontsize = 30)
plt.plot(Density,'k',label = 'TIPS Pentacene')
plt.subplot(122)
plt.ylabel('Density (g/cm^3)', fontsize = 30 )
plt.ylim([ymin,ymax])
plt.xlabel('Temperature (Kelvin)', fontsize = 30)
plt.plot(T, D,'o', label = 'TIPS Pentacene')
x = numpy.linspace(225,600,100)
plt.plot(x, m*x + b)
plt.plot(x, m1*x + b1)

plt.legend(loc="upper left")
plt.show()
