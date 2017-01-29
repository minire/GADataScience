import requests
data = requests.get("http://apps.who.int/gho/athena/api/GHO/MDG_0000000026.json")
data = data.json()

print data.keys()

print

print "fact"
for row in data["fact"][:2]:

  for dim in row["Dim"]:
    row[dim["category"]] = dim["code"]
  del row["Dim"]

  for key in row["value"]:
    row["value." + key] = row["value"][key]
  del row["value"]

  print row
  print

print "dim"
for row in data["dimension"]:
  #print row["label"]
  for v in row["code"]:
    #print v["label"], v["display"]
    pass
