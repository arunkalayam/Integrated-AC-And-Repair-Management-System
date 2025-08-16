from django.shortcuts import render,redirect,get_object_or_404

from .forms import UserLogin,UserForm,UserTech,User,Technician,Store,Shop,LoginForm,Login,EmailEdit,BookingForm,Booking,FeedbackForm,Feedback,PartsForm,Parts,Payment,PaymentForm,Order,Chat,ChatForm,Complaint,ComplaintForm,OrderForm
from django.db.models import Q
from django.contrib import messages
from django.http import HttpResponse

def admin(request):
    return render(request,'admin.html')

def login(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        print(form)
        if form.is_valid():
            email=form.cleaned_data['Email']
            password=form.cleaned_data['Password']
            if email == "admin@g.com" and password=="1":
                request.session['user_id'] ="admin"
                return redirect('admin1')
            
            try:
                user=Login.objects.get(Email=email)
                if user.Password==password and user.Usertype=='user'and user.status==1:
                    request.session['user_id']=user.id
                    return redirect('user_home')
                elif user.Password==password and user.Usertype=='technician'and user.status==1:
                    request.session['techinician_id']=user.id
                    return redirect('tech_home')
                elif user.Password==password and user.Usertype=='shop'and user.status==1:
                    request.session['store_id']=user.id
                    return redirect('store_home')

                else:
                    messages.error(request,'Invalid password')
            except Login.DoesNotExist:
                messages.error(request,'User not exists')
    else:
        form=LoginForm()
    return render(request,'login.html',{'form':form})

def home(request):
    return render(request,'home.html')

def user_home(request):
    return render(request,'user_home.html')

def userprofile(request):
    upro=request.session.get('user_id')
    user_data=get_object_or_404(User,loginid=upro)
    logindata=get_object_or_404(Login,id=upro)
    if request.method=='POST':
        form1=UserForm(request.POST,instance=user_data)
        form2=EmailEdit(request.POST,instance=logindata)
        if form1.is_valid() and form2.is_valid():
            form1.save()
            form2.save()
            return redirect('user_home')
    else:
        form1=UserForm(instance=user_data)
        form2=EmailEdit(instance=logindata)
    return render(request,'userprofile.html',{'form1':form1,'form2':form2})

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
            return redirect("login")
    else:
        form=UserLogin()
        form1=UserForm()
    return render(request,'user_register.html',{'form':form,'form1':form1})

def userheader(request):
    return render(request,'userheader.html')

def tech_home(request):
    return render(request,'tech_home.html')

def technician_reg(request):
    if request.method=='POST':
        form=UserLogin(request.POST)
        usertech=UserTech(request.POST)
        if form.is_valid() and usertech.is_valid():
            f=form.save(commit=False)
            f.Usertype='technician'
            f.status=0
            f.save()
            t= usertech.save(commit=False)
            t.loginid=f
            t.save()
            return redirect("login")
    else:
        form=UserLogin()
        usertech=UserTech()
    return render(request,'techreg.html',{'form':form,'usertech':usertech})

def techprofile(request):
    tpro=request.session.get('techinician_id')
    tech_data=get_object_or_404(Technician,loginid=tpro)
    logindata=get_object_or_404(Login,id=tpro)
    if request.method=='POST':
        forms1=UserTech(request.POST,instance=tech_data)
        form2=EmailEdit(request.POST,instance=logindata)
        if forms1.is_valid() and form2.is_valid():
            forms1.save()
            form2.save()
            return redirect('tech_home')
    else:
        forms1=UserTech(instance=tech_data)
        form2=EmailEdit(instance=logindata)
    return render(request,'techprofile.html',{'forms1':forms1,'form2':form2})

def techheader(request):
    return render(request,'techheader.html')


def adminviewuser(request):
   users=User.objects.all()
   return render(request,'admin-table.html',{'users':users})

def adminviewtech(request):
    user1=Technician.objects.all()
    return render(request,'admintechview.html',{'user1':user1})

def store_home(request):
    return render(request,'store_home.html')

def store(request):
    if request.method=='POST':
        form=UserLogin(request.POST)
        store=Store(request.POST)
        if form.is_valid() and store.is_valid():
            f=form.save(commit=False)
            f.Usertype='shop'
            f.status=0
            f.save()
            s= store.save(commit=False)
            s.loginid=f
            s.save()
            return redirect("login")
    else:
        form=UserLogin()
        store=Store()
    return render(request,'storereg.html',{'form':form,'store':store})

def storeprofile(request):
    spro=request.session.get('store_id')
    store_data=get_object_or_404(Shop,loginid=spro)
    logindata=get_object_or_404(Login,id=spro)
    if request.method=='POST':
        forms2=Store(request.POST,instance=store_data)
        form2=EmailEdit(request.POST,instance=logindata)
        if forms2.is_valid() and form2.is_valid():
            forms2.save()
            form2.save()
            return redirect('store_home')
    else:
        forms2=Store(instance=store_data)
        form2=EmailEdit(instance=logindata)
    return render(request,'storeprofile.html',{'forms2':forms2,'form2':form2})

def storeheader(request):
    return render(request,'storeheader.html')

def adminviewstore(request):
    user2=Shop.objects.all()
    return render(request,'adminstore.html',{'user2':user2})

def registers(request):
    return render(request,'user_register.html')


def aprove(request,id):
    lo=get_object_or_404(Login,id=id)
    lo.status=1
    lo.save()
    return redirect('/')

def reject(request,id):
    lo1=get_object_or_404(Login,id=id)
    lo1.save()
    return redirect('/')

def usertechview(request):
    query=request.GET.get('query')
    if query is None:
        user1=Technician.objects.all()
    elif query:
        user1=Technician.objects.filter(Q(Technician_Name__icontains=query)|Q(District__icontains=query)|Q(City__icontains=query)|Q(Contact__icontains=query))
    else:
        user1=Technician.objects.all()
    return render(request,'usertechview.html',{'user1':user1})

def booking(request,id):
    bo=get_object_or_404(Login,id=id)
    bo.status=1
    bo.save()
    return redirect('home')

def booktable(request,id):
    a=request.session.get('user_id')
    u_data=get_object_or_404(User,loginid=a)
    t_data=get_object_or_404(Technician,id=id)
    if request.method=='POST':
        forms3=BookingForm(request.POST)
        print(forms3)
        a=forms3.save(commit=False)
        a.user=u_data
        a.technicianid=t_data
        a.save()
        return redirect('user_home')
    else:
        forms3=BookingForm()
    return render(request,'booktable.html',{'forms3':forms3})

def tech_request(request):
    logid=request.session.get('techinician_id')
    tech_id=get_object_or_404(Technician,loginid=logid)
    forms3=Booking.objects.filter(technicianid=tech_id,co_status = 0)
    return render(request,'tech_request.html',{'forms3':forms3})

def bookingviewuser(request):
    loid=request.session.get('user_id')
    user_id=get_object_or_404(User,loginid=loid)
    forms3=Booking.objects.filter(user=user_id)
    return render(request,'bookingviewuser.html',{'forms3':forms3})

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


def feedback_user(request,id):
    a=request.session.get('user_id')
    u_data=get_object_or_404(User,loginid=a)
    b_data=get_object_or_404(Technician,id=id)
    if request.method=='POST':
        forms4=FeedbackForm(request.POST)
        a=forms4.save(commit=False)
        a.technicianid=b_data
        a.user=u_data
        a.save()
        return redirect('feedbackview')
    else:
        forms4=FeedbackForm()
    return render(request,'feedback.html',{'forms4':forms4})

def feedbackview(request):
    loid=request.session.get('user_id')
    user_id=get_object_or_404(User,loginid=loid)
    forms4=Feedback.objects.filter(user=user_id)
    return render(request,'feedbackview.html',{'forms4':forms4})


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

def feedbackbookview(request,id):
    forms5=Feedback.objects.filter(technicianid=id)
    return render(request,'feedbook.html',{'forms5':forms5})

def storeparts(request):
    a=request.session.get('store_id')
    s_data=get_object_or_404(Shop,loginid=a)
    if request.method=='POST':
        forms5=PartsForm(request.POST,request.FILES)
        if forms5.is_valid():
            a=forms5.save(commit=False)
            a.store_id=s_data
            a.save()
            return redirect('partsview')
    else:
        forms5=PartsForm()
    return render(request,'storeparts.html',{'forms5':forms5})

def partsview(request):
    loid=request.session.get('store_id')
    store=get_object_or_404(Shop,loginid=loid)
    forms5=Parts.objects.filter( store_id=store)
    return render(request,'partsview.html',{'forms5':forms5})

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

def techpartsview(request,id):
    c=get_object_or_404(Booking,id=id)
    query=request.GET.get('query')
    if query is None:
        forms5=Parts.objects.all()
    elif query:
        forms5=Parts.objects.filter(Q(Parts_name__icontains=query)|Q(Amount__icontains=query)|Q(Parts_Image__icontains=query)|Q(Description__icontains=query))
    else:
        forms5=Parts.objects.all()
    return render(request,'techpartsview.html',{'forms5':forms5,'c':c})

def payment(request, id, qq):
    technician_id = request.session.get('techinician_id')
    u_data = get_object_or_404(Technician, loginid=technician_id)
    ordid = get_object_or_404(Order, id=id)
    
    try:
        quantity = int(qq)
    except ValueError:
        messages.error(request, "Invalid quantity received.")
        return redirect('orderview')  # Or some error fallback page

    unit_price = int(ordid.partsid.Amount)
    total_amount = quantity * unit_price

    if request.method == 'POST':
        forms4 = PaymentForm(request.POST)
        if forms4.is_valid():
            payment_obj = forms4.save(commit=False)
            payment_obj.technicianid = u_data
            payment_obj.amount = total_amount  # if your model has amount field
            payment_obj.save()

            ordid.p_status = '1'
            ordid.Total_Amount=total_amount
            ordid.save()

            return redirect('paystoreview')
    else:
        forms4 = PaymentForm()

    return render(request, 'payment.html', {
        'forms4': forms4,
        'amt': unit_price,
        'quantity': quantity,
        'total': total_amount
    })


from django.contrib import messages

def orderview(request, id, c):
    cc = get_object_or_404(Parts, id=id)
    book = get_object_or_404(Booking, id=c)
    technician_id = request.session.get('techinician_id')
    u_data = get_object_or_404(Technician, loginid=technician_id)

    if request.method == 'POST':
        qq = request.POST.get('Quantity')
        print("Received Quantity:", qq)

        try:
            buy_qn = int(qq)
            if buy_qn <= 0:
                raise ValueError("Quantity must be positive")
        except (TypeError, ValueError):
            messages.error(request, "Invalid quantity input. Please enter a positive number.")
            return render(request, 'orderview.html', {'c': cc, 'u_data': u_data})

        if cc.Quantity < buy_qn:
            messages.error(request, f"Only {cc.Quantity} items are available in stock.")
            return render(request, 'orderview.html', {'c': cc, 'u_data': u_data})

        # Create the order
        d = Order.objects.create(
            technicianid=u_data,
            partsid=cc,
            p_status=0,
            c_status=0,
            r_status=0,
            bookin_id=book,

        )

        cc.Quantity -= buy_qn
        cc.save()

        return redirect('payorder', d.id, buy_qn)  # Passing quantity as integer

    return render(request, 'orderview.html', {'c': cc, 'u_data': u_data})

    
def paystoreview(request):
    loid=request.session.get('store_id')
    tech_id = get_object_or_404(Shop,loginid = loid)
    store=Order.objects.filter(partsid__store_id=tech_id,p_status=1)
    return render(request,'paystoreview.html',{'forms5':store})

def tech_order_view(request,id):
    loid=request.session.get('techinician_id')
    tech_id = get_object_or_404(Technician,loginid = loid)
    book=get_object_or_404(Booking,id=id)
    store1 = Order.objects.filter(bookin_id=book,technicianid=tech_id,p_status=1)
    return render(request,'ordersview_tech.html',{'forms5':store1})
    
def userstoreview(request,id):
    a=request.session.get('user_id')
    # tech_id = get_object_or_404(User,loginid=a)
    book=get_object_or_404(Booking,id=id)
    store=Order.objects.filter(bookin_id=book,p_status=1)
    return render(request,'userstoreview.html',{'forms5':store})

def cancelled(request, id):
    order = get_object_or_404(Order, id=id)
    order.c_status = 1
    order.save()
    return redirect('tech_order', id=order.bookin_id.id)  # Pass Booking ID



def refund(request, id):
    technician_id = request.session.get('techinician_id')
    u_data = get_object_or_404(Technician, loginid=technician_id)
    order = get_object_or_404(Order, id=id)

    # Parse amount safely
    try:
        unit_price = int(order.partsid.Amount)
    except (ValueError, TypeError):
        messages.error(request, "Invalid part price.")
        return redirect('tech_order', technician_id)

    # Calculate quantity from Total_Amount if not saved explicitly
    quantity = order.Total_Amount // unit_price if order.Total_Amount else 1
    total_amount = unit_price * quantity

    # ✅ Prevent multiple refunds
    if order.r_status == 1:
        messages.warning(request, "This order was already refunded.")
        return redirect('tech_order', technician_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            refund_obj = form.save(commit=False)
            refund_obj.technicianid = u_data
            refund_obj.amount = total_amount
            refund_obj.save()

            # ✅ Update refund status
            order.r_status = 1
            order.save()

            # ✅ Restore quantity in the parts table
            part = order.partsid
            part.Quantity += quantity
            part.save()

            messages.success(request, f"Refund completed. {quantity} items returned to stock.")
            return redirect('paystoreview')
    else:
        form = PaymentForm()

    return render(request, 'payment.html', {
        'forms4': form,
        'amt': unit_price,
        'quantity': quantity,
        'total': total_amount
    })


def chat(request, id):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')  # Handle unauthorized access

    user = get_object_or_404(Login, id=user_id)
    technician = get_object_or_404(Login, id=id)
    tech =get_object_or_404(Technician,loginid=technician)

    # Get all messages between user and technician
    chat_history = Chat.objects.filter(
        Q(senderid=user, recieverid=technician) |
        Q(senderid=technician, recieverid=user)
    ).order_by('currentdate')

    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.senderid = user
            chat.recieverid = technician
            chat.save()
            return redirect('chat', id=id)
    else:
        form = ChatForm()

    return render(request, 'chat.html', {
        'form': form,
        'ch': chat_history,
        'tech':tech
    })


def tech_chat(request, id):
    technician_id = request.session.get('techinician_id')  # Check session key spelling

    if not technician_id:
        return redirect('login')  # Or handle unauthorized access

    technician = get_object_or_404(Login, id=technician_id)
    user= get_object_or_404(Login,id=id)
    userdata=get_object_or_404(User,loginid=user)

    # Correct query using Q for bidirectional chat
    chat_history = Chat.objects.filter(
        Q(senderid=technician, recieverid=user) |
        Q(senderid=user, recieverid=technician)
    ).order_by('currentdate')

    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.senderid = technician
            chat.recieverid = user
            chat.save()
            return redirect('tech_chat', id=id)
    else:
        form = ChatForm()

    return render(request, 'tech_chat.html', {'form': form, 'ch': chat_history ,'user':userdata})

from django.db.models import Prefetch

def techchat_profile(request):
    technician_id = request.session.get('techinician_id')
    if not technician_id:
        return redirect('login')

    technician = get_object_or_404(Login, id=technician_id)

    # Get all unique sender Login IDs
    sender_login_ids = Chat.objects.filter(recieverid=technician)\
                                   .values_list('senderid', flat=True).distinct()

    # Get (Login, User) pairs using select_related
    senders = User.objects.select_related('loginid').filter(loginid__in=sender_login_ids)

    return render(request, 'techchat_profile.html', {'senders': senders})

def usertechpay_notify(request,id):
    bo2=get_object_or_404(Booking,id=id)
    bo2.pa_status=1
    bo2.save()
    return redirect('tech_status',id)

def tracking(request, id):
    booking = get_object_or_404(Booking, id=id)

    steps = {
        'ongoing': True,
        'tracked': True,
        'onroad': booking.on_status == 1,
        'work_in_progress': booking.t_status == 1,
        'completed': booking.pa_status == 1,
    }

    # Determine progress percentage
    if steps['completed']:
        progress = 100
    elif steps['work_in_progress']:
        progress = 80
    elif steps['onroad']:
        progress = 60
    else:
        progress = 40

    return render(request, 'tracking.html', {'steps': steps, 'progress': progress})


def tech_status(request,id):
    c=get_object_or_404(Booking,id=id)
    return render(request,'tech_status.html',{'c':c})

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
    return redirect('login')

def complaint(request,id):
    a=request.session.get('user_id')
    u_data=get_object_or_404(User,loginid=a)
    b_data=get_object_or_404(Technician,id=id)
    if request.method=='POST': 
        forms4=ComplaintForm(request.POST)
        if forms4.is_valid(): 
            a=forms4.save(commit=False)
            a.technicianid=b_data
            a.user_id=u_data
            a.save()
            return redirect('complaintview')
    else:
        forms4=ComplaintForm()
    return render(request,'complaint.html',{'forms4':forms4})

def complaintview(request):
    loid=request.session.get('user_id')
    user_id=get_object_or_404(User,loginid=loid)
    forms4=Complaint.objects.filter(user_id=user_id)
    return render(request,'complaintview.html',{'forms4':forms4})

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

def admincomplaintreply(request,id):
    comp=get_object_or_404(Complaint,id=id)
    if request.method=='POST':
        re=request.POST.get('reply')
        comp.reply=re
        comp.save()
        return redirect('adminviewcomplaint')
    return render(request,'admincomplaintreply.html')

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

def userpay(request, id):  # id = Booking ID
    booking = get_object_or_404(Booking, id=id)
    technician = booking.technicianid
    technician_orders = Order.objects.filter(bookin_id=booking, technicianid=technician, p_status=1,r_status=0)
    parts_amount = sum(order.Total_Amount for order in technician_orders)

    # 💼 Technician service fee (already set)
    service_fee = 500

    # 💰 Final total to be paid by the user
    total_to_pay = parts_amount + service_fee

    # ✅ Update the booking model fields before rendering
    booking.parts_amount = parts_amount
    booking.book_amount = service_fee
    booking.book_amount = booking.book_amount or 0  # fallback if somehow still None
    booking.save()

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.technicianid = technician
            payment.amount = total_to_pay
            payment.save()

            # ✅ Mark as paid
            booking.pa_status = 1
            booking.co_status = 1
            booking.TotalAmount=total_to_pay
            booking.save()

            messages.success(request, "Payment successfully made to the technician.")
            return redirect('bookingviewuser')  # Or your actual dashboard URL
    else:
        form = PaymentForm(initial={'amount': total_to_pay})

    return render(request, 'userpay.html', {
        'form': form,
        'booking': booking,
        'technician': technician,
        'parts_amount': parts_amount,
        'book_amount': service_fee,
        'total': total_to_pay
    })
















       











    
    









    





















# Create your views here.