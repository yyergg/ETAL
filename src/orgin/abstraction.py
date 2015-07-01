class Abstraction:
  def __init__(self):
    self.reset()

  '''
  Set Layer Abstraction.
  Or you don't use this function to use the
  default situation.
  '''
  def setAbstractionLayer(self,layer):
    self.isSetLayer = True
    self.layer = layer


  '''
  Set Layout Abstraction.
  Notice that you only need to choose at most one method
  from the following four functions.
  Or you can choose none of these functions and using the
  default situation.
  '''
  def setConsiderLayoutOnly(self):
    self.LayoutAbstractionName = "ConsiderLayoutOnly"

  def setIgnoreListView(self):
    self.LayoutAbstractionName = "IgnoreListView"

  def setIgnoredClasses(self,ignoredList):
    self.LayoutAbstractionName = "IgnoredClasses"
    self.ignoredClassesList = ignoredList


  '''
  Set Attributes Abstraction.
  Notice that you only need to choose at most one method
  from the following three functions.
  Or you can choose none of these functions and using the
  default situation.
  '''
  def setConsideredAttrib(self,attribList):
    self.AttribAbstractionName = "Considered"
    self.consideredAttribList = attribList

  def setIgnoredAttrib(self,attribList):
    self.AttribAbstractionName = "Ignored"
    self.ignoredAttribList = attribList


  '''''
  End of settings.
  '''''


  def getViews(self,root,layer):
    returnList = []
    for child in root:
      returnList.append((child,layer))
      returnList.extend(self.getViews(child,layer+1))
    return returnList


  def compare(self,viewList1,viewList2):
    if len(viewList1) == 0 and len(viewList2) == 0:
            #print("both views are None")
            return True

    elif len(viewList1) == 0 or len(viewList2) == 0:
            #print("A view is None")
            return False

##    print("---------------------------------------------------")
##    print("before abstraction xml file 1:")
##    for (view1,view2) in zip(viewList1,viewList2):
##      print("class1 = "+ str(view1.getClass())+" layer = "+str(view1.getLayer())," \
##             class2 = "+ str(view2.getClass())+" layer = "+str(view2.getLayer()))
    '''
    start abstraction compare
    '''
    self.layerAbstraction(viewList1)
    self.layerAbstraction(viewList2)
##    print("---------------------------------------------------")
##    print("after layer abstraction xml file1:")
##    for (view1,view2) in zip(viewList1,viewList2):
##      print("class1 = "+ str(view1.getClass())+" layer = "+str(view1.getLayer())," \
##             class2 = "+ str(view2.getClass())+" layer = "+str(view2.getLayer()))

    self.layoutAbstraction(viewList1)
    self.layoutAbstraction(viewList2)
##    print("---------------------------------------------------")
##    print("after layout abstraction xml file1:")
##    for (view1,view2) in zip(viewList1,viewList2):
##      print("class1 = "+ str(view1.getClass())+" layer = "+str(view1.getLayer())," \
##             class2 = "+ str(view2.getClass())+" layer = "+str(view2.getLayer()))

    result = self.attribCompare(viewList1,viewList2)
##    print("---------------------------------------------------")
##    print("after attribute compare")
##    print("Two xml files are "+result)
    return self.result

  def layerAbstraction(self,viewList):
    # start layer abstraction
    if self.isSetLayer:
      for view in viewList[:]:
        if view.getLayer() > self.layer:
          viewList.remove(view)

  def layoutAbstraction(self,viewList):
    # start layout abstraction
    if self.LayoutAbstractionName == "None":
      None

    elif self.LayoutAbstractionName == "ConsiderLayoutOnly":
      frame = "android.widget.FrameLayout"
      linear = "android.widget.LinearLayout"
      relative = "android.widget.RelativeLayout"
      layout = [frame,linear,relative]
      # [:] is used to iterate and remove concurrently
      for view in viewList[:]:
        if view.getClass() not in layout:
          viewList.remove(view)

    elif self.LayoutAbstractionName == "IgnoreListView":
      isStartRemove = False
      listViewLayer = 100 # it's large enough
      for view in viewList[:]:
        # remove all nodes that appear right after ListView and
	# have larger layer
        if view.getClass() == "android.widget.ListView":
          isStartRemove = True
          listViewLayer = view.getLayer()
        elif isStartRemove and view.getLayer()>listViewLayer:
          viewList.remove(view)
        else:
          isStartRemove = False
          listViewLayer = 100

    elif self.LayoutAbstractionName == "IgnoredClasses":
      for view in viewList[:]:
        if view.getClass() in self.ignoredClassesList:
          viewList.remove(view)

  def attribCompare(self,viewList1,viewList2):
    # start attribute abstraction
    if len(viewList1) == 0 and len(viewList2) == 0:
        return "all None"

    elif len(viewList1) == 0 or len(viewList2) == 0:
        return "None of some one"

    if len(viewList1) != len(viewList2):
        self.result = False
        return "different by size"
    attributes = []

    if self.AttribAbstractionName == "None":
      None
    elif self.AttribAbstractionName == "Considered":
        attributes = self.consideredAttribList
    elif self.AttribAbstractionName == "Ignored":
      for attrib in viewList1[0].attrDict:
        attributes.append(attrib)
      for attrib in attributes[:]:
        if attrib in self.ignoredAttribList:
          attributes.remove(attrib)
##
##    print("---------------------------------------------------")
##    print("attributes need to be compared:")
##    print(attributes)

    for view1, view2 in zip(viewList1,viewList2):
      for attrib in attributes:
        if view1.attrDict[attrib] != view2.attrDict[attrib]:
            self.result = False
            return "different by attributes with view1 class = "+view1.getClass()+" "+str(attrib)+" = "+str(view1.attrDict[attrib])+\
                                               " view2 class = "+view2.getClass()+" "+str(attrib)+" = "+str(view2.attrDict[attrib])

    self.result = True
    return "the same"


  def reset(self):
    # Layer Abstraction settings
    self.layer = 0
    self.isSetLayer = False

    # Layout Abstraction settings
    self.LayoutAbstractionName = "None"
    self.ignoredClassesList = []

    # Attribute Abstraction settings
    self.AttribAbstractionName = "None"
    self.consideredAttribList = []
    self.ignoredAttribList = []

    self.result = False # the final answer to return

  def getConsideredAttributes(self):
    return self.consideredAttribList

  def getIgnoredAttributes(self):
    return self.ignoredAttribList

  def absSettingParse(self,taskSetting):
    absLayer = taskSetting["abstractionLayer"]
    absLayout = taskSetting["abstractionLayout"]
    absIgnoredClasses = taskSetting["absIgnoredClasses"]
    absAttrib = taskSetting["abstractionAttributes"]
    abs = [absLayer,absLayout,absIgnoredClasses,absAttrib]
    if absAttrib == "None":
        abs.append("None")
    elif absAttrib == "setConsideredAttrib":
        absConsideredAttrib = taskSetting["absConsideredAttrib"]
        abs.append(absConsideredAttrib)
    elif absAttrib == "setIgnoredAttrib":
        absIgnoredAttrib = taskSetting["absIgnoredAttrib"]
        abs.append(absIgnoredAttrib)

    return abs

  def setAbstraction(self,abs):
    ''''''''''''''''''''''''''''''''''''
    '''  set the abstraction details '''
    ''''''''''''''''''''''''''''''''''''
    # abs = [5, 'setIgnoreListView', 'None', 'setIgnoredAttrib', ['checkable', 'text']]
    absLayer = abs[0]
    absLayout = abs[1]
    absIgnoredClasses = abs[2]
    absAttrib = abs[3]
    absAttribList = abs[4]

    # 1. layer abstraction
    if absLayer <= 0 or absLayer == "None": # turn off layer abstraction
        pass
    else:
        self.setAbstractionLayer(absLayer)

    # 2. layout abstraction
    if absLayout == "None": # turn off layout abstraction
        pass
    elif absLayout == "setConsiderLayoutOnly":
        self.setConsiderLayoutOnly()
    elif absLayout == "setIgnoreListView":
        self.setIgnoreListView()
    elif absLayout == "setIgnoredClasses":
        if absIgnoredClasses != "None":
            self.setIgnoredClasses(absIgnoredClasses)

    # 3. attributes abstraction
    if absAttrib == "None": # turn off attributes abstraction
        pass
    elif absAttribList != "None":
        if absAttrib == "setConsideredAttrib":
            self.setConsideredAttrib(absAttribList)

        elif absAttrib == "setIgnoredAttrib":
            self.setIgnoredAttrib(absAttribList)


##
##  def absState(self,xmlPath):
##    # get the viewList
##    xml = ET.parse(xmlPath)
##    root = xml.getroot()
##    viewList = self.getViews(root,1)
##    print("-----------------------------------")
##    print("layer = "+str(self.layer))
##    for view in viewList:
##      print("class = "+ str(view[0].attrib["class"])+" layer = "+str(view[1]))
##    print("-----------------------------------")
##
##
##    self.layerAbstraction(viewList)
##    self.layoutAbstraction(viewList)
##    print("-----------------------------------")
##    for view in viewList:
##      print("class = "+ str(view[0].attrib["class"])+" layer = "+str(view[1]))
##    print("-----------------------------------")
##
##
##    from Automata import State,View
##    state = State()
##
##    for index,view in enumerate(viewList):
##        newView = View(view[0],view[1],index)
##        state.viewList.append(newView)
##
##    return state







