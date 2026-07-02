import csv
import os
import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payroll.models import Department, Role, Employee, Contract, ContractType

class Command(BaseCommand):
    help = 'Imports the COS Masterlist CSV and creates department users'

    def handle(self, *args, **options):
        csv_path = r"C:\Users\ajbas\Downloads\HR Masterlist as of JUNE 2026 - COS APRIL 2026.csv"
        
        if not os.path.exists(csv_path):
            self.stdout.write(self.style.ERROR(f"CSV file not found at: {csv_path}"))
            return

        self.stdout.write("Creating department users (Unit AOs and Unit Heads)...")
        # 1. Create AO and Head users for all 35 departments
        for dept in Department.choices:
            dept_code = dept[0].lower()
            dept_name = dept[1]

            # Create Unit AO
            ao_username = f"ao_{dept_code}"
            ao_user, created = User.objects.get_or_create(
                username=ao_username,
                defaults={
                    'first_name': f"AO {dept[0]}",
                    'last_name': "Staff",
                    'email': f"{ao_username}@up.edu.ph"
                }
            )
            if created or not ao_user.has_usable_password():
                ao_user.set_password('password123')
                ao_user.save()
            
            ao_profile = ao_user.profile
            ao_profile.role = Role.UNIT_AO
            ao_profile.department = dept[0]
            ao_profile.unit_code = dept[0]
            ao_profile.save()

            # Create Unit Head
            head_username = f"head_{dept_code}"
            head_user, created = User.objects.get_or_create(
                username=head_username,
                defaults={
                    'first_name': f"Head {dept[0]}",
                    'last_name': "Supervisor",
                    'email': f"{head_username}@up.edu.ph"
                }
            )
            if created or not head_user.has_usable_password():
                head_user.set_password('password123')
                head_user.save()

            head_profile = head_user.profile
            head_profile.role = Role.UNIT_HEAD
            head_profile.department = dept[0]
            head_profile.unit_code = dept[0]
            head_profile.save()

        self.stdout.write(self.style.SUCCESS("All department users created successfully!"))

        self.stdout.write("Parsing and importing COS Masterlist...")
        
        # Mapper for unitcode in CSV to Department choices
        dept_mapper = {
            'CIDS': Department.CIDS,
            'UPS CIDS': Department.CIDS,
            'CWGS': Department.CWGS,
            'CIFAL': Department.CIFAL,
            'COA': Department.COA,
            'SHRDO-COA': Department.COA,
            'ITDC': Department.ITDC,
            'UP ITDC': Department.ITDC,
            'MPRO': Department.MPRO,
            'MCO': Department.MPRO,
            'OVPDX': Department.OVPDX,
            'OVPDx': Department.OVPDX,
            'OAD': Department.OAD,
            'OAR': Department.OAR,
            'ODPI': Department.ODPI,
            'OIL': Department.OIL,
            'OSR': Department.OSR,
            'OP': Department.OP,
            'OVPAA': Department.OVPAA,
            'OSDS': Department.OVPAA,
            'OVPA': Department.OVPA,
            'QMS': Department.OVPA_ISO,
            'OVPD': Department.OVPD,
            'TTBDO': Department.OVPD,
            'OVPLA': Department.OVPLA,
            'OVPPF': Department.OVPPF,
            'SBO': Department.OVPPF,
            'OVPRI': Department.OVPRI,
            'PADAYON': Department.PADAYON,
            'PGC': Department.PGC,
            'PMO': Department.PMO,
            'SAO': Department.SAO,
            'SCO': Department.SCO,
            'SHRDO': Department.SHRDO,
            'SPO': Department.SPO,
            'SPMO': Department.SSPMO,
            'TVUP': Department.TVUP,
            'BGC': Department.UPBGC,
            'ISC': Department.ISC,
            'KRC': Department.KRC,
            'UP PRESS': Department.PRESS,
            'UPRI': Department.UPRI,
            'UNP': Department.PAHINUNGOD,
        }

        # Clear existing employees and contracts to avoid duplicate confusion
        Employee.objects.all().delete()
        Contract.objects.all().delete()

        with open(csv_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                fullname = row.get('Full Name', '').strip()
                if not fullname:
                    continue

                tin = row.get('person_tin', '').strip()
                email = row.get('upmail', '').strip()
                csv_unitcode = row.get('unitcode', '').strip()
                
                # Resolve department
                dept_val = dept_mapper.get(csv_unitcode, Department.OP)
                
                # Create Employee
                employee = Employee.objects.create(
                    name=fullname,
                    tin=tin,
                    email=email,
                    department=dept_val,
                    unit=csv_unitcode or 'UP System'
                )

                # Create a sample contract matching their SG in the CSV
                sg_str = row.get('salarygrade', '10').strip()
                try:
                    sg = int(sg_str)
                except ValueError:
                    sg = 10

                # Approximate a monthly rate based on SG (SG 10 ~ 23,000, SG 18 ~ 46,000 etc.)
                monthly_rate = 15000 + (sg * 1800)
                daily_rate = monthly_rate / 22

                # Alternate Daily and Monthly rate types for diversity in the test list
                rate_type = ContractType.MONTHLY if count % 2 == 0 else ContractType.DAILY

                Contract.objects.create(
                    employee=employee,
                    rate_type=rate_type,
                    monthly_rate=monthly_rate,
                    daily_rate=daily_rate,
                    is_active=True,
                    designation=row.get('designation_name', 'COS Staff'),
                    start_date=datetime.date(2026, 1, 1),
                    end_date=datetime.date(2026, 6, 30)
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully imported {count} employees and contracts!"))
