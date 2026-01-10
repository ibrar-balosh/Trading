from django.db import models
from django.db.models import Sum
from django.utils import timezone
    
class Company(models.Model):
    name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200, blank=True, null=True)
    cnic = models.CharField(max_length=15, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    alternate_mobile = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.name


    def get_unpaid_amount(self):
        ledgers = self.company_ledger.all()
        debit = ledgers.aggregate(Sum('debit_amount'))['debit_amount__sum'] or 0
        credit = ledgers.aggregate(Sum('credit_amount'))['credit_amount__sum'] or 0
        return debit - credit


class CompanyLedger(models.Model):
    company = models.ForeignKey(
        Company, related_name='company_ledger', on_delete=models.CASCADE
    )
    debit_amount = models.DecimalField(max_digits=65, decimal_places=2, default=0)
    credit_amount = models.DecimalField(max_digits=65, decimal_places=2, default=0)
    details = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.company.name
