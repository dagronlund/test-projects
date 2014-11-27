__author__ = 'David'

# import tkinter
#
# top = tkinter.Tk()
#
# C = tkinter.Canvas(top, bg="blue", height=250, width=300)
#
# coord = 10, 50, 240, 210
# arc = C.create_arc(coord, start=0, extent=150, fill="red")
#
# C.pack()
# top.mainloop()

print('fuck the world')

from vispy import mpl_plot as plt

plt.plot([1, 2, 4, 2, 3], color='r')
plt.plot([3, 1, 2, 4, 1], color='b')
# plt.scatter([20, 40], [20, 40])

plt.show(True)