from django.shortcuts import render

#@login_required
def super_admin_dashboard(request):
    return render(request, 'super_admin/super_admin_dashboard.html')  # Add `.html` extension