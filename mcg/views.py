from django.contrib import messages
from django.shortcuts import render
from .forms import EnquiryForm


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def terms_of_service(request):
    return render(request, 'terms.html')


def return_policy(request):
    return render(request, 'return.html')


def refund_policy(request):
    return render(request, 'refund.html')


def shipping_policy(request):
    return render(request, 'shipping.html')


def index(request):
    return render(request, 'index.html')


def contact_us(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your enquiry has been registered successfully!')
            return render(request, 'contact-us.html', {'form': form})
        else:
            messages.error(request, f'{form.errors}')
            return render(request, 'contact-us.html', {'form': form})
    else:
        form = EnquiryForm()
        return render(request, 'contact-us.html', {'form': form})
