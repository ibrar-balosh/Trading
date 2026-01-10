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
    class Meta:
        model = CompanyLedger
        fields = '__all__'
