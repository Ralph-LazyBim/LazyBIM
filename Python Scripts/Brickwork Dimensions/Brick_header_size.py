# Load the Python Standard and DesignScript Libraries
import clr
clr.AddReference('ProtoGeometry')
clr.AddReference('RevitServices')
import RevitServices
import math
from Autodesk.DesignScript.Geometry import *
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument

# The inputs to this node will be stored as a list in the IN variables.
dimlines = UnwrapElement(IN[0])
# Variables
brickheaderM = 102.5
jointM = 10
ftmmconversion = 304.8
brickwork_headersize = brickheaderM + jointM
brick_text = []

# Methods
def round_off_rating(number):
    return round(number * 2) / 2

def headersize_form(dim, brickheaderM, jointM):
  value_mm = round_off_rating(dim.Value * ftmmconversion)
  header_count = int(round(value_mm / (brickwork_headersize)))
  total_size_headers = (brickwork_headersize * header_count)
  additional_measurement = (value_mm - total_size_headers)
  total_headers = str(int(round(value_mm / (brickwork_headersize))))
    
  if value_mm % brickwork_headersize == jointM:
    result = total_headers + "B+J"
  elif value_mm % brickwork_headersize == brickheaderM:
    result = total_headers + "B-J"
  elif value_mm % brickwork_headersize == 0:
    result = total_headers + "B"
  elif value_mm % brickwork_headersize >= (brickwork_headersize / 2):
    result = str(int(math.ceil(value_mm / brickwork_headersize))) + "B " + str(additional_measurement) + "R" 
  else:
    result = str(int(value_mm // brickwork_headersize)) + "B+" + str(additional_measurement) + "R"
        
  dim.Below = result
  return result
    
TransactionManager.Instance.EnsureInTransaction(doc)
for dims in dimlines:
  if dims.Value == None:
    form = []
    for dim in dims.Segments:
      form.append(headersize_form(dim, brickheaderM, jointM))
    brick_text.append(form)
  else:
    form = []
    form.append(headersize_form(dims, brickheaderM, jointM))
    brick_text.append(form)
TransactionManager.Instance.TransactionTaskDone()

# Assign your output to the OUT variable
OUT = brick_text