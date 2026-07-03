from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('transactions/', views.transactions_list, name='transactions_list'),
    path('switch-role/', views.switch_role, name='switch_role'),
    path('transaction/create/', views.create_obr_dv, name='create_obr_dv'),
    path('obr/<int:pk>/', views.obr_view, name='obr_view'),
    path('dv/<int:pk>/', views.dv_view, name='dv_view'),
    path('obr/<int:pk>/approve/', views.approve_obr, name='approve_obr'),
    path('dv/<int:pk>/approve/', views.approve_dv, name='approve_dv'),
    path('dv-payee/<int:pk>/verify/', views.verify_contract, name='verify_contract'),
    path('contracts/', views.contracts_list, name='contracts_list'),
    path('employees/', views.employees_list, name='employees_list'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    path('general-payroll/list/', views.general_payroll_list, name='general_payroll_list'),
    path('general-payroll/create/', views.general_payroll_create, name='general_payroll_create'),
    path('general-payroll/<int:pk>/', views.general_payroll_detail, name='general_payroll_detail'),
    path('memos/', views.memos_viewer, name='memos_viewer'),
    path('contracts/<int:employee_id>/generate/', views.generate_contract_docx, name='generate_contract_docx'),
]
