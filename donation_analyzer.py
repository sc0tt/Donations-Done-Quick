from datetime import datetime, timedelta
from itertools import groupby
from db import Donation
import json

#interval = timedelta(minutes=30)
output = []

def get_key(d):
  # group by 30 minutes
  k = d.donation_date + timedelta(minutes=-(d.donation_date.minute % 30))
  return datetime(k.year, k.month, k.day, k.hour, k.minute, 0)

def seconds_since_epoch(dt):
  return (dt - datetime(1970,1,1)).total_seconds()

gdq_list = {
  "CGDQ '10": {"start": datetime(2010, 1, 1), "end": datetime(2010, 1, 4)},
  "AGDQ '11": {"start": datetime(2011, 1, 6), "end": datetime(2011, 1, 12)},
  "JRDQ '11": {"start": datetime(2011, 4, 7), "end": datetime(2011, 4, 11)},
  "SGDQ '11": {"start": datetime(2011, 8, 4), "end": datetime(2011, 8, 7)},
  "AGDQ '12": {"start": datetime(2012, 1, 4), "end": datetime(2012, 1, 10)},
  "SGDQ '12": {"start": datetime(2012, 5, 24), "end": datetime(2012, 5, 29)},
  "AGDQ '13": {"start": datetime(2013, 1, 6), "end": datetime(2013, 1, 13)},
  "SGDQ '13": {"start": datetime(2013, 7, 25), "end": datetime(2013, 7, 31)},
  "AGDQ '14": {"start": datetime(2014, 1, 5), "end": datetime(2014, 1, 12)},
  "SGDQ '14": {"start": datetime(2014, 6, 22), "end": datetime(2014, 6, 29)},
  "AGDQ '15": {"start": datetime(2015, 1, 4), "end": datetime(2015, 1, 11)},
  "SGDQ '15": {"start": datetime(2015, 7, 26), "end": datetime(2015, 8, 3)},
  "AGDQ '16": {"start": datetime(2016, 1, 3), "end": datetime(2016, 1, 11)},
}


for name, dates in gdq_list.items():
  section_data = []
  data = Donation.select().where(Donation.donation_date >= dates["start"], Donation.donation_date <= dates["end"]).order_by(Donation.donation_date).asc()

  event_length = (dates["end"] - dates["start"]).total_seconds()

  g = groupby(data, key=get_key)
  iter_count = 0
  for key, items in g:
    total = sum([d.donation_amount for d in list(items)])
    total = float(total)

    if iter_count > 0:
      total += section_data[-1][1]

    # Get percentage complete
    section = (key - dates["start"]).total_seconds()
    progress = (section / event_length) * 100

    section_data.append([progress, total])
    iter_count += 1
  output.append({"name": name, "data": sorted(section_data, key=lambda x: x[0])})

with open("data.json", "w") as out:
  json.dump(output, out)