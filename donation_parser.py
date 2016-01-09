from bs4 import BeautifulSoup
import requests
from db import Donation
import datetime
import peewee

args = {"page": 1}

while True:
  print("Parsing page: %s" % args["page"])
  req = requests.get("https://gamesdonequick.com/tracker/donations/", params=args)

  if req.status_code != 200:
    print("Not found. Exiting...")
    break

  soup = BeautifulSoup(req.content, 'html.parser')
  table = soup.findAll("table", class_="table")

  rows = table[0].findAll("tr")[1:]

  for row in reversed(rows):
    td = row.findAll("td")
    donation_date = td[1].text.strip()
    donation_date = datetime.datetime.strptime(donation_date, "%m/%d/%Y %H:%M:%S +0000")
    donation_amount = float(td[2].text.strip()[1:].replace(",", ""))

    donation_url = td[2].find('a')["href"].rsplit("/", 1)[1]
    print("%s - %s - %s" % (donation_date, donation_amount, donation_url))
    try:
      Donation.create(donation_date=donation_date, donation_amount=donation_amount, donation_id=donation_url)
    except peewee.IntegrityError:
      exit("Duplicate donation found")

  args["page"] += 1
