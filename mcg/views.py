from django.shortcuts import render


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def terms_of_service(request):
    return render(request, 'terms.html')
