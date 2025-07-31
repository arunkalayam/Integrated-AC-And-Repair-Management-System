from django.shortcuts import render,redirect,get_object_or_404

from .forms import *
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User, Technician, Shop  # Make sure these are imported

from django.shortcuts import render
from .models import User, Technician, Shop

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Technician, Shop, Booking  # Make sure Booking is imported

def admin1(request):
    admin_id = request.session.get('admin_id')
    if not admin_id:
        messages.warning(request, "Please log in as an admin to access the dashboard.")
        return redirect('login')

    context = {
        'user_count': User.objects.count(),
        'technician_count': Technician.objects.count(),
        'store_count': Shop.objects.count(),
        'booking_count': Booking.objects.count(),  # 🔹 Added booking count here
    }

    return render(request, 'admin.html', context)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import LoginForm
from .models import Login, Delivery   # import Delivery to fetch its shop

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['Email']
            password = form.cleaned_data['Password']

            # --- 1. Hard‑coded admin shortcut ---------------------------------
            if email == "admin@g.com" and password == "1":
                request.session.flush()  # Clear any existing session
                request.session['admin_id'] = "admin"  # ✅ Set correct session key
                return redirect('admin1')

            # --- 2. Look up Login record --------------------------------------
            try:
                user = Login.objects.get(Email=email)
            except Login.DoesNotExist:
                messages.error(request, "User does not exist")
                return render(request, 'login.html', {'form': form})

            # --- 3. Check password & active status ----------------------------
            if user.Password != password or user.status != 1:
                messages.error(request, "Invalid credentials or inactive account")
                return render(request, 'login.html', {'form': form})

            # --- 4. Route by user‑type ----------------------------------------
            utype = user.Usertype

            if utype == 'user':
                request.session.flush()
                request.session['user_id'] = user.id
                return redirect('user_home')

            elif utype == 'technician':
                request.session.flush()
                request.session['techinician_id'] = user.id
                return redirect('tech_home')

            elif utype == 'shop':
                request.session.flush()
                request.session['store_id'] = user.id
                return redirect('store_home')

            elif utype == 'delivery':
                # Fetch Delivery profile to know which shop this boy belongs to
                delivery_obj = get_object_or_404(Delivery, loginid=user)

                # Save *both* delivery_id and optionally shop_id in session
                request.session.flush()
                request.session['delivery_id'] = user.id
                return redirect('delivery_home')

            else:
                messages.error(request, "Unsupported user type")
                return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})



def home(request):
    return render(request,'home.html')

def user_home(request):
    a=request.session.get('user_id')
    logindata=get_object_or_404(User,loginid=a)
    return render(request,'user_home.html',{'logindata':logindata})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, Login
from .forms import UserForm, EmailEdit

def userprofile(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        messages.warning(request, "Please log in to access your profile.")
        return redirect('login')

    # Fetch user and login objects
    user_data = get_object_or_404(User, loginid=user_id)
    login_data = get_object_or_404(Login, id=user_id)

    if request.method == 'POST':
        form1 = UserForm(request.POST, instance=user_data)
        form2 = EmailEdit(request.POST, instance=login_data)

        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('user_home')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form1 = UserForm(instance=user_data)
        form2 = EmailEdit(instance=login_data)

    return render(request, 'userprofile.html', {
        'form1': form1,
        'form2': form2
    })

def user_register(request):
    if request.method=='POST':
        form=UserLogin(request.POST)
        form1=UserForm(request.POST)
        if form.is_valid() and form1.is_valid():
            f=form.save(commit=False)
            f.Usertype='user'
            f.status=1
            f.save()
            f1= form1.save(commit=False)
            f1.loginid=f
            f1.save()
            return redirect("home")
    else:
        form=UserLogin()
        form1=UserForm()
    return render(request,'user_register.html',{'form':form,'form1':form1})

def userheader(request):
    return render(request,'userheader.html')

def tech_home(request):
    return render(request,'tech_home.html')

def technician_reg(request):
    if request.method == 'POST':
        form = UserLogin(request.POST)
        usertech = UserTech(request.POST)

        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        location_name = request.POST.get('location_name')

        if form.is_valid() and usertech.is_valid():
            f = form.save(commit=False)
            f.Usertype = 'technician'
            f.status = 0
            f.save()

            t = usertech.save(commit=False)
            t.loginid = f

            # Save coordinates and location name
            try:
                if latitude:
                    t.latitude = float(latitude)
                if longitude:
                    t.longitude = float(longitude)
            except ValueError:
                pass

            if location_name:
                t.location_name = location_name

            t.save()
            return redirect("home")
    else:
        form = UserLogin()
        usertech = UserTech()

    return render(request, 'techreg.html', {'form': form, 'usertech': usertech})



from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserTech, EmailEdit
from .models import Technician, Login

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Technician, Login
from .forms import UserTech, EmailEdit

def techprofile(request):
    # ------------------------------------------------------------------
    # Session check — Ensure technician is logged in
    # ------------------------------------------------------------------
    tech_id = request.session.get('techinician_id')
    if not tech_id:
        messages.warning(request, "Please log in to access your profile.")
        return redirect('login')

    # ------------------------------------------------------------------
    # Get Technician and Login instances
    # ------------------------------------------------------------------
    tech_data = get_object_or_404(Technician, loginid=tech_id)
    login_data = get_object_or_404(Login, id=tech_id)

    # ------------------------------------------------------------------
    # POST → handle form submission
    # ------------------------------------------------------------------
    if request.method == 'POST':
        form1 = UserTech(request.POST, instance=tech_data)
        form2 = EmailEdit(request.POST, instance=login_data)

        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        location_name = request.POST.get('location_name')

        if form1.is_valid() and form2.is_valid():
            technician = form1.save(commit=False)

            # Safely update coordinates
            try:
                if latitude:
                    technician.latitude = float(latitude)
                if longitude:
                    technician.longitude = float(longitude)
            except ValueError:
                messages.warning(request, "Invalid coordinates were ignored.")

            # Update location name if provided
            if location_name:
                technician.location_name = location_name

            technician.save()
            form2.save()

            messages.success(request, "Profile updated successfully.")
            return redirect('tech_home')
        else:
            messages.error(request, "Please correct the errors below.")

    # ------------------------------------------------------------------
    # GET → show profile form
    # ------------------------------------------------------------------
    else:
        form1 = UserTech(instance=tech_data)
        form2 = EmailEdit(instance=login_data)

    return render(request, 'techprofile.html', {
        'forms1': form1,
        'form2': form2,
    })




def techheader(request):
    return render(request,'techheader.html')

from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import User  # Ensure you import your User model

def adminviewuser(request):
    # ✅ Session check for admin
    admin_id = request.session.get('admin_id')
    if not admin_id:
        messages.warning(request, "Please log in as an admin to view users.")
        return redirect('login')  # Redirect to your login page

    # ✅ Fetch and display all users
    users = User.objects.all()
    return render(request, 'admin-table.html', {'users': users})

from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Technician  # Make sure Technician model is imported

def adminviewtech(request):
    # ✅ Check if admin is logged in
    admin_id = request.session.get('admin_id')
    if not admin_id:
        messages.warning(request, "Please log in as an admin to view technicians.")
        return redirect('admintechview')  # Replace with the correct login URL name

    # ✅ Fetch all technician records
    user1 = Technician.objects.all()

    # ✅ Render technician view for admin
    return render(request, 'admintechview.html', {'user1': user1})


def store_home(request):
    return render(request,'store_home.html')

from django.shortcuts import render, redirect
from .forms import UserLogin, Store  # Make sure these are correctly imported
from .models import Shop

from django.shortcuts import render, redirect
from .forms import UserLogin, Store  # Adjust import if needed
def store(request):
    if request.method == 'POST':
        form = UserLogin(request.POST)
        store_form = Store(request.POST)

        if form.is_valid() and store_form.is_valid():
            # Save login credentials
            login_instance = form.save(commit=False)
            login_instance.Usertype = 'shop'
            login_instance.status = 0
            login_instance.save()

            # Save shop details
            shop_instance = store_form.save(commit=False)
            shop_instance.loginid = login_instance

            # Use cleaned_data for safe, validated input
            lat = store_form.cleaned_data.get('latitude')
            lon = store_form.cleaned_data.get('longitude')
            location = store_form.cleaned_data.get('location_name')

            # Print to console
            print(f"Latitude: {lat}, Longitude: {lon}, Location Name: {location}")

            shop_instance.latitude = float(lat) if lat else None
            shop_instance.longitude = float(lon) if lon else None
            shop_instance.location_name = location

            shop_instance.save()

            return redirect("home")
        else:
            print("Form errors:", form.errors, store_form.errors)

    else:
        form = UserLogin()
        store_form = Store()

    return render(request, 'storereg.html', {
        'form': form,
        'store': store_form
    })




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import Shop, Login
from .forms import Store, EmailEdit


def storeprofile(request):
    # ----------------------------------------------------------------------
    # 1. SESSION CHECK → Only allow access if store is logged in
    # ----------------------------------------------------------------------
    store_id = request.session.get('store_id')
    if not store_id:
        messages.warning(request, "You must log in to view your profile.")
        return redirect('login')

    # ----------------------------------------------------------------------
    # 2. FETCH existing Shop and Login objects
    # ----------------------------------------------------------------------
    store_data = get_object_or_404(Shop, loginid=store_id)
    login_data = get_object_or_404(Login, id=store_id)

    # ----------------------------------------------------------------------
    # 3. POST → Update Profile
    # ----------------------------------------------------------------------
    if request.method == 'POST':
        form1 = Store(request.POST, instance=store_data)
        form2 = EmailEdit(request.POST, instance=login_data)

        if form1.is_valid() and form2.is_valid():
            shop = form1.save(commit=False)

            # Store hidden/location fields if present
            shop.latitude = form1.cleaned_data.get('latitude')
            shop.longitude = form1.cleaned_data.get('longitude')
            shop.location_name = form1.cleaned_data.get('location_name')

            shop.save()
            form2.save()

            messages.success(request, "Profile updated successfully.")
            return redirect('store_home')
        else:
            messages.error(request, "Please correct the errors in the form.")

    # ----------------------------------------------------------------------
    # 4. GET → Show current profile data
    # ----------------------------------------------------------------------
    else:
        form1 = Store(instance=store_data)
        form2 = EmailEdit(instance=login_data)

    return render(request, 'storeprofile.html', {
        'forms2': form1,   # Preserving your original variable key
        'form2' : form2
    })




def storeheader(request):
    return render(request,'storeheader.html')

from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from .models import Shop  # Ensure Shop is correctly imported

def adminviewstore(request):
    # ✅ Ensure admin is logged in
    admin_id = request.session.get('admin_id')
    if not admin_id:
        messages.warning(request, "Please log in as an admin to view store accounts.")
        return redirect('adminstore')  # Replace 'login' with your actual admin login URL name

    # ✅ Fetch all shop/store records
    user2 = Shop.objects.all()

    # ✅ Render admin store view
    return render(request, 'adminstore.html', {'user2': user2})


def registers(request):
    return render(request,'user_register.html')


def aprove(request,id):
    lo=get_object_or_404(Login,id=id)
    lo.status=1
    lo.save()
    return redirect('admin1')

def reject(request,id):
    lo1=get_object_or_404(Login,id=id)
    lo1.save()
    return redirect('admin1')

from django.shortcuts import render
from django.db.models import Q
from geopy.distance import geodesic
from .models import Technician
from urllib.parse import urlencode

# views.py

from django.db.models import Avg

from django.shortcuts import render
from django.db.models import Q, Max
from geopy.distance import geodesic
from .models import Technician, Feedback

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Max, Q
from geopy.distance import geodesic

from .models import Technician, Feedback


def usertechview(request):
    # ------------------------------------------------------------------
    # 1.  Session check — ensure the user is logged in
    # ------------------------------------------------------------------
    if not request.session.get('user_id'):
        messages.warning(request, "Please log in to view technicians.")
        return redirect('login')

    # ------------------------------------------------------------------
    # 2.  Collect query‑string parameters
    # ------------------------------------------------------------------
    query        = request.GET.get('query', '').strip()
    user_lat     = request.GET.get('latitude')
    user_lon     = request.GET.get('longitude')
    search_type  = request.GET.get('search_type', 'general')
    error_code   = request.GET.get('error_code', 'noerror')
    image_url    = request.GET.get('image_url', '')

    # ------------------------------------------------------------------
    # 3.  Base queryset: annotate each technician with max rating
    # ------------------------------------------------------------------
    technicians = (
        Technician.objects
        .annotate(max_rating=Max('feedback__rating'))  # new efficient DB‑side annotation
        .all()
    )

    # ------------------------------------------------------------------
    # 4.  Text search (name, district, city, contact) if `query` provided
    # ------------------------------------------------------------------
    if query:
        technicians = technicians.filter(
            Q(Technician_Name__icontains=query) |
            Q(District__icontains=query)       |
            Q(City__icontains=query)           |
            Q(Contact__icontains=query)
        )

    # ------------------------------------------------------------------
    # 5.  Nearest‑first sorting if coords + search_type=nearest
    # ------------------------------------------------------------------
    if search_type == 'nearest' and user_lat and user_lon:
        try:
            user_pos = (float(user_lat), float(user_lon))
            tech_list = []
            for tech in technicians:
                if tech.latitude and tech.longitude:
                    tech.distance = round(
                        geodesic(user_pos, (float(tech.latitude), float(tech.longitude))).km, 2
                    )
                else:
                    tech.distance = None
                tech_list.append(tech)

            # sort by distance, pushing None to the end
            technicians = sorted(
                tech_list,
                key=lambda t: t.distance if t.distance is not None else float('inf')
            )
        except (ValueError, TypeError):
            messages.warning(request, "Invalid coordinates — distance sort ignored.")

    # ------------------------------------------------------------------
    # 6.  Render template
    # ------------------------------------------------------------------
    return render(request, 'usertechview.html', {
        'user1'     : technicians,
        'error_code': error_code,
        'image_url' : image_url,
    })





def booking(request,id):
    bo=get_object_or_404(Login,id=id)
    bo.status=1
    bo.save()
    return redirect('home')

from django.http import JsonResponse

from django.utils import timezone
from datetime import datetime, time, timedelta
from django.http import JsonResponse
from .models import Booking, Technician  # update if paths differ


def get_available_slots(request, tech_id):
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'error': 'No date provided'}, status=400)

    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        today = timezone.localdate()
        now_time = timezone.localtime().time()

        technician = Technician.objects.get(id=tech_id)
        all_slots = generate_time_slots(time(9, 0), time(17, 0))

        # ✨ Filter out past time slots if the selected date is today
        if selected_date == today:
            all_slots = [slot for slot in all_slots if slot > now_time]

        # Get existing bookings and mark conflicting slots
        existing_bookings = Booking.objects.filter(technicianid=technician, Date=selected_date)
        unavailable = set()

        for booking in existing_bookings:
            booking_dt = datetime.combine(selected_date, booking.Time)
            window_start = booking_dt - timedelta(minutes=30)
            window_end = booking_dt + timedelta(minutes=30)
            for slot in all_slots:
                slot_dt = datetime.combine(selected_date, slot)
                if window_start <= slot_dt <= window_end:
                    unavailable.add(slot)

        available_slots = [slot for slot in all_slots if slot not in unavailable]
        slot_list = [(slot.strftime('%H:%M'), slot.strftime('%I:%M %p')) for slot in available_slots]

        return JsonResponse({'slots': slot_list})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


import os
import requests
from urllib.parse import urlparse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
from django.contrib import messages
from .models import Booking, Technician, User
from .forms import BookingForm

from .models import User, Technician, Booking
from .forms import BookingForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime, timedelta, date, time
from urllib.parse import urlparse
from django.core.files.base import ContentFile
import os, requests


def generate_time_slots(start_time, end_time, interval_minutes=30):
    slots = []
    current = datetime.combine(date.today(), start_time)
    end = datetime.combine(date.today(), end_time)
    while current <= end:
        slots.append(current.time())
        current += timedelta(minutes=interval_minutes)
    return slots


from datetime import datetime, timedelta, time, date
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.contrib import messages
from django.utils import timezone
import requests
import os
from urllib.parse import urlparse

from .models import Booking, Technician, User
from .forms import BookingForm

# Utility: Generate time slots between 9:00 AM and 5:00 PM
def generate_time_slots(start_time: time, end_time: time, interval_minutes: int = 30):
    slots = []
    current = datetime.combine(date.today(), start_time)
    end_dt = datetime.combine(date.today(), end_time)
    while current <= end_dt:
        slots.append(current.time())
        current += timedelta(minutes=interval_minutes)
    return slots

def booktable(request, id, error):
    user_login_id = request.session.get('user_id')
    u_data = get_object_or_404(User, loginid=user_login_id)
    t_data = get_object_or_404(Technician, id=id)

    error_code = error
    image_url = request.GET.get('image_url')
    today = timezone.localdate()

    selected_date_str = request.POST.get('Date') or request.GET.get('Date')
    try:
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date() if selected_date_str else today
    except ValueError:
        selected_date = today

    # Generate all slots from 9:00 to 17:00
    all_slots = generate_time_slots(time(9, 0), time(17, 0))

    # Remove past slots if date is today — round to next 30-min slot
    if selected_date == today:
        now_dt = timezone.localtime()
        hour = now_dt.hour
        minute = now_dt.minute

        if minute < 30:
            next_slot = time(hour, 30)
        else:
            next_slot = time(hour + 1, 0) if hour < 23 else time(23, 59)

        all_slots = [s for s in all_slots if s >= next_slot]

    # Filter out ±30 min conflicts
    blocked = set()
    existing_bookings = Booking.objects.filter(technicianid=t_data, Date=selected_date)
    for booking in existing_bookings:
        booking_dt = datetime.combine(selected_date, booking.Time)
        win_start = booking_dt - timedelta(minutes=30)
        win_end = booking_dt + timedelta(minutes=30)
        for slot in all_slots:
            slot_dt = datetime.combine(selected_date, slot)
            if win_start <= slot_dt <= win_end:
                blocked.add(slot)

    available_slots = [s for s in all_slots if s not in blocked]
    time_choices = [(s.strftime('%H:%M'), s.strftime('%I:%M %p')) for s in available_slots]

    # --- POST logic ---
    if request.method == 'POST':
        forms3 = BookingForm(request.POST, request.FILES)
        forms3.fields['Time'].choices = time_choices  # update choices dynamically

        if forms3.is_valid():
            booking_date = forms3.cleaned_data['Date']
            if booking_date < today:
                messages.error(request, "You cannot book a past date.")
            else:
                booking_time = datetime.strptime(forms3.cleaned_data['Time'], "%H:%M").time()
                booking_dt = datetime.combine(booking_date, booking_time)
                win_start = booking_dt - timedelta(minutes=30)
                win_end = booking_dt + timedelta(minutes=30)

                conflict = Booking.objects.filter(
                    technicianid=t_data,
                    Date=booking_date,
                    Time__gte=win_start.time(),
                    Time__lte=win_end.time()
                ).exists()

                if conflict:
                    messages.error(request, "Technician is already booked in this time window.")
                else:
                    booking = forms3.save(commit=False)
                    booking.user = u_data
                    booking.technicianid = t_data
                    booking.Time = booking_time

                    if not request.FILES.get('Error_img') and image_url:
                        fetch_url = image_url
                        if fetch_url.startswith('/'):
                            fetch_url = request.build_absolute_uri(fetch_url)
                        try:
                            resp = requests.get(fetch_url)
                            if resp.status_code == 200:
                                filename = os.path.basename(urlparse(fetch_url).path) or 'error.jpg'
                                booking.Error_img.save(filename, ContentFile(resp.content), save=False)
                        except requests.RequestException:
                            pass  # fail silently

                    booking.save()
                    messages.success(request, "Booking successful.")
                    return redirect('user_home')
    else:
        # Initial form load
        forms3 = BookingForm(initial={'Error_code': error_code, 'Date': selected_date})
        forms3.fields['Time'].choices = time_choices

    # Always enforce min="today" on the date field
    forms3.fields['Date'].widget.attrs['min'] = today.isoformat()

    return render(request, 'booktable.html', {
        'forms3': forms3,
        'image_url': image_url,
        't_data': t_data,
        'today': today.isoformat(),
    })




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Technician, Booking


def tech_request(request):
    # ---------------------------------------------------------------
    # 1️⃣  Session check – technician must be logged in
    # ---------------------------------------------------------------
    tech_login_id = request.session.get('techinician_id')
    if not tech_login_id:
        messages.warning(request, "Please log in to view your booking requests.")
        return redirect('login')

    # ---------------------------------------------------------------
    # 2️⃣  Get technician record linked to the session login ID
    # ---------------------------------------------------------------
    technician = get_object_or_404(Technician, loginid=tech_login_id)

    # ---------------------------------------------------------------
    # 3️⃣  Fetch all open booking requests (co_status = 0)
    # ---------------------------------------------------------------
    pending_requests = Booking.objects.filter(
        technicianid=technician,
        co_status=0
    )

    # ---------------------------------------------------------------
    # 4️⃣  Render template
    # ---------------------------------------------------------------
    return render(request, 'tech_request.html', {
        'forms3': pending_requests
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, Booking


def bookingviewuser(request):
    # ---------------------------------------------------------------
    # 1️⃣  Session check — ensure the user is logged in
    # ---------------------------------------------------------------
    user_login_id = request.session.get('user_id')
    if not user_login_id:
        messages.warning(request, "Please log in to see your bookings.")
        return redirect('login')

    # ---------------------------------------------------------------
    # 2️⃣  Retrieve the User record linked to this session
    # ---------------------------------------------------------------
    user_obj = get_object_or_404(User, loginid=user_login_id)

    # ---------------------------------------------------------------
    # 3️⃣  Fetch all bookings for this user
    # ---------------------------------------------------------------
    user_bookings = Booking.objects.filter(user=user_obj)

    # ---------------------------------------------------------------
    # 4️⃣  Render the bookings template
    # ---------------------------------------------------------------
    return render(request, 'bookingviewuser.html', {
        'forms3': user_bookings
    })


def cancel(request,id):
    bo=get_object_or_404(Booking,id=id)
    bo.status=1
    bo.save()
    return redirect('bookingviewuser')

def edit(request,id):
    a=request.session.get('user_id')
    u_data=get_object_or_404(User,loginid=a)
    t_data=get_object_or_404(Booking,id=id)
    if request.method=='POST':
        forms3=BookingForm(request.POST,instance=t_data)
        a=forms3.save(commit=False)
        a.save()
        return redirect('bookingviewuser')
    else:
        forms3=BookingForm(instance=t_data)
    return render(request,'booktable.html',{'forms3':forms3})

def techapprove(request,id):
    bo2=get_object_or_404(Booking,id=id)
    bo2.tech_status=1
    bo2.save()
    return redirect('tech_request')

def techreject(request,id):
    bo3=get_object_or_404(Booking,id=id)
    bo3.tech_status=2
    bo3.save()
    return redirect('tech_request')


def feedback_user(request, id):
    a = request.session.get('user_id')
    u_data = get_object_or_404(User, loginid=a)
    b_data = get_object_or_404(Technician, id=id)

    if request.method == 'POST':
        forms4 = FeedbackForm(request.POST)
        if forms4.is_valid():
            feedback = forms4.save(commit=False)
            feedback.user = u_data
            feedback.technicianid = b_data
            feedback.rating = int(request.POST.get('rating', 0))  # safely get the rating
            feedback.save()
            return redirect('feedbackview')
    else:
        forms4 = FeedbackForm()

    return render(request, 'feedback.html', {'forms4': forms4})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, Feedback

def feedbackview(request):
    # ---------------------------------------------------------------
    # 1️⃣  Check if user is logged in via session
    # ---------------------------------------------------------------
    user_login_id = request.session.get('user_id')
    if not user_login_id:
        messages.warning(request, "Please log in to view your feedback.")
        return redirect('login')

    # ---------------------------------------------------------------
    # 2️⃣  Fetch the corresponding User object
    # ---------------------------------------------------------------
    user_obj = get_object_or_404(User, loginid=user_login_id)

    # ---------------------------------------------------------------
    # 3️⃣  Fetch feedback records for this user
    # ---------------------------------------------------------------
    user_feedback = Feedback.objects.filter(user=user_obj)

    # ---------------------------------------------------------------
    # 4️⃣  Render the template with feedback
    # ---------------------------------------------------------------
    return render(request, 'feedbackview.html', {
        'forms4': user_feedback
    })



def feedback_delete(request,id):
    ko=get_object_or_404(Feedback,id=id)
    ko.delete()
    return redirect('feedbackview')

def feedback_edit(request,id):
    a=request.session.get('user_id')
    r_data=get_object_or_404(User,loginid=a)
    t_data=get_object_or_404(Feedback,id=id)
    if request.method=='POST':
        forms4=FeedbackForm(request.POST,instance=t_data)
        a=forms4.save(commit=False)
        a.save()
        return redirect('feedbackview')
    else:
        forms4=FeedbackForm(instance=t_data)
    return render(request,'feedback.html',{'forms4':forms4})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Feedback

def feedbackbookview(request, id):
    # ------------------------------------------------------------------
    # 1️⃣  Session check – must be logged‑in (user or technician)
    # ------------------------------------------------------------------
    if not (request.session.get('user_id') or request.session.get('techinician_id')):
        messages.warning(request, "Please log in to view feedback.")
        return redirect('login')

    # ------------------------------------------------------------------
    # 2️⃣  Fetch all feedback entries for the given technician ID
    # ------------------------------------------------------------------
    feedback_qs = Feedback.objects.filter(technicianid=id)

    # ------------------------------------------------------------------
    # 3️⃣  Render template
    # ------------------------------------------------------------------
    return render(request, 'feedbook.html', {
        'forms5': feedback_qs
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Shop
from .forms import PartsForm

def storeparts(request):
    # ------------------------------------------------------------------
    # 1️⃣ Session validation
    # ------------------------------------------------------------------
    store_login_id = request.session.get('store_id')
    if not store_login_id:
        messages.warning(request, "Please log in as a store to add parts.")
        return redirect('login')

    # ------------------------------------------------------------------
    # 2️⃣ Fetch store data using loginid from session
    # ------------------------------------------------------------------
    s_data = get_object_or_404(Shop, loginid=store_login_id)

    # ------------------------------------------------------------------
    # 3️⃣ Handle POST request — save part linked to the store
    # ------------------------------------------------------------------
    if request.method == 'POST':
        forms5 = PartsForm(request.POST, request.FILES)
        if forms5.is_valid():
            part = forms5.save(commit=False)
            part.store_id = s_data
            part.save()
            messages.success(request, "Part added successfully.")
            return redirect('partsview')
    else:
        forms5 = PartsForm()

    # ------------------------------------------------------------------
    # 4️⃣ Render the form
    # ------------------------------------------------------------------
    return render(request, 'storeparts.html', {
        'forms5': forms5
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Shop, Parts

def partsview(request):
    # ------------------------------------------------------------------
    # 1️⃣  Session check — must be a logged‑in store
    # ------------------------------------------------------------------
    store_login_id = request.session.get('store_id')
    if not store_login_id:
        messages.warning(request, "Please log in as a store to view your parts.")
        return redirect('login')

    # ------------------------------------------------------------------
    # 2️⃣  Retrieve the store linked to this login ID
    # ------------------------------------------------------------------
    store_obj = get_object_or_404(Shop, loginid=store_login_id)

    # ------------------------------------------------------------------
    # 3️⃣  Fetch all parts belonging to this store
    # ------------------------------------------------------------------
    store_parts = Parts.objects.filter(store_id=store_obj)

    # ------------------------------------------------------------------
    # 4️⃣  Render the template
    # ------------------------------------------------------------------
    return render(request, 'partsview.html', {
        'forms5': store_parts
    })


def parts_edit(request,id):
    a=request.session.get('store_id')
    r_data=get_object_or_404(Shop,loginid=a)
    t_data=get_object_or_404(Parts,id=id)
    if request.method=='POST':
        forms5=PartsForm(request.POST,request.FILES,instance=t_data)
        a=forms5.save(commit=False)
        a.save()
        return redirect('partsview')
    else:
        forms5=PartsForm(instance=t_data)
    return render(request,'storeparts.html',{'forms5':forms5})

def parts_delete(request,id):
    ko=get_object_or_404(Parts,id=id)
    ko.delete()
    return redirect('partsview')

from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from geopy.distance import geodesic
from .models import Booking, Parts

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from geopy.distance import geodesic
from .models import Booking, Parts, Technician

def techpartsview(request, id):
    # ------------------------------------------------------------------
    # 1️⃣  Session check — technician must be logged in
    # ------------------------------------------------------------------
    tech_login_id = request.session.get('techinician_id')
    if not tech_login_id:
        messages.warning(request, "Please log in as a technician to view parts.")
        return redirect('login')

    # ------------------------------------------------------------------
    # 2️⃣  Validate technician from session
    # ------------------------------------------------------------------
    technician = get_object_or_404(Technician, loginid=tech_login_id)

    # ------------------------------------------------------------------
    # 3️⃣  Fetch booking details (used in template)
    # ------------------------------------------------------------------
    booking = get_object_or_404(Booking, id=id)

    # ------------------------------------------------------------------
    # 4️⃣  Get search params
    # ------------------------------------------------------------------
    query = request.GET.get('query', '')
    user_lat = request.GET.get('latitude')
    user_lon = request.GET.get('longitude')
    search_type = request.GET.get('search_type')

    # ------------------------------------------------------------------
    # 5️⃣  Base parts queryset
    # ------------------------------------------------------------------
    parts = Parts.objects.select_related('store_id').all()

    # ------------------------------------------------------------------
    # 🔍 Text-based search
    # ------------------------------------------------------------------
    if query:
        parts = parts.filter(
            Q(Parts_name__icontains=query) |
            Q(Amount__icontains=query) |
            Q(Description__icontains=query)
        )

    # ------------------------------------------------------------------
    # 📍 Location-based search
    # ------------------------------------------------------------------
    if search_type == "nearest" and user_lat and user_lon:
        try:
            user_location = (float(user_lat), float(user_lon))
            parts_with_distance = []

            for part in parts:
                shop = part.store_id
                if shop.latitude and shop.longitude:
                    shop_location = (float(shop.latitude), float(shop.longitude))
                    part.distance = round(geodesic(user_location, shop_location).km, 2)
                else:
                    part.distance = None
                parts_with_distance.append(part)

            parts = sorted(parts_with_distance, key=lambda p: p.distance if p.distance is not None else float('inf'))

        except (ValueError, TypeError):
            pass  # Ignore invalid coordinates

    # ------------------------------------------------------------------
    # ✅ Final render
    # ------------------------------------------------------------------
    return render(request, 'techpartsview.html', {
        'forms5': parts,
        'c': booking
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app2.models import Technician, Order
from app2.forms import PaymentForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Technician, Order
from .forms  import PaymentForm


def payment(request, id, qq):
    # ------------------------------------------------------------------
    # 1️⃣  Session check – technician must be logged in
    # ------------------------------------------------------------------
    tech_login_id = request.session.get('techinician_id')
    if not tech_login_id:
        messages.warning(request, "Please log in as a technician to proceed with payment.")
        return redirect('login')

    # ------------------------------------------------------------------
    # 2️⃣  Fetch technician and order objects
    # ------------------------------------------------------------------
    technician = get_object_or_404(Technician, loginid=tech_login_id)
    order_obj  = get_object_or_404(Order, id=id)

    # ------------------------------------------------------------------
    # 3️⃣  Validate quantity from URL param
    # ------------------------------------------------------------------
    try:
        quantity = int(qq)
        if quantity <= 0:
            raise ValueError
    except ValueError:
        messages.error(request, "Invalid quantity received.")
        return redirect('orderview')

    # ------------------------------------------------------------------
    # 4️⃣  Calculate pricing
    # ------------------------------------------------------------------
    unit_price   = int(order_obj.partsid.Amount)
    total_amount = quantity * unit_price

    # ------------------------------------------------------------------
    # 5️⃣  POST – process payment form
    # ------------------------------------------------------------------
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_obj = form.save(commit=False)
            payment_obj.technicianid = technician
            payment_obj.amount       = total_amount
            # deliveryid left blank for technician payment
            payment_obj.save()

            # Update order as paid
            order_obj.p_status     = 1
            order_obj.Total_Amount = total_amount
            order_obj.save()

            messages.success(request, "Payment successful.")
            return redirect('tech_order', technician.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PaymentForm()

    # ------------------------------------------------------------------
    # 6️⃣  Render payment page
    # ------------------------------------------------------------------
    return render(request, 'payment.html', {
        'forms4'  : form,
        'amt'     : unit_price,
        'quantity': quantity,
        'total'   : total_amount
    })


from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Parts, Booking, Technician, Order

def orderview(request, id, c):
    # ----------------------------------------
    # 1️⃣  Session: Check technician is logged in
    # ----------------------------------------
    technician_login_id = request.session.get('techinician_id')
    if not technician_login_id:
        messages.warning(request, "Please log in as a technician.")
        return redirect('login')

    # ----------------------------------------
    # 2️⃣  Get relevant objects
    # ----------------------------------------
    part      = get_object_or_404(Parts, id=id)
    booking   = get_object_or_404(Booking, id=c)
    technician = get_object_or_404(Technician, loginid=technician_login_id)

    # ----------------------------------------
    # 3️⃣  POST: Process quantity and create order
    # ----------------------------------------
    if request.method == 'POST':
        quantity_str = request.POST.get('Quantity')
        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError("Quantity must be positive.")
        except (TypeError, ValueError):
            messages.error(request, "Invalid quantity. Please enter a valid positive number.")
            return render(request, 'orderview.html', {'c': part, 'u_data': technician})

        # Check stock availability
        if part.Quantity < quantity:
            messages.error(request, f"Only {part.Quantity} items are available in stock.")
            return render(request, 'orderview.html', {'c': part, 'u_data': technician})

        # ----------------------------------------
        # ✅ Create Order
        # ----------------------------------------
        order = Order.objects.create(
            technicianid=technician,
            partsid=part,
            p_status=0,
            c_status=0,
            r_status=0,
            del_status=0,
            ret_status=0,
            bookin_id=booking,
        )

        # Update parts quantity
        part.Quantity -= quantity
        part.save()

        messages.success(request, "Order placed. Proceeding to payment.")
        return redirect('payorder', order.id, quantity)

    # ----------------------------------------
    # 4️⃣  GET: Show order form
    # ----------------------------------------
    return render(request, 'orderview.html', {'c': part, 'u_data': technician})


    
from django.shortcuts import render, get_object_or_404
from .models import Order, Shop

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Shop, Order

def paystoreview(request):
    # ----------------------------------------
    # 1️⃣ Check session: store must be logged in
    # ----------------------------------------
    store_login_id = request.session.get('store_id')
    if not store_login_id:
        messages.warning(request, "Please log in as a store.")
        return redirect('login')  # or a dedicated store login view

    # ----------------------------------------
    # 2️⃣ Get store object
    # ----------------------------------------
    store = get_object_or_404(Shop, loginid=store_login_id)

    # ----------------------------------------
    # 3️⃣ Get only paid orders for this store
    # ----------------------------------------
    paid_orders = Order.objects.filter(partsid__store_id=store, p_status=1)

    # ----------------------------------------
    # 4️⃣ Render page
    # ----------------------------------------
    return render(request, 'paystoreview.html', {
        'forms5': paid_orders,
        'store_id': store.id
    })

from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Technician, Order

def tech_order_view(request, id):  # `id` is unused but still in signature
    # ----------------------------------------
    # 1️⃣ Check if technician is logged in
    # ----------------------------------------
    technician_login_id = request.session.get('techinician_id')
    if not technician_login_id:
        messages.warning(request, "Please log in as a technician to view orders.")
        return redirect('login')  # redirect to login page if not authenticated

    # ----------------------------------------
    # 2️⃣ Get Technician object
    # ----------------------------------------
    technician = get_object_or_404(Technician, loginid=technician_login_id)

    # ----------------------------------------
    # 3️⃣ Filter orders where payment is completed
    # ----------------------------------------
    paid_orders = Order.objects.filter(technicianid=technician, p_status=1)

    # ----------------------------------------
    # 4️⃣ Render the order list to technician
    # ----------------------------------------
    return render(request, 'ordersview_tech.html', {
        'forms5': paid_orders
    })

    
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Booking, Order, User  # adjust imports as needed

def userstoreview(request, id):
    # ✅ Ensure user is logged in
    user_login_id = request.session.get('user_id')
    if not user_login_id:
        messages.warning(request, "You must be logged in to view this page.")
        return redirect('login')  # Change 'login' to your login URL name

    # ✅ Get the user instance
    user = get_object_or_404(User, loginid=user_login_id)

    # ✅ Get the booking and verify it belongs to the logged-in user
    book = get_object_or_404(Booking, id=id)
    if book.user != user:
        return HttpResponseForbidden("You are not authorized to view this booking's store details.")

    # ✅ Fetch only PAID orders linked to this booking
    store_orders = Order.objects.filter(bookin_id=book, p_status=1)

    return render(request, 'userstoreview.html', {
        'forms5': store_orders
    })



def cancelled(request, id):
    order = get_object_or_404(Order, id=id)
    order.c_status = 1
    order.save()
    return redirect('tech_order', id=order.bookin_id.id)  # Pass Booking ID



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Order, Return, Technician, Delivery
from .forms import PaymentForm  # assume you have a form for payment

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Order, Technician, Return
from .forms import PaymentForm

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.contrib import messages
from .models import Technician, Order, Return
from .forms import PaymentForm

def refund(request, technician_id, order_id):
    # ✅ Fetch technician and order using URL parameters
    technician = get_object_or_404(Technician, id=technician_id)
    order = get_object_or_404(Order, id=order_id)

    # ✅ Verify the order belongs to the technician
    if order.technicianid != technician:
        return HttpResponseForbidden("You are not authorized to refund this order.")

    # ✅ Validate part price
    try:
        unit_price = int(order.partsid.Amount)
    except (ValueError, TypeError):
        messages.error(request, "Invalid part price.")
        return redirect('tech_order', technician.id)

    # ✅ Calculate quantity and total
    quantity = order.Total_Amount // unit_price if order.Total_Amount else 1
    total_amount = unit_price * quantity

    # ✅ Prevent double refunds
    if order.r_status == 1:
        messages.warning(request, "This order has already been refunded.")
        return redirect('tech_order', technician.id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # ✅ Save refund/payment record
            refund_obj = form.save(commit=False)
            refund_obj.technicianid = technician
            refund_obj.amount = total_amount
            refund_obj.save()

            # ✅ Update order status
            order.r_status = 1  # refunded
            order.ret_status = 1  # return pending
            order.save()

            # ✅ Restore stock quantity
            part = order.partsid
            part.Quantity += quantity
            part.save()

            # ✅ Create return record
            Return.objects.create(
                order_id=order,
                delivery_id=None,  # store will assign later
                technicianid=technician
            )

            messages.success(request, f"Refund completed. {quantity} item(s) returned to stock. Return pending.")
            return redirect('paystoreview')

    else:
        form = PaymentForm()

    return render(request, 'payment.html', {
        'forms4': form,
        'amt': unit_price,
        'quantity': quantity,
        'total': total_amount
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from .models import Chat, Technician, Login
from .forms import ChatForm

def chat(request, id):
    # ✅ Step 1: Validate session for logged-in user
    user_login_id = request.session.get('user_id')
    if not user_login_id:
        messages.error(request, "Please log in to access chat.")
        return redirect('login')  # Change this to your actual login route name

    # ✅ Step 2: Fetch user and technician logins
    user = get_object_or_404(Login, id=user_login_id)
    technician_login = get_object_or_404(Login, id=id)

    # ✅ Step 3: Fetch technician profile using their login
    technician_profile = get_object_or_404(Technician, loginid=technician_login)

    # ✅ Step 4: Fetch chat history between user and technician
    chat_history = Chat.objects.filter(
        Q(senderid=user, recieverid=technician_login) |
        Q(senderid=technician_login, recieverid=user)
    ).order_by('currentdate')

    # ✅ Step 5: Handle chat message submission
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.senderid = user
            chat.recieverid = technician_login
            chat.save()
            return redirect('chat', id=id)
    else:
        form = ChatForm()

    # ✅ Step 6: Render the chat template
    return render(request, 'chat.html', {
        'form': form,
        'ch': chat_history,
        'tech': technician_profile
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Chat, Login, User
from .forms import ChatForm

def tech_chat(request, id):
    # ✅ Step 1: Session check
    technician_login_id = request.session.get('techinician_id')
    if not technician_login_id:
        messages.error(request, "You must be logged in as a technician to access chat.")
        return redirect('login')  # Replace with your technician login route name

    # ✅ Step 2: Get technician Login and ensure existence
    technician_login = get_object_or_404(Login, id=technician_login_id)

    # ✅ Step 3: Get user Login and corresponding User profile
    user_login = get_object_or_404(Login, id=id)
    user_profile = get_object_or_404(User, loginid=user_login)

    # ✅ Step 4: Fetch chat messages between technician and user
    chat_history = Chat.objects.filter(
        Q(senderid=technician_login, recieverid=user_login) |
        Q(senderid=user_login, recieverid=technician_login)
    ).order_by('currentdate')

    # ✅ Step 5: Handle POST message submission
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.senderid = technician_login
            chat.recieverid = user_login
            chat.save()
            return redirect('tech_chat', id=id)
    else:
        form = ChatForm()

    # ✅ Step 6: Render template
    return render(request, 'tech_chat.html', {
        'form': form,
        'ch': chat_history,
        'user': user_profile  # passed to show user info in the template
    })


from django.db.models import Prefetch

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Chat, Login, User

def techchat_profile(request):
    # ✅ Step 1: Check if technician is logged in via session
    technician_login_id = request.session.get('techinician_id')
    if not technician_login_id:
        messages.error(request, "You must be logged in as a technician.")
        return redirect('login')  # Adjust to your actual login URL name

    # ✅ Step 2: Get the technician's Login object
    technician_login = get_object_or_404(Login, id=technician_login_id)

    # ✅ Step 3: Get all unique sender Login IDs who sent messages to this technician
    sender_login_ids = Chat.objects.filter(recieverid=technician_login)\
                                   .values_list('senderid', flat=True).distinct()

    # ✅ Step 4: Get corresponding User objects (linked to those Login IDs)
    senders = User.objects.select_related('loginid').filter(loginid__in=sender_login_ids)

    # ✅ Step 5: Render profile/chat list page
    return render(request, 'techchat_profile.html', {
        'senders': senders
    })


def usertechpay_notify(request,id):
    bo2=get_object_or_404(Booking,id=id)
    bo2.pa_status=1
    bo2.save()
    return redirect('tech_status',id)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Booking

def tracking(request, id):
    # ✅ Step 1: Ensure user is logged in via session
    user_login_id = request.session.get('user_id')
    if not user_login_id:
        messages.error(request, "You must be logged in to view tracking.")
        return redirect('login')  # Change to your actual login route name

    # ✅ Step 2: Fetch the booking and ensure it belongs to the logged-in user
    booking = get_object_or_404(Booking, id=id)
    if booking.user.loginid.id != user_login_id:
        messages.error(request, "Unauthorized access to booking tracking.")
        return redirect('bookingviewuser')  # Redirect to user's booking page

    # ✅ Step 3: Define booking progress steps
    steps = {
        'ongoing': True,
        'tracked': True,
        'onroad': booking.on_status == 1,
        'work_in_progress': booking.t_status == 1,
        'completed': booking.pa_status == 1,
    }

    # ✅ Step 4: Calculate progress percentage
    if steps['completed']:
        progress = 100
    elif steps['work_in_progress']:
        progress = 80
    elif steps['onroad']:
        progress = 60
    else:
        progress = 40

    # ✅ Step 5: Render tracking template
    return render(request, 'tracking.html', {
        'steps': steps,
        'progress': progress
    })



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Booking, Technician

def tech_status(request, id):
    # ✅ Step 1: Ensure technician is logged in
    technician_login_id = request.session.get('techinician_id')
    if not technician_login_id:
        messages.error(request, "You must be logged in as a technician to access this page.")
        return redirect('login')  # Replace with your actual login route

    # ✅ Step 2: Get the booking and verify that it belongs to this technician
    booking = get_object_or_404(Booking, id=id)

    # Optional strict check: ensure the booking is assigned to this technician
    if booking.technicianid.loginid.id != technician_login_id:
        messages.error(request, "Unauthorized access to booking status.")
        return redirect('tech_request')  # Redirect to technician's bookings list

    # ✅ Step 3: Render the technician status page
    return render(request, 'tech_status.html', {'c': booking})


def onroad(request,id):
    bo2=get_object_or_404(Booking,id=id)
    bo2.on_status=1
    bo2.save()
    return redirect('tech_status',id)


def work_in_progress(request,id):
    bo2=get_object_or_404(Booking,id=id)
    bo2.t_status=1
    bo2.save()
    return redirect('tech_status',id)

def logout(request):
    request.session.flush()
    return redirect('/')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, Technician
from .forms import ComplaintForm

def complaint(request, id):
    # ✅ Ensure user is logged in
    user_login_id = request.session.get('user_id')
    if not user_login_id:
        messages.warning(request, "Please log in to submit a complaint.")
        return redirect('login')

    # ✅ Get User and Technician instances
    user_obj = get_object_or_404(User, loginid=user_login_id)
    technician_obj = get_object_or_404(Technician, id=id)

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.technicianid = technician_obj
            complaint.user_id = user_obj
            complaint.save()
            messages.success(request, "Your complaint has been submitted.")
            return redirect('complaintview')
    else:
        form = ComplaintForm()

    return render(request, 'complaint.html', {'forms4': form})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Complaint, User

def complaintview(request):
    # ✅ 1. Check session for logged-in user
    user_login_id = request.session.get('user_id')
    if not user_login_id:
        messages.warning(request, "Please log in to view your complaints.")
        return redirect('login')

    # ✅ 2. Get User instance from Login ID
    try:
        user_obj = get_object_or_404(User, loginid=user_login_id)
    except:
        messages.error(request, "User not found.")
        return redirect('login')

    # ✅ 3. Filter complaints for this user
    complaints = Complaint.objects.filter(user_id=user_obj)

    # ✅ 4. Render template with user complaints
    return render(request, 'complaintview.html', {'forms4': complaints})

def complaint_delete(request,id):
    ko=get_object_or_404(Complaint,id=id)
    ko.delete()
    return redirect('complaintview')

def complaint_edit(request,id):
    a=request.session.get('user_id')
    r_data=get_object_or_404(User,loginid=a)
    t_data=get_object_or_404(Complaint,id=id)
    if request.method=='POST':
        forms4=ComplaintForm(request.POST,instance=t_data)
        if forms4.is_valid():
            a=forms4.save(commit=False)
            a.save()
            return redirect('complaintview')
    else:
        forms4=ComplaintForm()
    return render(request,'complaint.html',{'forms4':forms4})

def adminviewcomplaint(request):
   users=Complaint.objects.all()
   return render(request,'adminviewcomplaint.html',{'users':users})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Complaint

def admincomplaintreply(request, id):
    # ✅ 1. Check if admin is logged in
    admin_id = request.session.get('admin_id')
    if not admin_id:
        messages.warning(request, "Please log in as an admin to reply to complaints.")
        return redirect('login')

    # ✅ 2. Get the specific complaint
    comp = get_object_or_404(Complaint, id=id)

    # ✅ 3. Handle POST submission
    if request.method == 'POST':
        reply_text = request.POST.get('reply')
        if reply_text:
            comp.reply = reply_text
            comp.save()
            messages.success(request, "Reply submitted successfully.")
            return redirect('adminviewcomplaint')
        else:
            messages.error(request, "Reply cannot be empty.")

    # ✅ 4. Render reply form
    return render(request, 'admincomplaintreply.html', {'comp': comp})


def admin_header(request):
    return render(request,'admin_header.html')

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Booking, Order, Payment
from .forms import PaymentForm

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Booking, Order, Payment
from .forms import PaymentForm

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Sum
from .models import Booking, Order, Payment, Technician, User
from .forms import PaymentForm

def userpay(request, id):  # id = Booking ID
    # ✅ Step 1: Ensure user is logged in
    user_login_id = request.session.get('user_id')
    if not user_login_id:
        messages.error(request, "You must be logged in as a user to make a payment.")
        return redirect('login')  # Replace with your login URL

    # ✅ Step 2: Fetch booking and validate ownership
    booking = get_object_or_404(Booking, id=id)
    if booking.user.loginid.id != user_login_id:
        messages.error(request, "Unauthorized access to this booking.")
        return redirect('bookingviewuser')

    technician = booking.technicianid

    # ✅ Step 3: Get only eligible orders (not refunded)
    technician_orders = Order.objects.filter(
        bookin_id=booking,
        technicianid=technician,
        p_status=1,
        r_status=0
    )
    parts_amount = sum(order.Total_Amount for order in technician_orders)

    # 💼 Technician service fee
    service_fee = 500

    # 💰 Final total to be paid
    total_to_pay = parts_amount + service_fee

    # ✅ Update booking amounts before rendering
    booking.parts_amount = parts_amount
    booking.book_amount = service_fee or 0
    booking.save()

    # ✅ Step 4: Handle payment form
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.technicianid = technician
            payment.amount = total_to_pay
            payment.save()

            # ✅ Mark booking as fully paid
            booking.pa_status = 1
            booking.co_status = 1
            booking.TotalAmount = total_to_pay
            booking.save()

            messages.success(request, "Payment successfully made to the technician.")
            return redirect('bookingviewuser')
    else:
        form = PaymentForm(initial={'amount': total_to_pay})

    # ✅ Step 5: Render payment page
    return render(request, 'userpay.html', {
        'form': form,
        'booking': booking,
        'technician': technician,
        'parts_amount': parts_amount,
        'book_amount': service_fee,
        'total': total_to_pay
    })

def acdisplay(request):
    return render(request, 'chatbot.html')


from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.conf import settings
import logging, json, re, requests

logger = logging.getLogger(__name__)
NEMOTRON_API_KEY = settings.NEMOTRON_API_KEY

# Utility: Format AI's HTML response
import re

def format_ai_response(ai_answer):
    # Format strong (bold)
    ai_answer = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', ai_answer)
    
    # Format italic
    ai_answer = re.sub(r'(?<!\*)\*(?!\*)(.*?)\*(?<!\*)', r'<em>\1</em>', ai_answer)
    
    # Format inline code
    ai_answer = re.sub(r'`([^`]*)`', r'<code>\1</code>', ai_answer)
    
    # Horizontal rule
    ai_answer = ai_answer.replace('---', '<hr>')
    
    # Blockquotes
    ai_answer = re.sub(r'^> (.*)', r'<blockquote>\1</blockquote>', ai_answer, flags=re.MULTILINE)

    # Ordered list items
    ai_answer = re.sub(r'(?m)^\d+\.\s+(.*)', r'<li>\1</li>', ai_answer)
    if '<li>' in ai_answer:
        ai_answer = '<ol>' + ai_answer + '</ol>'
    
    # Unordered list items
    ai_answer = re.sub(r'(?m)^[-*]\s+(.*)', r'<li>\1</li>', ai_answer)
    if '<li>' in ai_answer and '<ol>' not in ai_answer:
        ai_answer = '<ul>' + ai_answer + '</ul>'

    # Paragraphs
    ai_answer = ai_answer.replace('\n\n', '</p><p>')
    ai_answer = f'<p>{ai_answer}</p>'

    return ai_answer


from datetime import datetime, timedelta

@csrf_exempt
@require_POST
def acqn(request):
    try:
        session = request.session
        question = request.POST.get('question', '').strip()
        if not question:
            return JsonResponse({'error': 'Please provide a health-related question.'}, status=400)

        # Block questions related to AC error codes, repair, etc.
        restricted_keywords = [
            'error', 'e1', 'e2', 'e3', 'ec', 'f0', 'h3', 'p1', 'fault', 'leak', 
            'repair', 'compressor', 'drainage', 'technician', 'sensor', 'issue', 'troubleshoot'
        ]
        if any(keyword in question.lower() for keyword in restricted_keywords):
            return JsonResponse({
                'answer': (
                    "I'm here to assist with operating AC units and using remote control features. "
                    "Please ask a question related to using your AC or its remote."
                )
            })

        # Clear session if older than 10 minutes
        last_active = session.get('last_active')
        if last_active:
            last_time = datetime.strptime(last_active, "%Y-%m-%d %H:%M:%S")
            if datetime.now() - last_time > timedelta(minutes=10):
                session['chat_history'] = []

        # Retrieve or initialize chat history
        chat_history = session.get('chat_history', [])
        chat_history.append({"role": "user", "content": question})

        # Define system prompt
        system_prompt = {
            "role": "system",
            "content": (
                "You are a certified AI assistant trained exclusively to guide users on how to operate air conditioners (AC) and use remote control functions for specific AC brands. "
                "Your responses should strictly cover how to use features like cooling, heating, swing, fan speed, sleep mode, timers, and brand-specific functionalities (e.g., Daikin, LG, Voltas, Samsung, Panasonic, etc.). "
                "If a user asks any question that is not related to operating an AC or using its remote control—such as installation, repair, electrical issues, pricing, programming, or non-AC topics like sports, politics, or technology—reply strictly with: "
                "'I'm here to assist with operating AC units and using remote control features. Please ask a question related to using your AC or its remote.' "
                "Maintain a helpful, brand-aware, and instructional tone. Do not provide any unrelated information or general conversation."
            )
        }

        messages = [system_prompt] + chat_history[-10:]  # last 10 messages only

        # Prepare payload
        payload = {
            "model": "meta/llama3-70b-instruct",
            "messages": messages,
            "temperature": 0.5,
            "max_tokens": 800,
            "top_p": 1.0
        }

        headers = {
            'Authorization': f'Bearer {NEMOTRON_API_KEY}',
            'Content-Type': 'application/json'
        }

        response = requests.post("https://integrate.api.nvidia.com/v1/chat/completions", headers=headers, json=payload)

        if response.status_code != 200:
            logger.error(f"NemoTron API Error: {response.status_code} - {response.text}")
            return JsonResponse({'error': 'AI service is temporarily unavailable.'}, status=500)

        data = response.json()
        ai_answer = data['choices'][0]['message']['content'].strip()

        # Store updated session
        chat_history.append({"role": "assistant", "content": ai_answer})
        session['chat_history'] = chat_history
        session['last_active'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session.modified = True

        formatted_answer = format_ai_response(ai_answer)
        return JsonResponse({'answer': formatted_answer})
    except Exception as e:
        logger.exception("Error in AI conversation")
        return JsonResponse({'error': 'An unexpected error occurred. Please try again later.'}, status=500)


def uploadimage(request):
    return render(request,'upload.html')


       


import easyocr
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.files.storage import default_storage
import os

@csrf_exempt
def analyze_error_code(request):
    if request.method == 'POST' and 'image' in request.FILES:
        image_file = request.FILES['image']
        temp_path = default_storage.save(f'temp/{image_file.name}', image_file)
        image_full_path = default_storage.path(temp_path)

        reader = easyocr.Reader(['en'])
        results = reader.readtext(image_full_path)
        extracted_text = ' '.join([r[1] for r in results])
        detected_code = match_error_code(extracted_text)

        # Move to permanent storage
        final_path = default_storage.save(f'uploads/{image_file.name}', image_file)

        return JsonResponse({
            'code': detected_code or 'Not Recognized',
            'image_url': default_storage.url(final_path)  # Return URL path
        })

    return JsonResponse({'error': 'No image provided'}, status=400)

def match_error_code(text):
    # Extended AC error code database
    codes = {
        "E1": "Indoor unit temperature sensor fault",
        "E2": "Anti-freezing protection",
        "E3": "Fan motor fault",
        "E4": "Indoor fan speed out of control",
        "E5": "Communication error between indoor and outdoor units",
        "E6": "Compressor failure or overload protection",
        "E7": "Mode conflict or drive board error",
        "EC": "Refrigerant leakage detected",
        "F0": "Low refrigerant or blocked filter",
        "F1": "Indoor unit EEPROM parameter error",
        "F2": "Indoor unit ambient temperature sensor error",
        "F3": "Indoor coil temperature sensor error",
        "H1": "Defrost mode active (normal operation in heating)",
        "H3": "Compressor overload protection",
        "H5": "IPM module protection",
        "P0": "IPM module malfunction (DC drive)",
        "P1": "Voltage protection or high temp",
        "P2": "High discharge temperature",
        "P4": "Inverter compressor drive error",
        "U0": "Insufficient refrigerant",
        "U4": "Communication error between indoor units",
    }

    text_upper = text.upper()
    for code in codes:
        if code in text_upper:
            return f"{code}: {codes[code]}"
    return None

  # Assuming these are in forms.py

from django.shortcuts import get_object_or_404

def delivery_register(request):
    if request.method == 'POST':
        form = UserLogin(request.POST)
        form1 = DeliveryForm(request.POST, request.FILES)

        if form.is_valid() and form1.is_valid():
            login_obj = form.save(commit=False)
            login_obj.Usertype = 'delivery'
            login_obj.status = 1
            login_obj.save()

            delivery_obj = form1.save(commit=False)
            delivery_obj.loginid = login_obj

            # ✅ Get shop/store from session
            store_id = request.session.get('store_id')
            if not store_id:
                messages.error(request, "Store ID not found in session.")
                return redirect("some_error_page")  # handle gracefully

            shop = get_object_or_404(Shop, loginid=store_id)
            delivery_obj.store_id = shop
            delivery_obj.save()

            return redirect("login")
    else:
        form = UserLogin()
        form1 = DeliveryForm()

    return render(request, 'deliver_register.html', {'form': form, 'form1': form1})





from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Shop, Delivery

def delivery_reg_view(request, id):  # id = Order ID or reference ID
    # ✅ Step 1: Validate store session
    loid = request.session.get('store_id')
    if not loid:
        messages.error(request, "You must be logged in as a store to view deliveries.")
        return redirect('login')  # Adjust this to your login route name

    # ✅ Step 2: Get store/shop based on login ID
    shop = get_object_or_404(Shop, loginid=loid)

    # ✅ Step 3: Get all delivery personnel registered under this store
    deliveries = Delivery.objects.filter(store_id=shop)

    # ✅ Step 4: Render the view with relevant context
    return render(request, 'delivery_reg_view.html', {
        'forms3': deliveries,  # delivery list passed to template
        'order_id': id         # in case needed to allot from view
    })

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Shop, Delivery

def delivery_view_boys(request):
    # ✅ Step 1: Check if store is logged in via session
    loid = request.session.get('store_id')
    if not loid:
        messages.error(request, "Please log in as a store to view delivery personnel.")
        return redirect('login')  # 🔄 Adjust to your login route name

    # ✅ Step 2: Get the store (Shop) instance based on session login ID
    shop = get_object_or_404(Shop, loginid=loid)

    # ✅ Step 3: Fetch all delivery boys linked to this store
    deliveries = Delivery.objects.filter(store_id=shop)

    # ✅ Step 4: Render the template with delivery data
    return render(request, 'delivery_view.html', {
        'forms3': deliveries
    })



from .models import Allot

from django.shortcuts import render
from .models import Allot

from django.shortcuts import render, get_object_or_404, redirect
from .models import Allot, Order, Delivery
# views.py

from .forms import DeliveryAllotForm

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Order, Delivery, Allot
from .forms import DeliveryAllotForm

def assign_delivery(request, order_id, delivery_id):
    # ✅ Validate store session
    store_id = request.session.get('store_id')
    if not store_id:
        messages.error(request, "Please log in as a store.")
        return redirect('login')  # Adjust to your login URL name

    # ✅ Fetch order and delivery objects
    order = get_object_or_404(Order, id=order_id)
    delivery = get_object_or_404(Delivery, id=delivery_id)

    # ✅ Prevent duplicate allotments
    if Allot.objects.filter(Order_id=order).exists():
        messages.warning(request, "This order has already been assigned a delivery person.")
        return redirect('paystoreview')

    # ✅ Handle form submission
    if request.method == 'POST':
        form = DeliveryAllotForm(request.POST)
        if form.is_valid():
            delivery_time = form.cleaned_data['delivery_time']
            Allot.objects.create(
                Order_id=order,
                Delivery_id=delivery,
                delivery_time=delivery_time
            )
            order.del_status = 1  # ✅ Mark delivery as assigned
            order.save()

            messages.success(request, f"Delivery assigned to {delivery.Name} successfully.")
            return redirect('paystoreview')
    else:
        form = DeliveryAllotForm()

    # ✅ Render assignment form
    return render(request, 'assign_delivery_time.html', {
        'form': form,
        'order': order,
        'delivery': delivery
    })

# ✅ redirect back to orders list

from django.shortcuts import render, redirect, get_object_or_404
from .models import Allot, Order, Delivery
from django.contrib import messages

from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Allot

from django.shortcuts import render, get_object_or_404, redirect
from .models import Allot
from django.contrib import messages

def view_allotments(request, order_id):
    # ✅ Validate store session
    store_id = request.session.get('store_id')
    if not store_id:
        messages.error(request, "Please log in as a store to view allotments.")
        return redirect('store_home')  # Adjust to your store login/home URL

    # ✅ Fetch all allotments for the given order and store
    allotments = Allot.objects.select_related(
        'Order_id__partsid',
        'Order_id__technicianid',
        'Delivery_id'
    ).filter(
        Order_id__id=order_id,
        Delivery_id__store_id__loginid=store_id
    )

    # ✅ Render the allotments in the template
    return render(request, 'views_allotment.html', {
        'allotments': allotments
    })


from django.shortcuts import render, get_object_or_404, redirect
from .models import Delivery
from .forms import DeliveryForm  # Make sure this form exists
from django.shortcuts import render, redirect, get_object_or_404
from .models import Delivery
from .forms import DeliveryForm

def delivery_edit(request, id):
    delivery = get_object_or_404(Delivery, id=id)
    if request.method == 'POST':
        form1 = DeliveryForm(request.POST, instance=delivery)
        if form1.is_valid():
            form1.save()
            return redirect('delivery_view_boys')  # Redirect to delivery list view
    else:
        form1 = DeliveryForm(instance=delivery)
    return render(request, 'deliveryprofile.html', {'form1': form1, 'delivery': delivery})

from django.http import HttpResponseForbidden

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from .models import Delivery
from .forms  import DeliveryForm

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from .models import Delivery, Login
from .forms import DeliveryForm
from django.contrib import messages

def deliveryprofile(request):
    # ✅ Get the delivery login ID from session
    delivery_login_id = request.session.get('delivery_id')
    
    if not delivery_login_id:
        messages.error(request, "Please log in as a delivery personnel.")
        return redirect('login')  # Redirect to login if session is missing

    # ✅ Fetch Login and Delivery instance
    logindata = get_object_or_404(Login, id=delivery_login_id)

    try:
        delivery_data = Delivery.objects.get(loginid=logindata)
    except Delivery.DoesNotExist:
        return HttpResponseForbidden("Access denied: Delivery profile not found.")

    # ✅ Handle form POST and update profile
    if request.method == 'POST':
        form1 = DeliveryForm(request.POST, instance=delivery_data)
        if form1.is_valid():
            form1.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('deliveryprofile')
    else:
        form1 = DeliveryForm(instance=delivery_data)

    # ✅ Render the profile update form
    return render(request, 'deliveryprofile.html', {
        'form1': form1,
        'delivery': delivery_data
    })



def delivery_delete(request, id):
    delivery = get_object_or_404(Delivery, id=id)
    delivery.delete()
    return redirect('delivery_view_boys')

from django.shortcuts import render, get_object_or_404
from .models import Allot, Delivery

from django.shortcuts import render, get_object_or_404, redirect
from .models import Allot, Delivery, Order

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Delivery, Allot, Payment

def my_allotted_deliveries(request):
    # 1. Ensure user is logged‑in as a delivery person
    delivery_login_id = request.session.get('delivery_id')
    if not delivery_login_id:
        return redirect('login')

    delivery_obj = get_object_or_404(Delivery, loginid=delivery_login_id)

    # 2. Pull this delivery person’s current allotments
    my_allots = (
        Allot.objects
        .filter(Delivery_id=delivery_obj)
        .select_related('Order_id', 'Order_id__partsid', 'Order_id__technicianid')
    )

    # 3. Check if the current month’s payment has been logged
    today = timezone.localdate()
    payment_received = (
        Payment.objects
        .filter(
            deliveryid=delivery_obj,
            curr_date__year=today.year,
            curr_date__month=today.month
        )
        .exists()
    )

    # 4. Current datetime (for delivery time comparison in template)
    current_datetime = timezone.now()

    # 5. Render the template
    return render(
        request,
        'my_deliveries.html',
        {
            'my_allots': my_allots,
            'payment_received': payment_received,
            'now': current_datetime  # ✅ Add this to support time-based labels in the template
        }
    )


def mark_delivered(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.del_status = 2  # Mark as delivered
    order.save()
    return redirect('mydeliveries')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order, Return

def allot_return_delivery(request, order_id):
    # ✅ 1. Validate store session
    store_login_id = request.session.get('store_id')
    if not store_login_id:
        messages.error(request, "Unauthorized access. Please log in.")
        return redirect('login')  # Or your actual store login page

    # ✅ 2. Get the order
    order = get_object_or_404(Order, id=order_id)

    # ✅ 3. Check return eligibility: canceled, delivered, not already returned
    if order.c_status == 1 and order.del_status == 2 and order.ret_status == 0:
        # ✅ 4. Try to fetch previous delivery assignment
        previous_allot = order.allot_set.first()
        delivery_boy = previous_allot.Delivery_id if previous_allot else None

        if delivery_boy:
            # ✅ 5. Create return record
            Return.objects.create(
                order_id=order,
                technicianid=order.technicianid,
                delivery_id=delivery_boy
            )
            # ✅ 6. Mark return status on the order
            order.ret_status = 0
            order.save()

            messages.success(request, f"Return pickup assigned for Order #{order.id}")
        else:
            messages.error(request, "No previous delivery person found to assign return.")
    else:
        messages.warning(request, "This order is not eligible for return allotment.")

    return redirect('paystoreview')  # ✅ Replace if you have a custom order management view


from django.shortcuts import render, get_object_or_404
from .models import Order, Return
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order, Return

def view_return_delivery(request, order_id):
    # ✅ 1. Ensure the store is logged in
    store_login_id = request.session.get('store_id')
    if not store_login_id:
        messages.error(request, "Unauthorized access. Please log in as a store.")
        return redirect('login')

    # ✅ 2. Fetch the order
    order = get_object_or_404(Order, id=order_id)

    # ✅ 3. Try to fetch all associated return objects
    return_qs = Return.objects.filter(order_id=order)

    if return_qs.exists():
        return_objs = return_qs
        delivery_persons = [ret.delivery_id for ret in return_qs]
    else:
        return_objs = None
        delivery_persons = None

    # ✅ 4. Prepare context for the template
    context = {
        'order': order,
        'return_objs': return_objs,
        'delivery_persons': delivery_persons,
    }

    return render(request, 'view_return_delivery.html', context)




def mark_returned(request, order_id):
    # Get the order or return 404 if not found
    order = get_object_or_404(Order, id=order_id)

    # Allow return only if the technician has canceled the order and it's not yet returned
    if order.c_status == 1 and order.ret_status == 0:
        # Try to get the associated delivery (via Allot)
        allot = order.allot_set.first()
        if allot and allot.Delivery_id:
            # Record the return
            Return.objects.create(
                order_id=order,
                delivery_id=allot.Delivery_id,
                technicianid=order.technicianid
            )
            # Update order's return status
            order.ret_status = 1
            order.save()

    # Redirect back to delivery view
    return redirect('mydeliveries')  # Make sure 'mydeliveries' is the correct URL name
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Count, ExpressionWrapper, IntegerField
from .models import Delivery, Allot, Order, Shop, Payment
from datetime import datetime

from django.db.models import Count, ExpressionWrapper, IntegerField, Q
from .models import Payment  # make sure Payment is imported

from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Count, ExpressionWrapper, IntegerField
from .models import Delivery, Allot, Order, Shop, Payment
from datetime import datetime

def del_pay_list(request, store_id):
    store = get_object_or_404(Shop, pk=store_id)

    selected_month = request.GET.get('month')

    if selected_month:
        try:
            year, month = map(int, selected_month.split('-'))
            start_of_month = datetime(year, month, 1)
            end_of_month = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)
        except ValueError:
            start_of_month = timezone.now().replace(day=1)
            end_of_month = timezone.now()
    else:
        start_of_month = timezone.now().replace(day=1)
        end_of_month = timezone.now()

    deliveries = Delivery.objects.filter(store_id=store)

    allots = Allot.objects.filter(
        Order_id__current_date__gte=start_of_month,
        Order_id__current_date__lt=end_of_month,
        Delivery_id__store_id=store
    )

    allots_grouped = (
        allots.values('Delivery_id')
        .annotate(
            delivery_count=Count('id'),
            payment=ExpressionWrapper(Count('id') * 150, output_field=IntegerField())
        )
    )

    allot_map = {item['Delivery_id']: item for item in allots_grouped}

    delivery_data = []
    for d in deliveries:
        delivery_count = allot_map.get(d.id, {}).get('delivery_count', 0)
        payment_amount = allot_map.get(d.id, {}).get('payment', 0)

        # Check if payment was made for this delivery for this month
        is_paid = Payment.objects.filter(
            deliveryid=d,
            curr_date__gte=start_of_month,
            curr_date__lt=end_of_month
        ).exists()

        delivery_data.append({
            'id': d.id,
            'Name': d.Name,
            'Contact': d.Contact,
            'City': d.City,
            'License_no': d.License_no,
            'delivery_count': delivery_count,
            'payment': payment_amount,
            'is_paid': is_paid,
        })

    return render(request, 'del_pay_list.html', {
        'delivery_data': delivery_data,
        'selected_month': selected_month or timezone.now().strftime('%Y-%m'),
        'store': store,
    })



from django.shortcuts import redirect

def make_payment(request, delivery_id):
    today = timezone.now().date()
    start_of_month = today.replace(day=1)

    delivery = get_object_or_404(Delivery, pk=delivery_id)

    delivery_count = Allot.objects.filter(
        Delivery_id=delivery,
        Order_id__current_date__gte=start_of_month
    ).count()

    payment_amount = delivery_count * 150

    if request.method == "POST":
        # Redirect to payment input form
        return redirect('payment_form', delivery_id=delivery.id)

    context = {
        'delivery': delivery,
        'delivery_count': delivery_count,
        'payment': payment_amount,
    }
    return render(request, 'make_payment.html', context)

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Delivery, Allot, Order, Payment

from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import Delivery, Allot, Order, Payment

def delivery_pay_form(request, delivery_id):
    delivery = get_object_or_404(Delivery, pk=delivery_id)

    # Get selected month from GET (first visit) or POST (after form submission)
    selected_month = request.GET.get('month') or request.POST.get('selected_month')

    if selected_month:
        # Parse 'YYYY-MM' to date range
        try:
            start_of_month = datetime.strptime(selected_month, '%Y-%m')
            if start_of_month.month == 12:
                end_of_month = start_of_month.replace(year=start_of_month.year + 1, month=1, day=1)
            else:
                end_of_month = start_of_month.replace(month=start_of_month.month + 1, day=1)
        except ValueError:
            start_of_month = timezone.now().replace(day=1)
            end_of_month = (start_of_month + timedelta(days=32)).replace(day=1)
    else:
        # Default: current month
        start_of_month = timezone.now().replace(day=1)
        end_of_month = (start_of_month + timedelta(days=32)).replace(day=1)
        selected_month = start_of_month.strftime('%Y-%m')

    # Get deliveries from Allot where Order.current_date is within selected month
    allots = Allot.objects.filter(
        Delivery_id=delivery,
        Order_id__current_date__gte=start_of_month,
        Order_id__current_date__lt=end_of_month
    )

    delivery_count = allots.count()
    payment_amount = delivery_count * 150

    if request.method == 'POST':
        name = request.POST.get('name')
        card_no = request.POST.get('card_no')
        cvv = request.POST.get('cvv')
        expiry = request.POST.get('expiry')

        # Create payment record
        Payment.objects.create(
            Name_on_card=name,
            Card_No=card_no,
            CVV=cvv,
            Expiry_date=expiry,
            amount=str(payment_amount),
            technicianid=None,
            deliveryid=delivery,
            delivery_count=delivery_count
        )

        # Mark orders as paid (p_status = 1)
        for allot in allots:
            order = allot.Order_id
            order.p_status = 1
            order.save()

        return redirect('del_pay_list', store_id=delivery.store_id.id)

    return render(request, 'delivery_pay_form.html', {
        'delivery': delivery,
        'delivery_count': delivery_count,
        'payment': payment_amount,
        'selected_month': selected_month,
    })

def delivery_home(request):
    return render(request,'delivery_home.html')




























    
    









    





















# Create your views here