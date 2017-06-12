import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui

app = QtGui.QApplication([])
win = QtGui.QWidget()

layout = QtGui.QGridLayout()
win.setLayout(layout)

iv = pg.ImageView()
pw = pg.PlotWidget()

img = (np.random.random((300, 200)) * 255).astype('uint8')

data = np.zeros(((255,) + img.shape))
for i in xrange(255):
    data[i, :, :] = np.where(img > i, img, 0)
    prof = np.array([data[i, :, x].sum() for x in xrange(data.shape[2])])

iv.setImage(data, xvals=np.linspace(0, 255, data.shape[0]))
layout.addWidget(iv, 0, 1)

pw.setFixedWidth(100)
pw.setYLink(iv.view)
pw.plot(prof, np.arange(prof.shape[0]))
layout.addWidget(pw, 0, 0)

win.show()

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()