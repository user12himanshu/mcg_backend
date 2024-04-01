from django.shortcuts import render


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
