from pylasdev import *
#from mnem_base import *

# Simple test with full LAS output for LAS reader

file = "test_data/1475IBK3.las" # bashneft cp866 # 11

las_info = read_las_file(file)


if(las_info is None):
	print "Error, file not readed!"
else:
	print "=== Curves:"
	for k in xrange(len(las_info['curves_order'])):
		print "  ", k, las_info['curves_order'][k]

	print "=== Logs:"
	for key_ordered in las_info['curves_order']:
		print "  ",  key_ordered, [key_ordered], [las_info['logs'][key_ordered]]

depthcurve = las_info['logs'][las_info['curves_order'][0]][-1000:]
curve = las_info['logs'][las_info['curves_order'][2]][-1000:]
import numpy as np
import matplotlib.pyplot as plt
import math
from tools import *


curve = np.log(curve)

len = depthcurve.shape[0]
depthcurve2 = depthcurve + create_distortion_array(len)

# creates noize in data
curve2 = np.array(curve, copy=True) + np.random.random_sample(len)

# plots initial curve and morthed curve
plt.figure(1)
plt.subplot(141)
plt.plot(curve, -depthcurve)
#plt.plot(curve2, -depthcurve2, color='red')
plt.title(las_info['curves_order'][2])


full_spectrum, filtered_curve = low_pass_filter(curve, 6)
low_spectrum = np.array(full_spectrum, copy=True)
low_spectrum[6:] = 0.0

plt.plot(filtered_curve, -depthcurve, color='red')

plt.subplot(142)
print full_spectrum.shape[0]
plt.plot(full_spectrum, -np.arange(len/2+1))
#plt.plot(low_spectrum, -np.arange(len/2+1), linestyle='None', marker='.', color = 'red')
plt.xlim((-50, 200))


zero_points, zero_values = find_zeros(filtered_curve, depthcurve)
zero_points2, zero_values = find_zeros(filtered_curve, depthcurve2)

plt.subplot(143)
plt.plot(filtered_curve, -depthcurve)
plt.plot(filtered_curve, -depthcurve2, color='red')
plt.plot(zero_values, -zero_points, linestyle='None', color='blue', marker='o')
plt.plot(zero_values, -zero_points2, linestyle='None', color='red', marker='o')



improved_points = genetics(filtered_curve, depthcurve, zero_points, zero_values)


plt.subplot(144)
plt.plot(filtered_curve, -depthcurve)
plt.plot(filtered_curve, -depthcurve2, color='red')
plt.plot(zero_values, -zero_points, linestyle='None', color='blue', marker='o')
plt.plot(zero_values, -zero_points2, linestyle='None', color='red', marker='o')
plt.plot(zero_values+0.5, -improved_points, linestyle='None', color='yellow', marker='*', markersize=10)



plt.show()



















