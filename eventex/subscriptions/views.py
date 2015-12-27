from django.shortcuts import render
from eventex.subscriptions.forms import SubscriptionForm


def subscribe(request):
    context = {'forms': SubscriptionForm()}
    return render(request, 'subscriptions/subscription_form.html', context)
