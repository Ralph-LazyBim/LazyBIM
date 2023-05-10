import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

#Import DocumentManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

#Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk

#Import ToDSType(bool) extension method
clr.AddReference("RevitNodes")
import Revit
from Autodesk.Revit.DB import *
from Autodesk.Revit.Creation import *
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)

# The inputs to this node will be stored as a list in the IN variables.
doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
views = UnwrapElement(IN[0])
dimensionsperview = list()

TransactionManager.Instance.EnsureInTransaction(doc)

# Collect dimensions in Views
for v in views:
  dimensions = list()  
  colldimension = FilteredElementCollector(doc, v.Id)
  filtdimension = ElementCategoryFilter(BuiltInCategory.OST_Dimensions)
  dimensions = colldimension.WherePasses(filtdimension).ToElements()  
  dimensionsperview.append(dimensions)
  
TransactionManager.Instance.TransactionTaskDone()

doc.Regenerate()
uidoc.RefreshActiveView()

OUT = dimensionsperview