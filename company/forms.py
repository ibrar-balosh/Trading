from django import forms
from company.models import Company, CompanyLedger


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            'name', 'contact_person', 'cnic',
            'mobile', 'alternate_mobile', 'city'
        ]


class CompanyLedgerForm(forms.ModelForm):
    debit_amount = forms.DecimalField(required=False)
    credit_amount = forms.DecimalField(required=False)
    
    class Meta:
        model = CompanyLedger
        fields = [
            'debit_amount', 'credit_amount', 
            'date', 'details'
        ]
