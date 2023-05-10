# Load the Python Standard and DesignScript Libraries
import clr
#Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk.Revit.DB as DB
import math

# The inputs to this node will be stored as a list in the IN variables.
grids = UnwrapElement(IN[0])
reverse_horizontal = IN[1]
reverse_vertical = IN[2]

# Separate gridlines by orientation
def separate_by_orientation(grids):
    h_grids = []
    v_grids = []
    for grid in grids:
        if isinstance(grid, DB.Grid) and not grid.IsCurved:
            vector = grid.Curve.GetEndPoint(0) - grid.Curve.GetEndPoint(1)
            angle = vector.AngleTo(DB.XYZ.BasisY) * (180/math.pi)
            if (45 <= angle <= 135) or (225 <= angle <= 315):
                h_grids.append(grid)
            else:
                v_grids.append(grid)
    return {
        "horizontal_grids": sorted(h_grids, key=lambda x: x.Curve.GetEndPoint(0).Y, reverse=reverse_horizontal),
        "vertical_grids": sorted(v_grids, key=lambda x: x.Curve.GetEndPoint(0).X, reverse=reverse_vertical)}
        
OUT = separate_by_orientation(grids)["vertical_grids"], separate_by_orientation(grids)["horizontal_grids"]