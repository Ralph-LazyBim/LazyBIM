# Load the Python Standard and DesignScript Libraries
import clr
# Import DocumentManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

#Import RevitAPI
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

# The inputs to this node will be stored as a list in the IN variables.
vertical_grids = UnwrapElement(IN[0])
horizontal_grids = UnwrapElement(IN[1])
vertical_grid_labels = IN[2]
horizontal_grid_labels = IN[3]
prefix = IN[4]
prefix_toggle = IN[5]

# Renumber grids
def Renumber(vertical_grids, horizontal_grids, vertical_grid_labels, horizontal_grid_labels, prefix, prefix_toggle):
    doc = DocumentManager.Instance.CurrentDBDocument
    with Transaction(doc) as t:
        t.Start("Refresh Grid labels")
        for i, grid in enumerate(vertical_grids):
            if i < len(vertical_grid_labels):
                if prefix_toggle:
                    grid.Name = "N/A-" + prefix + str(vertical_grid_labels[i])
                else:
                    grid.Name = "N/A-" + str(vertical_grid_labels[i])
        for i, grid in enumerate(horizontal_grids):
            if i < len(horizontal_grid_labels):
                if prefix_toggle:
                    grid.Name = "N/A-" + prefix + str(horizontal_grid_labels[i])
                else:
                    grid.Name = "N/A-" + str(horizontal_grid_labels[i])
        t.Commit()
    with Transaction(doc) as t:
        t.Start("Renumbering Grids")
        for i, grid in enumerate(vertical_grids):
            if i < len(vertical_grid_labels):            
                if prefix_toggle:
                    grid.Name = prefix + str(vertical_grid_labels[i])
                else:
                    grid.Name = str(vertical_grid_labels[i])
        for i, grid in enumerate(horizontal_grids):
            if i < len(horizontal_grid_labels):            
                if prefix_toggle:
                    grid.Name = prefix + str(horizontal_grid_labels[i])
                else:
                    grid.Name = str(horizontal_grid_labels[i])
        t.Commit()
    return {
    "vertical grids": vertical_grids, "horizontal grids" : horizontal_grids}
    
OUT = Renumber(vertical_grids, horizontal_grids, vertical_grid_labels, horizontal_grid_labels, prefix, prefix_toggle)