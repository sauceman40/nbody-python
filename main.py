#!/usr/bin/python
import matplotlib
matplotlib.use('TKAgg')
from gui import NBodyGUI


if __name__ == '__main__':
	gui = NBodyGUI(None)
	gui.title("N-Body Simulator")
	gui.mainloop()
