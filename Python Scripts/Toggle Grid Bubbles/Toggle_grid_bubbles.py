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
getfirstview = views[0]
annotationelements = list()

TransactionManager.Instance.EnsureInTransaction(doc)

# Variables
collgrids = FilteredElementCollector(doc, getfirstview.Id)
filtgrids = ElementCategoryFilter(BuiltInCategory.OST_Grids)
grids = collgrids.WherePasses(filtgrids).ToElements()
firstgrid = grids[0]

# Check if first grid is turned on/off.
x = firstgrid.IsBubbleVisibleInView(DatumEnds.End0, getfirstview)

# Gather all grids per view.
for view in views:
  collector = FilteredElementCollector(doc, view.Id)
  filter = ElementCategoryFilter(BuiltInCategory.OST_Grids)
  grids = collector.WherePasses(filter).ToElements()
  
  if x == True:
    for grid in grids:
      grid.HideBubbleInView(DatumEnds.End0, view)
      grid.HideBubbleInView(DatumEnds.End1, view)
      out = "Bubbles are Hidden"
  else:
    for grid in grids:
      grid.ShowBubbleInView(DatumEnds.End0, view)
      grid.ShowBubbleInView(DatumEnds.End1, view)
      out = "Bubbles are Shown"
      
  annotationelements.append(grids)

TransactionManager.Instance.TransactionTaskDone()
doc.Regenerate()
uidoc.RefreshActiveView()
# Assign your output to the OUT variable
OUT = (annotationelements, out)