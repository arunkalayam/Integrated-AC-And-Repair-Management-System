from django import forms
from .models import User,Login,Technician,Shop,Booking,Feedback,Parts,Payment,Order,Chat,Complaint
class UserLogin(forms.ModelForm):
    class Meta:
        model=Login
        fields=['Email','Password']

class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['Name','Contact_no']

class UserTech(forms.ModelForm):
    class Meta:
        model=Technician
        fields=['Technician_Name','District','City','Contact']
class Store(forms.ModelForm):
    class Meta:
        model=Shop
        fields=['Shop_name','Address','District','City']

class LoginForm(forms.Form):
    Email=forms.CharField(max_length=100)
    Password=forms.CharField(widget=forms.PasswordInput())
    
class EmailEdit(forms.ModelForm):
    class Meta:
        model=Login
        fields=['Email']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['Date', 'Time']
        widgets = {
            'Date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'Time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

class FeedbackForm(forms.ModelForm):
    class Meta:
        model=Feedback
        fields=['Feedbacks']

class PartsForm(forms.ModelForm):
    class Meta:
        model=Parts
        fields=['Parts_name','Amount','Parts_Image','Description','Quantity']

class PaymentForm(forms.ModelForm):
    class Meta:
        model=Payment
        fields=['Name_on_card','Card_No','CVV','Expiry_date','amount']

class ChatForm(forms.ModelForm):
    class Meta:
        model=Chat
        fields=['message']

class ComplaintForm(forms.ModelForm):
    class Meta:
        model=Complaint
        fields=['complaint']

class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['Total_Amount']



        