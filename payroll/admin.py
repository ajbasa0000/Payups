from django.contrib import admin
from .models import (
    UserProfile, Employee, Contract, ObligationRequest, DisbursementVoucher,
    DVPayeeDetail, WorkflowLog, GeneralPayroll, GeneralPayrollItem, OnboardingMemo
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'unit_code', 'department')
    list_filter = ('role', 'department')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'tin', 'bank_name', 'account_number', 'department', 'unit')
    list_filter = ('department', 'bank_name')
    search_fields = ('name', 'tin', 'email')

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('employee', 'rate_type', 'monthly_rate', 'daily_rate', 'start_date', 'end_date', 'is_active')
    list_filter = ('rate_type', 'is_active')
    search_fields = ('employee__name', 'designation')

@admin.register(ObligationRequest)
class ObligationRequestAdmin(admin.ModelAdmin):
    list_display = ('obr_number', 'transaction_date', 'status', 'total_amount', 'created_by')
    list_filter = ('status',)
    search_fields = ('obr_number',)

@admin.register(DisbursementVoucher)
class DisbursementVoucherAdmin(admin.ModelAdmin):
    list_display = ('dv_number', 'transaction_date', 'status', 'total_amount', 'created_by', 'general_payroll')
    list_filter = ('status',)
    search_fields = ('dv_number',)

@admin.register(DVPayeeDetail)
class DVPayeeDetailAdmin(admin.ModelAdmin):
    list_display = ('dv', 'employee', 'gross_amount', 'withholding_tax', 'net_amount', 'is_contract_verified')
    list_filter = ('is_contract_verified',)
    search_fields = ('employee__name', 'dv__dv_number')

@admin.register(WorkflowLog)
class WorkflowLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'dv', 'obr', 'status_from', 'status_to', 'changed_by', 'changed_at')
    list_filter = ('status_to', 'changed_at')

@admin.register(GeneralPayroll)
class GeneralPayrollAdmin(admin.ModelAdmin):
    list_display = ('payroll_name', 'department', 'fund', 'bank', 'period_start', 'period_end', 'status')
    list_filter = ('department', 'status')
    search_fields = ('payroll_name',)

@admin.register(GeneralPayrollItem)
class GeneralPayrollItemAdmin(admin.ModelAdmin):
    list_display = ('general_payroll', 'employee', 'salary_basis', 'no_of_days', 'gross_salary', 'net_salary')
    search_fields = ('employee__name',)

@admin.register(OnboardingMemo)
class OnboardingMemoAdmin(admin.ModelAdmin):
    list_display = ('memo_number', 'title', 'uploaded_at')
    search_fields = ('memo_number', 'title')
