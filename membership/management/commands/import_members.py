import csv
from datetime import datetime

from django.core.management.base import BaseCommand

from membership.models import Membership


class Command(BaseCommand):
    help = 'Import Existing Memberships from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('filepath', nargs='+', type=str, help="Path to csv file with member information")

    def handle(self, **options):
        filepath = options.get('filepath')[0]

        with open(filepath) as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                self.create_membership(row)

    def create_membership(self, member):
        m = Membership(
            title=member['TITLE'],
            first_name=member['FIRSTNAME'],
            initial=member['INITIAL'],
            last_name=member['LASTNAME'],
            agency=member['AGENCY'],
            address1=member['ADDRESS 1'],
            address2=member['ADDRESS 2'],
            city=member['CITY'],
            state=member['STATE'],
            zip_code=member['ZIP CODE'],
            telephone=member['TELEPHONE'],
            work_telephone=member['WORKPHONE'],
            email=member['Email Address'],
            member_type=member['TYPE'],
            billing_quarter=member['BILLING_QT'],
            dues_paid=self.convert_date(member['DUES_PAID']),
            digital_newsletter=True if member['E-Newsletter'] else False,
            print_newsletter=True if member['Newsletter'] == 'X' else False,
            create_date=self.convert_date(member['New member']),
            notes=member['NOTE']
        )
        m.save()

    def convert_date(self, date_stamp):
        if date_stamp.strip():
            return datetime.strptime(date_stamp.strip(), '%m/%d/%y').strftime('%Y-%m-%d')
