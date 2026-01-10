from django.views.generic import ListView, FormView, UpdateView
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from company.models import Company, CompanyLedger
from company.forms import CompanyForm, CompanyLedgerForm


class AddCompany(FormView):
    template_name = 'company/add_company.html'
    form_class = CompanyForm

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('company:list')


class CompanyList(ListView):
    model = Company
    template_name = 'company/company_list.html'
    paginate_by = 100
    ordering = '-id'

def get_queryset(self):
        queryset = Company.objects.all().order_by('-id')

        company_name = self.request.GET.get('company_name')
        company_cnic = self.request.GET.get('company_id')

        if company_name:
            queryset = queryset.filter(name__icontains=company_name)

        if company_cnic:
            queryset = queryset.filter(cnic__icontains=company_cnic)

        return queryset


class UpdateCompany(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company/update_company.html'

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('company:list'))


class CompanyLedgerListView(ListView):
    model = CompanyLedger
    template_name = 'company_ledger/ledger_list.html'

    def get_queryset(self):
        return CompanyLedger.objects.filter(
            company_id=self.kwargs.get('pk')
        ).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = Company.objects.get(id=self.kwargs.get('pk'))
        return context


class DebitCompanyLedger(FormView):
    template_name = 'company_ledger/debit.html'
    form_class = CompanyLedgerForm

    def form_valid(self, form):
        obj = form.save()
        return HttpResponseRedirect(
            reverse('company:ledger_list', kwargs={'pk': obj.company.id})
        )


class CreditCompanyLedger(DebitCompanyLedger):
    template_name = 'company_ledger/credit.html'
