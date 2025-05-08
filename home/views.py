from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import meds
# Create your views here.

#rendering the landing page
def landing(request):
    return render(request, "landing_page.html")

#Register
def register(request):
    if request.method == 'POST':
        form_type = request.POST.get('submit_type')
        if form_type == "patientForm":
            name = request.POST.get('Pname')
            email = request.POST.get('Pemail')
            no = request.POST.get('Pno')
            age = request.POST.get('Page')
            password = request.POST.get('Ppassword')


            patient = User.objects.filter(email = email)
            if patient.exists():
                messages.info(request, 'User with this email already exists, Try another email')
                return redirect('register/')
            patient = User.objects.create(
                first_name = name,
                email = email,
                last_name = age,
                username = no,
            )

            patient.set_password(password)
            patient.save()
            messages.info(request, 'Account created successfully')

            return redirect('/login1/')



        elif form_type == "doctorForm":
            name = request.POST.get('Dname')
            email = request.POST.get('Demail')
            no = request.POST.get('Dno')
            lic = request.POST.get('lic')
            password = request.POST.get('Dpassword')


            doctor = User.objects.filter(username = no)
            if doctor.exists():
                messages.info(request, 'User with this license already exists, Try another email')
                return redirect('register/')
            doctor = User.objects.create(
                first_name = name,
                email = email,
                last_name = lic,
                username = no,
        )

            doctor.set_password(password)
            doctor.save()
            messages.info(request, 'Account created successfully')

            return redirect('/login1/')
    return render(request, 'register.html')





# Login
def login1(request):
    if request.method == 'POST':
        form_type = request.POST.get('submit_type')
        if form_type == 'patientForm':
            no = request.POST.get('Pno')
            password = request.POST.get('Ppassword')

            if not User.objects.filter(username = no).exists():
                messages.error(request, 'Invalid user')
                return redirect('/login1/')
        
            patient = authenticate(username = no, password = password)

            if patient is None:
                messages.error(request, 'Invalid Password')
                return redirect('/login1/')
        
            else:
                login(request, patient)
                return redirect('/pdash/')
            
        
        elif form_type == 'doctorForm':
            no = request.POST.get('Dno')
            password = request.POST.get('Dpassword')

            if not User.objects.filter(username = no).exists():
                messages.error(request, 'Invalid user')
                return redirect('/login1/')
        
            doctor = authenticate(username = no, password = password)

            if doctor is None:
                messages.error(request, 'Invalid Password')
                return redirect('/login1/')
        
            else:
                login(request, doctor)
                return redirect('/ddash/')

    return render(request, 'login.html')

#Logout
def log_out(request):
    logout(request)
    return redirect('/login1')


#uid function
from .models import rfid
@login_required(login_url='/login1/')
def card(request):
    if request.method == 'POST':
        data = request.POST
        uid = data.get('uid')

        # Save the UID to RFID table
        rfid_obj = rfid.objects.create(uid=uid)

        # Save UID in session for next view
        request.session['rfid_uid'] = uid

        messages.info(request, "UID added....\n\n")
        return redirect('/pcard')

    return render(request, 'Patient/uid.html')



#patient pages
@login_required(login_url='/login1/')
def patient_dashboard(request):#dashboard
    return render (request, 'Patient/patient_dashb.html')

@login_required(login_url='/login1/')
def appointment(request):#appointment page
     
     if request.method == 'POST':
         messages.success(request, "Request Sent!\n Our team will respond shortly")
         return redirect('/pappointment')
     
     return render (request, 'Patient/patient_appointment.html')

@login_required(login_url='/login1/')
def pmeds(request):
    if request.method == "POST":
        data = request.POST
        bfr = data.get('bfr')
        afr = data.get('afr')

        # Get UID from session
        uid = request.session.get('rfid_uid')
        rfid_obj = None

        if uid:
            try:
                rfid_obj = rfid.objects.get(uid=uid)
            except rfid.DoesNotExist:
                pass  # optional: handle this edge case

        # Save meds with UID
        meds.objects.create(
            uid=rfid_obj,
            bfr=bfr,
            afr=afr
        )
        return redirect('/pmeds')

    return render(request, 'Patient/patient_meds.html', { 'pmeds': meds.objects.all() })



#deleting meds
@login_required(login_url='/login1/')
def delete_med(request, id):
    queryset = meds.objects.get(id = id)
    queryset.delete()
    return redirect('/pmeds')


@login_required(login_url='/login1/')
def vitals(request):#vitals stroing and reports making through chart.js
     

     if request.method == 'POST':
         messages.info(request, "Updated!!!!")
         return redirect('/pvitals')
     

     return render (request, 'Patient/patient_vitals.html')

@login_required(login_url='/login1/')
def presc(request):
     return render (request, 'Patient/presc_upload.html')

@login_required(login_url='/login1/')
def profile_p(request):#patient's profile
     return render (request, 'Patient/profile.html')

#doctor pages

@login_required(login_url='/login1/')
def doctor_dashboard(request):
    return render(request, 'Doctor/doctor_dashb.html')

@login_required(login_url='/login1/')
def check(request):
    return render(request, 'Doctor/Check_requests.html')

@login_required(login_url='/login1/')
def dprofile(request):
    return render(request, 'Doctor/doc_profile.html')

@login_required(login_url='/login1/')
def prescribe(request):
    return render(request, 'Doctor/Prescribe.html')

@login_required(login_url='/login1/')
def view_patients(request):
    return render(request, 'Doctor/View_patients.html')

@login_required(login_url='/login1/')
def view_reports(request):
    return render(request, 'Doctor/View_reports.html')


#Making an Api for sending data to arduino backend.
#we are sending data to arduino backend in form of json and there we are extracting the data and the 
#esp32 microcontroller will show the data on display and open the respective servos

from django.http import JsonResponse
from .models import meds


def get_meds_api(request, uid):
    try:
        # Compare meds.uid.uid with input uid
        schedule = meds.objects.get(uid__uid=uid)
        return JsonResponse({
            'before_food': schedule.bfr,
            'after_food': schedule.afr
        })
    except meds.DoesNotExist:
        return JsonResponse({'error': 'UID not found'}, status=404)

    

