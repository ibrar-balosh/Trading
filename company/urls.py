from django.urls import path
from company.views import (
    AddCompany, CompanyList, UpdateCompany,
    CompanyLedgerListView, DebitCompanyLedger, CreditCompanyLedger
)

app_name = 'company'

urlpatterns = [
    path('add/', AddCompany.as_view(), name='add'),
    path('list/', CompanyList.as_view(), name='list'),
    path('<int:pk>/update/', UpdateCompany.as_view(), name='update'),

    path('<int:pk>/ledger/', CompanyLedgerListView.as_view(), name='ledger_list'),
    path('<int:pk>/ledger/debit/', DebitCompanyLedger.as_view(), name='ledger_debit'),
    path('<int:pk>/ledger/credit/', CreditCompanyLedger.as_view(), name='ledger_credit'),
]
