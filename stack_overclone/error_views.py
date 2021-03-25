from django.shortcuts import render

def page_not_found_view(request, exception):
    return render(request, '404_not_found.html', context={'exception': exception}, status=404)