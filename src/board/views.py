import os
import logging
import tempfile
import subprocess

from django import shortcuts
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import DetailView

from accounts.users import list_all_users_by_date
from base.mixins import StaffRequiredMixin
from billing import forms as billing_forms
from billing.orders import list_all_processed_orders_by_date
from board.forms import DomainSyncForm, CSVFileSyncForm
from board.models import CSVFileSync
# from back.csv_import import load_from_csv
from zen import zmaster, zdomains

logger = logging.getLogger(__name__)


class FinancialReportView(StaffRequiredMixin, FormView):
    template_name = 'board/financial_report.html'
    form_class = billing_forms.FilterOrdersByDateForm
    success_url = reverse_lazy('financial_report')

    def form_valid(self, form):
        year = form.cleaned_data.get('year')
        month = form.cleaned_data.get('month')
        if year or (year and month):
            orders_for_specific_time = list_all_processed_orders_by_date(
                year=form.data.get('year'),
                month=form.data.get('month')
            )

            order_items = []
            total_payment = 0

            for order in orders_for_specific_time:
                for order_item in order.items.all():
                    order_items.append(order_item)
                    total_payment += order_item.price
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    object_list=order_items,
                    total_payment_by_users=total_payment,
                    total_registered_users=len(list_all_users_by_date(year, month))
                )
            )
        return super().form_valid(form)


class NotExistingDomainSyncView(StaffRequiredMixin, FormView):
    template_name = 'board/not_existing_domain_sync.html'
    form_class = DomainSyncForm
    success_url = reverse_lazy('not_existing_domain_sync')

    def form_valid(self, form):
        domain_name = form.cleaned_data.get('domain_name')
        zmaster.domain_synchronize_from_backend(
            domain_name=form.cleaned_data.get('domain_name'),
            refresh_contacts=True,
            rewrite_contacts=False,
            change_owner_allowed=True,
            create_new_owner_allowed=True,
            soft_delete=True,
            raise_errors=True,
            log_events=True,
            log_transitions=True,
        )

        domain_in_db = zdomains.domain_find(domain_name=domain_name)
        if domain_in_db:
            logger.info(f'{domain_name} is successfully synced.')
            messages.success(self.request, f'{domain_name} is successfully synced.')
        else:
            messages.warning(self.request, f'Something went wrong during sync of {domain_name}')

        return super().form_valid(form)


class CSVFileSyncRecordView(StaffRequiredMixin, DetailView):
    template_name = 'board/csv_file_sync_record.html'

    def get_object(self, queryset=None):
        return shortcuts.get_object_or_404(CSVFileSync, pk=self.kwargs.get('record_id'))


class CSVFileSyncView(StaffRequiredMixin, FormView):
    template_name = 'board/csv_file_sync.html'
    form_class = CSVFileSyncForm
    success_url = reverse_lazy('csv_file_sync')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['csv_file_sync_records'] = CSVFileSync.executions.all().order_by('-pk')
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('csv_file')

        if not form.is_valid():
            return self.form_invalid(form)

        if CSVFileSync.executions.filter(status='started').exists():
            messages.warning(self.request, 'Another background process is currently running, please wait before starting a new one.')
            return self.form_invalid(form)

        started_records = []

        for f in files:
            csv_sync_record = CSVFileSync.executions.create(
                input_filename='',
                dry_run=bool(form.data.get('dry_run', False)),
            )

            fout, csv_file_path = tempfile.mkstemp(suffix='.csv', prefix='domains-%d-' % csv_sync_record.id, dir='./csv_sync')
            csv_sync_record.input_filename = csv_file_path
            csv_sync_record.save()

            logger.info('reading {}\n'.format(csv_file_path))

            while True:
                chunk = f.file.read(100000)
                if not chunk:
                    break
                os.write(fout, chunk)
            os.close(fout)

            logger.info('file uploaded, new DB record created: %r', csv_sync_record)

            subprocess.Popen(
                './venv/bin/python src/manage.py csv_import --record_id={} {}'.format(
                    csv_sync_record.id, '--dry_run' if form.data.get('dry_run', False) else '',
                ),
                close_fds=True,
                shell=True,
            )

            started_records.append(csv_sync_record)

        messages.success(self.request, f'New background process started: {started_records}')
        return self.form_valid(form)
