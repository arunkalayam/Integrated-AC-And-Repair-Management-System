from django.db import models
class Login(models.Model):
    Email=models.CharField(max_length=100)
    Password=models.CharField(max_length=100)
    Usertype=models.CharField(max_length=100)
    status=models.IntegerField()

class User(models.Model):
    Name=models.CharField(max_length=100)
    Contact_no=models.CharField(max_length=100)
    loginid=models.OneToOneField('Login',on_delete=models.CASCADE,related_name='as_user')


class Technician(models.Model):
    Technician_Name=models.CharField(max_length=100)
    District=models.CharField(max_length=100)
    City=models.CharField(max_length=100)
    Contact=models.CharField(max_length=100)
    loginid=models.ForeignKey('Login',on_delete=models.CASCADE)



class Shop(models.Model):
    Shop_name=models.CharField(max_length=100)
    Address=models.CharField(max_length=100)
    District=models.CharField(max_length=100)
    City=models.CharField(max_length=100)
    loginid=models.ForeignKey('Login',on_delete=models.CASCADE)

class Booking(models.Model):
    Date=models.DateField()
    Time=models.TimeField()
    user=models.ForeignKey('User',on_delete=models.CASCADE)
    technicianid=models.ForeignKey('Technician',on_delete=models.CASCADE)
    status=models.IntegerField(default=0)
    tech_status=models.IntegerField(default=0)
    pa_status=models.IntegerField(default=0)
    on_status=models.IntegerField(default=0)
    t_status=models.IntegerField(default=0)
    TotalAmount=models.IntegerField(default=0)
    parts_amount=models.IntegerField(default=0)
    co_status=models.IntegerField(default=0)
    
   
class Feedback(models.Model):
    Feedbacks=models.CharField(max_length=100)
    user=models.ForeignKey('User',on_delete=models.CASCADE)
    technicianid=models.ForeignKey('Technician',on_delete=models.CASCADE)
    Cur_Date=models.DateField(auto_now_add=True)

class Parts(models.Model):
    Parts_name=models.CharField(max_length=100)
    Amount=models.CharField(max_length=100)
    Parts_Image=models.ImageField(upload_to='uploads/')
    Description=models.CharField(max_length=100)
    Quantity=models.IntegerField(max_length=100)
    cur_date=models.DateField(auto_now_add=True)
    store_id=models.ForeignKey('Shop',on_delete=models.CASCADE)

class Payment(models.Model):
    Name_on_card=models.CharField(max_length=100)
    Card_No=models.CharField(max_length=100)
    CVV=models.CharField(max_length=100)
    Expiry_date=models.CharField(max_length=100)
    technicianid=models.ForeignKey('Technician',on_delete=models.CASCADE)
    amount=models.CharField(max_length=100)
    curr_date=models.DateField(auto_now_add=True)

    
class Order(models.Model):
    partsid=models.ForeignKey('Parts',on_delete=models.CASCADE)
    technicianid=models.ForeignKey('Technician',on_delete=models.CASCADE)
    current_date=models.DateField(auto_now_add=True)
    p_status=models.IntegerField()
    c_status=models.IntegerField()
    r_status=models.IntegerField()
    bookin_id = models.ForeignKey('Booking', on_delete=models.CASCADE, null=True, blank=True)
    Total_Amount=models.IntegerField(default=0)




class Chat(models.Model):
    message=models.TextField()
    senderid=models.ForeignKey('Login',on_delete=models.CASCADE,related_name='send_chats')
    recieverid=models.ForeignKey('Login',on_delete=models.CASCADE,related_name='recieved_chat')
    currentdate=models.DateTimeField(auto_now_add=True)

class Complaint(models.Model):
    technicianid=models.ForeignKey('Technician',on_delete=models.CASCADE)
    complaint=models.TextField()
    user_id=models.ForeignKey('User',on_delete=models.CASCADE)
    reply=models.TextField(blank=True,null=True)
    cur_date=models.DateField(auto_now_add=True)

   









    