import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Department(models.TextChoices):
    CIDS = 'CIDS', 'Center For Integrative Development Studies (CIDS)'
    CWGS = 'CWGS', 'Center For Women And Gender Studies (CWGS)'
    CIFAL = 'CIFAL', 'Centre International de Formation des Autorités et Leaders (CIFAL)'
    COA = 'COA', 'Commission on Audit (COA-System)'
    ITDC = 'ITDC', 'Information Technology Development Center (ITDC)'
    MPRO = 'MPRO', 'Media and Public Relation (MPRO)'
    OVPDX = 'OVPDX', 'Office Of The Vice President For Digital Transformation (OVPDX)'
    OAD = 'OAD', 'Office of Admissions (OAD)'
    OAR = 'OAR', 'Office of Alumni Relations (OAR)'
    ODPI = 'ODPI', 'Office of Design and Planning Initiatives (ODPI)'
    OIL = 'OIL', 'Office of International Linkages (OIL)'
    OSR = 'OSR', 'Office of Sectoral Regents (OSR)'
    OP = 'OP', 'Office of the President (OP)'
    OVPAA = 'OVPAA', 'Office of the Vice President for Academic Affairs (OVPAA)'
    OVPA = 'OVPA', 'Office of the Vice President for Administration (OVPA)'
    OVPA_ISO = 'OVPA_ISO', 'Office of the Vice President for Administration (OVPA-ISO)'
    OVPD = 'OVPD', 'Office of the Vice President for Development (OVPD)'
    OVPLA = 'OVPLA', 'Office of the Vice President for Legal Affairs (OVPLA)'
    OVPPF = 'OVPPF', 'Office of the Vice President for Planning and Finance (OVPPF)'
    OVPRI = 'OVPRI', 'Office of the Vice President for Research and Innovation (OVPRI)'
    PADAYON = 'PADAYON', 'Padayon Public Service Office'
    PGC = 'PGC', 'Philippine Genome Center (PGC)'
    PMO = 'PMO', 'Project Management Office (PMO)'
    SAO = 'SAO', 'System Accounting Office (SAO)'
    SCO = 'SCO', 'System Cash Office (SCO)'
    SHRDO = 'SHRDO', 'System Human Resource Development Office (SHRDO)'
    SPO = 'SPO', 'System Procurement Office (SPO)'
    SSPMO = 'SSPMO', 'System Supply and Property Management Office (SSPMO)'
    TVUP = 'TVUP', 'TVUP (TVUP)'
    UPBGC = 'UPBGC', 'UP Bonifacio Global City Campus (UPBGC)'
    ISC = 'ISC', 'UP Intelligent Systems Center (ISC)'
    KRC = 'KRC', 'UP Korea Research Center (KRC)'
    PRESS = 'PRESS', 'UP Press'
    UPRI = 'UPRI', 'UP Resilience Institute (UPRI)'
    PAHINUNGOD = 'PAHINUNGOD', 'UP Ugnayan Ng Pahinungod Office'

class Role(models.TextChoices):
    UNIT_AO = 'UNIT_AO', 'Unit AO'
    UNIT_HEAD = 'UNIT_HEAD', 'Unit Head'
    SBO_STAFF = 'SBO_STAFF', 'SBO Staff (Budget)'
    SAO_RECEIVING = 'SAO_RECEIVING', 'SAO Receiving'
    SAO_PREAUDIT = 'SAO_PREAUDIT', 'SAO Pre-Audit'
    SAO_PAYROLLSUP = 'SAO_PAYROLLSUP', 'SAO Payroll Supervisor'
    SAO_CASHMONI = 'SAO_CASHMONI', 'SAO Cash Monitoring'
    SAO_DIRECTOR = 'SAO_DIRECTOR', 'SAO Director'
    OVPA_VP = 'OVPA_VP', 'VP OVPA'
    SCO_STAFF = 'SCO_STAFF', 'SCO Staff (Cash Office)'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.UNIT_AO)
    unit_code = models.CharField(max_length=20, default='SPMO-S')
    department = models.CharField(max_length=100, choices=Department.choices, default=Department.SSPMO)
    signature = models.ImageField(upload_to='signatures/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_role_display()})"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance)
    instance.profile.save()

class Employee(models.Model):
    name = models.CharField(max_length=150)
    tin = models.CharField(max_length=50, blank=True)
    bank_name = models.CharField(max_length=100, default='LBP')
    account_number = models.CharField(max_length=100, blank=True)
    unit = models.CharField(max_length=50, default='SPMO-S')
    department = models.CharField(max_length=100, choices=Department.choices, default=Department.SSPMO)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    govt_id = models.CharField(max_length=100, blank=True)
    govt_id_details = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.name

class ContractType(models.TextChoices):
    DAILY = 'DAILY', 'Daily Rate COS'
    MONTHLY = 'MONTHLY', 'Monthly Rate COS'

class Contract(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='contracts')
    designation = models.CharField(max_length=100, default='Non-UP Contractual')
    rate_type = models.CharField(max_length=10, choices=ContractType.choices, default=ContractType.MONTHLY)
    monthly_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    daily_rate = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    contract_file = models.FileField(upload_to='contracts/', blank=True, null=True)
    terms_of_reference = models.FileField(upload_to='contracts/tor/', blank=True, null=True)
    authority_to_hire = models.FileField(upload_to='contracts/ath/', blank=True, null=True)

    duties = models.TextField(blank=True, default="Perform general administrative functions.")
    funding_source = models.CharField(max_length=150, default='UPS SPMO MOOE')
    head_of_unit_name = models.CharField(max_length=150, default='ISAGANI L. BAGUS')
    head_of_unit_position = models.CharField(max_length=150, default='Acting Chief SSPMO')
    head_of_unit_id = models.CharField(max_length=100, default='NO4-03-000009')
    head_of_unit_id_details = models.CharField(max_length=150, default='June 8, 2022 / Quezon City')
    witness1_name = models.CharField(max_length=150, default='MARK JOSHUA M. PEDROSA')
    witness1_position = models.CharField(max_length=150, default='Administrative Assistant I')
    witness2_name = models.CharField(max_length=150, default='JULIUS MAR L. DELA CRUZ')
    witness2_position = models.CharField(max_length=150, default='Junior Office Manager')

    @property
    def is_viewable(self):
        # July 1, 2026 onwards contracts are viewable
        # June 30, 2026 backwards is not viewable
        limit_date = datetime.date(2026, 7, 1)
        return self.end_date >= limit_date

    def __str__(self):
        return f"Contract: {self.employee.name} - {self.designation} ({self.get_rate_type_display()})"

    def save(self, *args, **kwargs):
        # Per Memo No. ACR 26-100: Daily rate = Monthly rate / 22
        if self.rate_type == ContractType.DAILY and self.monthly_rate > 0 and self.daily_rate == 0:
            self.daily_rate = self.monthly_rate / 22
        elif self.rate_type == ContractType.MONTHLY and self.daily_rate > 0 and self.monthly_rate == 0:
            self.monthly_rate = self.daily_rate * 22
        super().save(*args, **kwargs)

class ObRStatus(models.TextChoices):
    DRAFTED = 'DRAFTED', 'Drafted'
    SUBMITTED = 'SUBMITTED', 'Created/Submitted'
    UNIT_HEAD_APPROVED = 'UNIT_HEAD_APPROVED', 'Approved by Unit Head'
    SBO_OFFICER_REVIEWED = 'SBO_OFFICER_REVIEWED', 'Reviewed by SBO Officer'
    SBO_SUPERVISOR_REVIEWED = 'SBO_SUPERVISOR_REVIEWED', 'Reviewed by SBO Supervisor'
    APPROVED = 'APPROVED', 'APPROVED'

class ObligationRequest(models.Model):
    obr_number = models.CharField(max_length=100, unique=True)
    transaction_date = models.DateField(auto_now_add=True)
    requesting_unit = models.CharField(max_length=100, default='SYSTEM SUPPLY AND PROPERTY MANAGEMENT OFFICE (SPMO-S)')
    expense_class = models.CharField(max_length=50, default='MOOE')
    fund_cluster = models.CharField(max_length=100, default='01 101101')
    bank = models.CharField(max_length=100, default='Land Bank of the Philippines')
    payment_option = models.CharField(max_length=50, default='ATM (ADA)')
    request_category = models.CharField(max_length=50, default='c/o Unit')
    status = models.CharField(max_length=30, choices=ObRStatus.choices, default=ObRStatus.DRAFTED)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_obrs')

    def __str__(self):
        return f"ObR: {self.obr_number} ({self.get_status_display()})"

class DVStatus(models.TextChoices):
    DRAFTED = 'DRAFTED', 'Drafted'
    WAITING_OBR = 'WAITING_OBR', 'Waiting for the Approval of ObR/BUR'
    UNIT_HEAD_APPROVED = 'UNIT_HEAD_APPROVED', 'Approved by Unit Head (Unit Head)'
    SAO_RECEIVED = 'SAO_RECEIVED', 'Received by SAO'
    SAO_PRE_AUDIT = 'SAO_PRE_AUDIT', 'Checked by SAO Pre-Audit Staff'
    SAO_SUPERVISOR = 'SAO_SUPERVISOR', 'Checked by SAO Supervisor'
    CASH_MONITORED = 'CASH_MONITORED', 'Released Cash Monitoring'
    SAO_DIRECTOR = 'SAO_DIRECTOR', 'Approved by SAO Director'
    APPROVED = 'APPROVED', 'APPROVED'
    RADA_DRAFT = 'RADA_DRAFT', 'DRAFT (RADA)'

class DisbursementVoucher(models.Model):
    dv_number = models.CharField(max_length=100, unique=True)
    transaction_date = models.DateField(auto_now_add=True)
    obr = models.ForeignKey(ObligationRequest, on_delete=models.SET_NULL, null=True, blank=True, related_name='dvs')
    requesting_unit = models.CharField(max_length=100, default='SYSTEM SUPPLY AND PROPERTY MANAGEMENT OFFICE (SPMO-S)')
    expense_class = models.CharField(max_length=50, default='MOOE')
    bank = models.CharField(max_length=100, default='Land Bank of the Philippines')
    payment_option = models.CharField(max_length=50, default='ATM (ADA)')
    request_category = models.CharField(max_length=50, default='c/o Unit')
    status = models.CharField(max_length=30, choices=DVStatus.choices, default=DVStatus.DRAFTED)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_dvs')
    
    general_payroll = models.ForeignKey('GeneralPayroll', on_delete=models.SET_NULL, null=True, blank=True, related_name='dvs')

    # Box E Payment info (added at step 10)
    check_ada_no = models.CharField(max_length=100, blank=True)
    payment_date = models.DateField(blank=True, null=True)
    payment_bank_account = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"DV: {self.dv_number} ({self.get_status_display()})"

class DVPayeeDetail(models.Model):
    dv = models.ForeignKey(DisbursementVoucher, on_delete=models.CASCADE, related_name='payee_details')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    particulars = models.TextField()
    gross_amount = models.DecimalField(max_digits=12, decimal_places=2)
    withholding_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # SBO / SAO Account codes matching BULSA sample
    account_to_debit = models.CharField(max_length=200, default='SA03010001 (GF) -- SPMO-SUPS Supply and Property Management Office (SPMO) - 106510A / SA03010001')
    expense_subclass = models.CharField(max_length=100, default='Regular MOOE/ Other General Services (Non-UP)')
    ppa = models.CharField(max_length=100, default='A.I.a - 100000100001000')

    # Pre-audit digital verification
    contract = models.ForeignKey(Contract, on_delete=models.SET_NULL, null=True, blank=True)
    is_contract_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_payees')
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.name} in {self.dv.dv_number}"

class WorkflowLog(models.Model):
    dv = models.ForeignKey(DisbursementVoucher, on_delete=models.CASCADE, null=True, blank=True, related_name='workflow_logs')
    obr = models.ForeignKey(ObligationRequest, on_delete=models.CASCADE, null=True, blank=True, related_name='workflow_logs')
    status_from = models.CharField(max_length=50, blank=True)
    status_to = models.CharField(max_length=50)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        target = self.dv.dv_number if self.dv else self.obr.obr_number
        return f"Log for {target}: -> {self.status_to} by {self.changed_by}"

class GeneralPayrollStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    SUBMITTED = 'SUBMITTED', 'Submitted'
    APPROVED = 'APPROVED', 'Approved'

class GeneralPayroll(models.Model):
    payroll_name = models.CharField(max_length=200, default='UP System ICS Payroll Semi Mo')
    department = models.CharField(max_length=100, choices=Department.choices, default=Department.SSPMO)
    fund = models.CharField(max_length=50, default='101')
    bank = models.CharField(max_length=50, default='LBP')
    period_start = models.DateField()
    period_end = models.DateField()
    status = models.CharField(max_length=20, choices=GeneralPayrollStatus.choices, default=GeneralPayrollStatus.DRAFT)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_payrolls')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payroll_name} ({self.get_department_display()}): {self.period_start} to {self.period_end}"

class GeneralPayrollItem(models.Model):
    general_payroll = models.ForeignKey(GeneralPayroll, on_delete=models.CASCADE, related_name='items')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary_basis = models.DecimalField(max_digits=12, decimal_places=2)
    no_of_days = models.DecimalField(max_digits=5, decimal_places=2, default=11.00)
    gross_salary = models.DecimalField(max_digits=12, decimal_places=2)
    philhealth_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    sss = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    nvat_3 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    ewt_5 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    ewt_10 = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Payroll item for {self.employee.name} in {self.general_payroll.id}"


class OnboardingMemo(models.Model):
    memo_number = models.CharField(max_length=100, unique=True, help_text="e.g. Memo No. ACR 26-100")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, help_text="A short summary of the memo's contents")
    file = models.FileField(upload_to='memos/', help_text="Upload the PDF document")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.memo_number} - {self.title}"

