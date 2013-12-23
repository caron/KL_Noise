
#
# Copyright 2010-2012 Fabric Technologies Inc. All rights reserved.
#

from FabricEngine.SceneGraph.Nodes.Rendering import *
from FabricEngine.SceneGraph.Nodes.Images import *
from FabricEngine.SceneGraph.PySide import *
  
class SimplexNoiseImage(BaseImage):
  
  def __init__(self, scene, resolution=256, color = RGBA(0.0, 0.0, 0.0, 0.0), **kwargs):

    super(SimplexNoiseImage, self).__init__(scene, format = 'RGB', **kwargs)

    format = self.getFormat()
    dgnode = self.getDGNode()
    dgnode.addMember('resolution', 'UInt32', resolution)
    dgnode.addMember('color', 'RGBA', color)
    self.addMemberParameter(dgnode, 'resolution', True)

    self.bindDGOperator(dgnode.bindings,
      name = 'computePixels', 
      fileName = FabricEngine.SceneGraph.buildAbsolutePath('SimplexNoise.kl'),
      layout = [
        'self.resolution',
        'self.image'
      ]
    )


class SimplexNoiseApp(SceneGraphApplication):
  
  def __init__(self):
    
    super(SimplexNoiseApp, self).__init__()

    self.setWindowTitle("Simplex Noise Viewer")
    
    self.setupViewports()
    
    scene = self.getScene()
    viewport = self.getViewport()
    
    simplexNoiseImage = SimplexNoiseImage(
      scene,
      resolution=640
    )

    viewport.getInPort('backgroundImage').setConnectedNode(simplexNoiseImage)
        
    self.addDockWidget(QtCore.Qt.RightDockWidgetArea, SGNodeInspectorDockWidget( node = simplexNoiseImage ))
    
    def resizeCallback(event):
      simplexNoiseImage.getParameter('resolution').setValue(event['width'])
      viewport.update()
    viewport.addEventListener('resize', resizeCallback)
    
    # open application
    self.constructionCompleted()

  def getStartupText(self):
    return "This sample shows a simple SimplexNoise set viewer implmented in Scene Graph."
    super(SimplexNoiseApp, self).getStartupText()

if __name__ == '__main__':
  app = SimplexNoiseApp()
  app.exec_()
