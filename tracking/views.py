from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import logout
from .models import Violation
from .forms import ViolationForm
from django.core.serializers import serialize
from django.db.models import Count
from django.utils import timezone
import json
from datetime import timedelta
from django.db.models import Sum, Count

def dashboard(request):
    today = timezone.now().date()
    last_week = today - timezone.timedelta(days=7)

    # Aggregate data for violations per date and violation type
    violations = (Violation.objects
                  .filter(date__range=[last_week, today])
                  .values('violation_type', 'date')
                  .annotate(count=Count('id'))
                  .order_by('date'))

    violation_list = []
    for violation in violations:
        violation_list.append({
            'violation_type': violation['violation_type'],
            'date': violation['date'].strftime('%Y-%m-%d'),  # Convert date to string
            'count': violation['count']
        })
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)  # Last 7 days

    fine_trend = (
        Violation.objects.filter(date__range=[start_date, end_date])
        .values('date')
        .annotate(total_fine=Sum('fine_collected'))
        .order_by('date')
    )

    # Convert to JSON serializable format
    fine_trend_data = list(fine_trend)

    # Serialize the data to JSON
    violation_df_json = json.dumps(violation_list)

    total_fine_collected = \
    Violation.objects.filter(date__range=[start_date, end_date]).aggregate(Sum('fine_collected'))[
        'fine_collected__sum'] or 0

    # Query the total number of violations for the last 7 days
    total_violations = Violation.objects.filter(date__range=[start_date, end_date]).count()
    total_vehicles = Violation.objects.filter(date__range=[start_date, end_date]).aggregate(
        distinct_vehicle_count=Count('vehicle_number', distinct=True)
    )['distinct_vehicle_count'] or 0



    violation = Violation.objects.all()
    context = {
        'violation_df_json': violation_df_json,
        'violations': violation,
        'fine_trend_json': json.dumps(fine_trend_data, default=str),
        'total_fine_collected': total_fine_collected,
        'total_violations': total_violations,
        'total_vehicles': total_vehicles

    }
    return render(request, 'home/index.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to a home or dashboard page
            else:
                messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html', {'form': form})


# View to create and edit violations
def violation_form(request, id=None):
    if id:
        violation = get_object_or_404(Violation, id=id)
    else:
        violation = None

    if request.method == 'POST':
        form = ViolationForm(request.POST, user=request.user)  # Pass the logged-in user to the form
        print("comimghere")
        if form.is_valid():
            form.save()  # Save the form
            return redirect('dashboard')  # Redirect to a list or confirmation page after submission
        else:
            print(form.errors)
    else:
        form = ViolationForm(user=request.user)
        form.fields['officer_name'].initial = request.user.username

    context = {
        'form': form,
        'current_violation': violation
    }

    return render(request, 'home/violation_form.html', context)


# View to list all violations
def violation_list(request):
    violations = Violation.objects.all()
    return render(request, 'violation_list.html', {'violations': violations})