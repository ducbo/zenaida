import btcpay
from django import shortcuts
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views import View

from billing.pay_btcpay.models import BTCPayInvoice


@login_required
def start_payment(request, transaction_id, amount):

    return shortcuts.render(
        request,
        'billing/btcpay/start_payment.html',
        {
            'transaction_id': transaction_id,
            'amount': amount
        }
    )


class ProcessPaymentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        transaction_id = kwargs.get('transaction_id')
        amount = request.POST['amount']

        client = btcpay.BTCPayClient(
                host=settings.ZENAIDA_BTCPAY_HOST,
                pem=settings.ZENAIDA_BTCPAY_CLIENT_PRIVATE_KEY,
                tokens={"merchant": settings.ZENAIDA_BTCPAY_MERCHANT}
            )

        btcpay_invoice = client.create_invoice({"price": amount, "currency": "USD"})

        BTCPayInvoice.invoices.create(
            transaction_id=transaction_id,
            invoice_id=btcpay_invoice.get('id'),
            status=btcpay_invoice.get('status'),
            amount=amount
        )

        return HttpResponseRedirect(btcpay_invoice.get("url"))