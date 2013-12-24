
#
# Copyright 2010-2012 Fabric Technologies Inc. All rights reserved.
#

from PySide.QtCore import QSize
from FabricEngine.SceneGraph.Nodes.Rendering import *
from FabricEngine.SceneGraph.Nodes.Images import *
from FabricEngine.SceneGraph.PySide import *

class SimplexNoiseManipulator(Manipulator):
  
  def __init__(self, scene, simplexNoiseImage, **options):
    
    self.__simplexNoiseImage = simplexNoiseImage
    # self.__moveStartCenter = None
    
    # call the baseclass constructor
    super(SimplexNoiseManipulator, self).__init__(scene, **options)
  
  # def mousePressEvent(self, event):
  #   if super(SimplexNoiseManipulator, self).mousePressEvent(event):
  #     return True
    
  #   if event['mouseButton'] == QtCore.Qt.MouseButton.LeftButton:
  #     self.__moveStartCenter = self.__simplexNoiseImage.getParameter('center').getValue()
  #     self.__moveStartCol = event['mousePos'].x
  #     self.__moveStartRow = event['mousePos'].y
      
  #     return True
  
  # def mouseMoveEvent(self, event):
  #   if super(SimplexNoiseManipulator, self).mouseMoveEvent(event):
  #     return True
    
  #   if self.__moveStartCenter is not None:
  #     col = event['mousePos'].x
  #     row = event['mousePos'].y
      
  #     viewport = event['viewport']
  #     cols = viewport.getWidth()
  #     rows = viewport.getHeight()
      
  #     width = 4.0 / self.__simplexNoiseImage.getParameter('zoom').getValue()
  #     height = width / float(cols) * float(rows)
      
  #     moveEndCenter = Complex64(
  #       self.__moveStartCenter.re - float(col-self.__moveStartCol) / float(cols - 1) * width,
  #       self.__moveStartCenter.im - float(row-self.__moveStartRow) / float(rows - 1) * height
  #       )
  #     #print "moveEndCenter = " + str(moveEndCenter)
      
  #     self.__simplexNoiseImage.getParameter('center').setValue(moveEndCenter)
  #     event['viewport'].update()
      
  #     return True
  
  # def mouseReleaseEvent(self, event):
  #   if super(SimplexNoiseManipulator, self).mouseMoveEvent(event):
  #     return True
    
  #   if event['mouseButton'] == QtCore.Qt.MouseButton.LeftButton:
  #     self.__moveStartCenter = None
      
  #     return True
  
  def wheelEvent(self, event):
    if super(SimplexNoiseManipulator, self).wheelEvent(event):
      return True
    
    oldZoom = self.__simplexNoiseImage.getParameter('scale').getValue()

    # inverting the mouse behavior with minus event['wheelDelta']
    newZoom = oldZoom * pow(1.001, -event['wheelDelta'])

    if newZoom < 1e-5:
      newZoom = 1e-5
    if newZoom > 1e10:
      newZoom = 1e10
    self.__simplexNoiseImage.getParameter('scale').setValue(newZoom)
    event['viewport'].update()
    return True
  
class SimplexNoiseImage(BaseImage):
  
  def __init__(self, scene, resolution=256, scale=1.0, color = RGBA(0.0, 0.0, 0.0, 0.0), **kwargs):

    super(SimplexNoiseImage, self).__init__(scene, format = 'RGB', **kwargs)

    format = self.getFormat()
    dgnode = self.getDGNode()
    dgnode.addMember('resolution', 'UInt32', resolution)
    dgnode.addMember('scale', 'Float32', scale)
    dgnode.addMember('color', 'RGBA', color)
    self.addMemberParameter(dgnode, 'resolution', True)
    self.addMemberParameter(dgnode, 'scale', True)

    self.bindDGOperator(dgnode.bindings,
      name = 'computePixels', 
      fileName = FabricEngine.SceneGraph.buildAbsolutePath('SimplexNoise.kl'),
      layout = [
        'self.resolution',
        'self.scale',
        'self.image'
      ]
    )


class SimplexNoiseApp(SceneGraphApplication):
  
  def __init__(self, size=QSize(640,640)):

    super(SimplexNoiseApp, self).__init__()

    self.resize(size)

    self.setWindowTitle("Simplex Noise Viewer")
    
    self.setupViewports()
    
    scene = self.getScene()
    viewport = self.getViewport()
    
    simplexNoiseImage = SimplexNoiseImage(
      scene,
      resolution=size.width(),
      scale=1.0
    )

    viewport.getInPort('backgroundImage').setConnectedNode(simplexNoiseImage)

    manipulator = SimplexNoiseManipulator(scene, simplexNoiseImage)
        
    #self.addDockWidget(QtCore.Qt.RightDockWidgetArea, SGNodeInspectorDockWidget( node = simplexNoiseImage ))
    
    def resizeCallback(event):
      simplexNoiseImage.getParameter('resolution').setValue(event['width'])
      viewport.update()
    viewport.addEventListener('resize', resizeCallback)
    
    # open application
    self.constructionCompleted()

  def getStartupText(self):
    return "A simple SimplexNoise viewer.\nUse the scroll wheel to zoom in and out!"
    super(SimplexNoiseApp, self).getStartupText()

if __name__ == '__main__':
  app = SimplexNoiseApp()
  app.exec_()
