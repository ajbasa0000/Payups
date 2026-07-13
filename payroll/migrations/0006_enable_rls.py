from django.db import migrations

def enable_rls(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        tables = [
            "django_migrations",
            "django_content_type",
            "auth_permission",
            "auth_group",
            "auth_group_permissions",
            "auth_user_groups",
            "auth_user_user_permissions",
            "django_admin_log",
            "auth_user",
            "payroll_disbursementvoucher",
            "payroll_obligationrequest",
            "payroll_dvpayeedetail",
            "payroll_workflowlog",
            "payroll_userprofile",
            "payroll_generalpayroll",
            "payroll_generalpayrollitem",
            "payroll_contract",
            "payroll_employee",
            "django_session",
        ]
        with schema_editor.connection.cursor() as cursor:
            for table in tables:
                cursor.execute(f'ALTER TABLE IF EXISTS "{table}" ENABLE ROW LEVEL SECURITY;')

def disable_rls(apps, schema_editor):
    if schema_editor.connection.vendor == 'postgresql':
        tables = [
            "django_migrations",
            "django_content_type",
            "auth_permission",
            "auth_group",
            "auth_group_permissions",
            "auth_user_groups",
            "auth_user_user_permissions",
            "django_admin_log",
            "auth_user",
            "payroll_disbursementvoucher",
            "payroll_obligationrequest",
            "payroll_dvpayeedetail",
            "payroll_workflowlog",
            "payroll_userprofile",
            "payroll_generalpayroll",
            "payroll_generalpayrollitem",
            "payroll_contract",
            "payroll_employee",
            "django_session",
        ]
        with schema_editor.connection.cursor() as cursor:
            for table in tables:
                cursor.execute(f'ALTER TABLE IF EXISTS "{table}" DISABLE ROW LEVEL SECURITY;')

class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0005_contract_duties_contract_funding_source_and_more'),
    ]

    operations = [
        migrations.RunPython(enable_rls, reverse_code=disable_rls),
    ]
