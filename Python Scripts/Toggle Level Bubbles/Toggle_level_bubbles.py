# Load the Python Standard and DesignScript Libraries
import clr
# Import DocumentManager
clr.AddReference("RevitServices")
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

#Import RevitAPI
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

# The inputs to this node will be stored as a list in the IN variables.
doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
views = UnwrapElement(IN[0])
leftbubbles = UnwrapElement(IN[1])
rightbubbles = UnwrapElement(IN[2])
annotationelements = list()

TransactionManager.Instance.EnsureInTransaction(doc)

# Gather all levels per view.
for view in views:
  collector = FilteredElementCollector(doc, view.Id)
  filter = ElementCategoryFilter(BuiltInCategory.OST_Levels)
  levels = collector.WherePasses(filter).ToElements()

  if leftbubbles == True:
    if rightbubbles == True:
      for level in levels:
        level.ShowBubbleInView(DatumEnds.End0, view)
        level.ShowBubbleInView(DatumEnds.End1, view)          
        out = "Bubbles on the left and Right are Shown"
    if rightbubbles == False:
      for level in levels:
        level.ShowBubbleInView(DatumEnds.End0, view)
        level.HideBubbleInView(DatumEnds.End1, view)
        out = "Bubbles on the left are Shown"
  elif rightbubbles == True and leftbubbles == False:
    for level in levels:
      level.ShowBubbleInView(DatumEnds.End1, view)
      level.HideBubbleInView(DatumEnds.End0, view)          
      out = "Bubbles on the right are Shown"
  else:
    for level in levels:
      level.HideBubbleInView(DatumEnds.End0, view)
      level.HideBubbleInView(DatumEnds.End1, view)
      out = "Bubbles are Hidden"              
  
  annotationelements.append(levels)

TransactionManager.Instance.TransactionTaskDone()
doc.Regenerate()
uidoc.RefreshActiveView()

# Assign your output to the OUT variable
OUT = (annotationelements, out)