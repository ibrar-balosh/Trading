from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from company.models import Company, CompanyLedger
from company.forms import CompanyForm, CompanyLedgerForm
from django.contrib import messages

class AddCompany(CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company/add_company.html'
    success_url = reverse_lazy('company:list')

    def form_valid(self, form):
        messages.success(self.request, "Company added successfully")
        return super().form_valid(form)

    # def get_success_url(self):
    #     return reverse('company:list')


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
    success_url = reverse_lazy('company:list')

    # def form_valid(self, form):
    #     form.save()
    #     return HttpResponseRedirect(reverse('company:list'))


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


class DebitCompanyLedger(CreateView):
    template_name = 'company_ledger/debit.html'
    form_class = CompanyLedgerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = get_object_or_404(
            Company, id=self.kwargs['pk']
        )
        return context

    def form_valid(self, form):
        company = get_object_or_404(Company, id=self.kwargs['pk'])
        ledger = form.save(commit=False)
        ledger.company = company
        ledger.credit_amount = 0
        ledger.save()

        return HttpResponseRedirect(
            reverse_lazy('company:ledger_list', kwargs={'pk': company.id})
        )

class CreditCompanyLedger(CreateView):
    template_name = 'company_ledger/credit.html'
    form_class = CompanyLedgerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = get_object_or_404(
            Company, id=self.kwargs['pk']
        )
        return context

    def form_valid(self, form):
        company = get_object_or_404(Company, id=self.kwargs['pk'])
        ledger = form.save(commit=False)
        ledger.company = company
        ledger.debit_amount = 0
        ledger.save()

        return HttpResponseRedirect(
            reverse_lazy('company:ledger_list', kwargs={'pk': company.id})
        )