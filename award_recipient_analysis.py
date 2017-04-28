import pandas as pd
import numpy as np
import json

def transition(value, maximum, start_point, end_point):
  return start_point + (end_point - start_point)*value/maximum

def transition3(value, maximum, start_triplet, end_triplet):
  s1, s2, s3 = start_triplet
  e1, e2, e3 = end_triplet
  r1= transition(value, maximum, s1, e1)
  r2= transition(value, maximum, s2, e2)
  r3= transition(value, maximum, s3, e3)
  return (r1, r2, r3)

def rgb_to_hsv(r, g, b):
  maxc= max(r, g, b)
  minc= min(r, g, b)
  v= maxc
  if minc == maxc:
    return (0, 0, v)
  diff= maxc - minc
  s= diff / maxc
  rc= (maxc - r) / diff
  gc= (maxc - g) / diff
  bc= (maxc - b) / diff
  if r == maxc:
    h= bc - gc
  elif g == maxc:
    h= 2.0 + rc - bc
  else:
      h = 4.0 + gc - rc
  h = (h / 6.0) % 1.0 #comment: this calculates only the fractional part of h/6
  return (h, s, v)

def hsv_to_rgb(hsv):
  h, s, v = hsv
  if s == 0.0: return (int(v), int(v), int(v))
  i= int(np.floor(h*6.0)) #comment: floor() should drop the fractional part
  f= (h*6.0) - i
  p= v*(1.0 - s)
  q= v*(1.0 - s*f)
  t= v*(1.0 - s*(1.0 - f))
  if i%6 == 0: return (int(v), int(t), int(p))
  if i == 1: return (int(q), int(v), int(p))
  if i == 2: return (int(p), int(v), int(t))
  if i == 3: return (int(p), int(q), int(v))
  if i == 4: return (int(t), int(p), int(v))
  if i == 5: return (int(v), int(p), int(q))
  #comment: 0 <= i <= 6, so we never come here

awards = pd.read_json('awards.json')

# The goal is to count the contractors that any two agencies have in common,
# First, determine the size of the matrix
vendors = list(set(awards['recipient.recipient_name']))
num_vendors = len(vendors)
toptier_agencies = list(set(awards['awarding_agency.toptier_agency.name']))
for k,agency in enumerate(toptier_agencies):
  if not isinstance(agency,str):
    if np.isnan(agency):
      toptier_agencies[k] = 'NA'
num_agencies = len(toptier_agencies)
start_triplet= rgb_to_hsv(0, 255, 0)
end_triplet= rgb_to_hsv(255, 0, 0)
maximum = 200

# Second, create the attributes list of objects
agency_objects = []
for k,agency in enumerate(toptier_agencies):
  rgb_triplet_to_display = hsv_to_rgb(transition3(k, num_agencies, start_triplet, end_triplet))
  color = '#%02x%02x%02x' % rgb_triplet_to_display
  agency_objects += [{'color':color,'name':agency}]

# Third, polulate matrix integers
toptier_agencies = np.array(toptier_agencies)
vendors = np.array(vendors)
ag_ven_matrix = [[0]*num_agencies for k in range(num_vendors)]
for k,agency in enumerate(awards['awarding_agency.toptier_agency.name']):
  ax = np.where( agency==toptier_agencies )[0]
  vx = np.where( awards['recipient.recipient_name'][k] == vendors)[0]
  if (len(ax)>0) & (len(vx)>0):
    ag_ven_matrix[vx[0]][ax[0]] +=1 # += 1 # if you want weighting on number of interactions

# Four, inner product of this matrix to get a square matrix
ag_ven_matrix = np.array(ag_ven_matrix)
agency_matrix = np.dot( np.transpose(ag_ven_matrix), ag_ven_matrix)

for k in range(num_agencies):
  agency_matrix[k][k] = 0
agency_matrix = agency_matrix / agency_matrix.max()

with open('agencies.json', 'w') as outfile:
    json.dump(agency_objects, outfile)

with open('matrix.json', 'w') as outfile:
    json.dump(agency_matrix.tolist(), outfile)

# return agency_objects, agency_matrix

# cities = 1x35 set of objects, each with this format:
# cities = [
#   {color:"#E41A1C",
#    latitude:"37.7244",
#    longitude:"-122.421",
#    name:"Excelsior",
#    population:"0.083884"
#    },
#   {}...]
#
# matrix = 35x35 of integers


# from collections import Counter
# import matplotlib.pyplot as plt
# recipient_names = Counter(awards['recipient.recipient_name']).keys()
# recipient_counts = Counter(awards['recipient.recipient_name']).values()
#
# plt.hist(list(recipient_counts),range(1,1000),log=True)
#
# obligation_names = Counter(awards['total_obligation']).keys()
# obligation_counts = Counter(awards['total_obligation']).values()
#
# plt.hist(list(awards['total_obligation']),range=(1,200000000),bins=50,log=True)
# plt.hist(list(awards['total_obligation']),range=(-200000000,-1),bins=50,log=True)
