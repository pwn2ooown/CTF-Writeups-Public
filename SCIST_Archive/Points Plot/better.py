import numpy
import matplotlib.pyplot as plt
x = []
y = []
coor_list = open('coordinates.txt', 'r').read().splitlines()
for coor in coor_list:
	x.append(int(coor.split(" ")[0]))
	y.append(int(coor.split(" ")[1]))
xs = numpy.array(x)
ys = numpy.array(y)
plt.scatter(xs, ys,s=5)
# plt.gca().invert_xaxis()
plt.gca().invert_yaxis()
plt.savefig('plot.png')