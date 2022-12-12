from django.shortcuts import render


def custom_error_view(request, exception=None):
    return render(request, "page-500.html", {})


def custom_permission_denied_view(request, exception=None):
    return render(request, "page-403.html", {})


def custom_page_not_found_view(request, exception):
    return render(request, "page-404.html", {})
