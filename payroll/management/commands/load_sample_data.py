import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from datetime import date
from payroll.models import Role, Employee, Contract, ContractType
from PIL import Image, ImageDraw, ImageFont

class Command(BaseCommand):
    help = 'Pre-populates the database with sample employees, contracts, and workflow roles'

    def handle(self, *args, **options):
        self.stdout.write('Initializing database with PayUPS sample data...')

        # Ensure signatures folder exists in media
        sig_dir = os.path.join(settings.MEDIA_ROOT, 'signatures')
        os.makedirs(sig_dir, exist_ok=True)

        # 1. Define Users and Roles
        users_to_create = [
            {'username': 'ao', 'first_name': 'Ruby Ann Luz', 'last_name': 'Wadawad', 'role': Role.UNIT_AO},
            {'username': 'unithead', 'first_name': 'Isagani L.', 'last_name': 'Bagus', 'role': Role.UNIT_HEAD},
            {'username': 'sbo_officer', 'first_name': 'Arvin M.', 'last_name': 'De Los Santos', 'role': Role.SBO_STAFF},
            {'username': 'sbo_supervisor', 'first_name': 'Leah B.', 'last_name': 'Cenicio', 'role': Role.SBO_STAFF},
            {'username': 'sbo_director', 'first_name': 'Noreen P.', 'last_name': 'Escultura', 'role': Role.SBO_STAFF},
            {'username': 'receiving', 'first_name': 'Dia-Lyn G.', 'last_name': 'Baluyut', 'role': Role.SAO_RECEIVING},
            {'username': 'preaudit', 'first_name': 'Melissa B.', 'last_name': 'Beldia', 'role': Role.SAO_PREAUDIT},
            {'username': 'payrollsup', 'first_name': 'Shirley M.', 'last_name': 'Cabrera', 'role': Role.SAO_PAYROLLSUP},
            {'username': 'cashmoni', 'first_name': 'Antonio R.', 'last_name': 'Ramilo', 'role': Role.SAO_CASHMONI},
            {'username': 'director', 'first_name': 'Ronnie B.', 'last_name': 'Pagal', 'role': Role.SAO_DIRECTOR},
            {'username': 'vp', 'first_name': 'Augustus C.', 'last_name': 'Resurreccion', 'role': Role.OVPA_VP},
            {'username': 'sco', 'first_name': 'Clenia S.', 'last_name': 'Delos Santos', 'role': Role.SCO_STAFF},
        ]

        for udata in users_to_create:
            user, created = User.objects.get_or_create(
                username=udata['username'],
                defaults={
                    'first_name': udata['first_name'],
                    'last_name': udata['last_name'],
                    'email': f"{udata['username']}@up.edu.ph"
                }
            )
            if created:
                user.set_password('password123')
                user.save()

            # Ensure profile has correct role
            profile = user.profile
            profile.role = udata['role']
            profile.unit_code = 'SPMO-S'

            # Generate elegant signature PNG programmatically using Pillow
            sig_filename = f"{udata['username']}_sig.png"
            sig_filepath = os.path.join(sig_dir, sig_filename)
            
            # Simple signature generation (transparent background, cursive-looking text)
            img = Image.new('RGBA', (200, 80), (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            
            # Add simple brush strokes mimicking a manual signature
            name_text = f"{udata['first_name']} {udata['last_name']}"
            draw.text((10, 25), name_text, fill=(12, 35, 100, 200)) # Dark blue signature
            # Draw a underline flourish
            draw.line([(10, 55), (180, 50), (190, 52)], fill=(12, 35, 100, 200), width=2)
            
            img.save(sig_filepath)
            profile.signature = f"signatures/{sig_filename}"
            profile.save()

            self.stdout.write(f"  Created user: {user.username} with role {profile.get_role_display()}")

        # 2. Define Employees
        employees_data = [
            {'name': 'BASA, AARON CHRISTIAN JUGAO', 'tin': '276-673-464', 'bank_name': 'LBP', 'account_number': '1234-5678-90'},
            {'name': 'CURA, SHERWIN RAFALLO', 'tin': 'NA', 'bank_name': 'LBP', 'account_number': '2345-6789-01'},
            {'name': 'DELA CRUZ, JULIUS MAR LIWAG', 'tin': 'NA', 'bank_name': 'LBP', 'account_number': '3456-7890-12'},
            {'name': 'DEL MUNDO, JOEVEN EXEQUIEL VAZQUEZ', 'tin': 'NA', 'bank_name': 'LBP', 'account_number': '4567-8901-23'},
            {'name': 'SARDUAL, ELDEFONSO TANO JR.', 'tin': 'NA', 'bank_name': 'LBP', 'account_number': '5678-9012-34'},
            {'name': 'WADAWAD, RUBY ANN LUZ COPETE', 'tin': 'NA', 'bank_name': 'LBP', 'account_number': '6789-0123-45'},
        ]

        for edata in employees_data:
            emp, created = Employee.objects.get_or_create(
                name=edata['name'],
                defaults={
                    'tin': edata['tin'],
                    'bank_name': edata['bank_name'],
                    'account_number': edata['account_number'],
                    'unit': 'SPMO-S'
                }
            )
            self.stdout.write(f"  Employee: {emp.name}")

            # 3. Create Contract for the employee (July - Dec 2026)
            # To show variety, we make some Daily Rate and some Monthly Rate
            rate_type = ContractType.MONTHLY
            monthly_rate = 0.00
            
            if 'BASA' in emp.name:
                rate_type = ContractType.DAILY
                monthly_rate = 61564.80 # daily rate will auto-calculate to 61564.80 / 22 = 2798.40
            elif 'CURA' in emp.name:
                monthly_rate = 36028.80
            elif 'DELA CRUZ' in emp.name:
                monthly_rate = 59997.70
            elif 'DEL MUNDO' in emp.name:
                monthly_rate = 44428.80
            else:
                monthly_rate = 44428.80

            Contract.objects.get_or_create(
                employee=emp,
                start_date=date(2026, 7, 1),
                end_date=date(2026, 12, 31),
                defaults={
                    'designation': 'Non-UP Contractual' if 'BASA' not in emp.name else 'COS IT Specialist',
                    'rate_type': rate_type,
                    'monthly_rate': monthly_rate,
                    'is_active': True
                }
            )
            self.stdout.write(f"    Loaded Contract type: {rate_type} for {emp.name}")

        self.stdout.write(self.style.SUCCESS('Successfully initialized PayUPS sample database!'))
