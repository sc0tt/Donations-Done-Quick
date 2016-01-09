import peewee

db = peewee.SqliteDatabase('donations.db')

class Donation(peewee.Model):
   donation_date = peewee.DateTimeField()
   donation_amount = peewee.DecimalField()
   donation_id = peewee.IntegerField(unique=True)

   class Meta:
      database = db

if not Donation.table_exists():
   Donation.create_table()