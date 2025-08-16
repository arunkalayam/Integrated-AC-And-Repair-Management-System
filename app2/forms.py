from django import forms
from .models import *
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
        model = Technician
        fields = ['Technician_Name', 'District', 'City', 'Contact', 'latitude', 'longitude', 'location_name']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'location_name': forms.HiddenInput(),  # Optional
        }

# forms.py

from django import forms
from .models import Shop

class Store(forms.ModelForm):
    latitude = forms.FloatField(required=False, widget=forms.HiddenInput())
    longitude = forms.FloatField(required=False, widget=forms.HiddenInput())
    location_name = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Shop
        fields = ['Shop_name', 'Address', 'District', 'City', 'latitude', 'longitude', 'location_name']

class LoginForm(forms.Form):
    Email=forms.CharField(max_length=100)
    Password=forms.CharField(widget=forms.PasswordInput())
    
class EmailEdit(forms.ModelForm):
    class Meta:
        model=Login
        fields=['Email']


from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    Time = forms.ChoiceField(choices=[], label='Time Slot')  # Replaced TimeField with ChoiceField

    class Meta:
        model = Booking
        fields = ['Date', 'Time', 'Error_code', 'Error_img']
        widgets = {
            'Date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Pop time_choices from kwargs if passed by the view
        time_choices = kwargs.pop('time_choices', [])
        super().__init__(*args, **kwargs)

        # Populate the dropdown with available time slots
        self.fields['Time'].choices = time_choices
        self.fields['Time'].widget.attrs.update({'class': 'form-control'})

        self.fields['Error_img'].required = False
        self.fields['Error_code'].widget.attrs.update({'class': 'form-control'})
# 👈 Make the image optional

class FeedbackForm(forms.ModelForm):
    class Meta:
        model=Feedback
        fields=['Feedbacks','rating']
        widgets = {
            'Feedbacks': forms.TextInput(attrs={'placeholder': 'Enter text here'}),
            'rating': forms.HiddenInput()  # will be set manually from POST
        }

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

class DeliveryForm(forms.ModelForm):
    class Meta:
        model=Delivery
        fields=['Name','Contact','City','License_no']

# forms.py

from django import forms

class DeliveryAllotForm(forms.Form):
    delivery_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Select Delivery Time"
    )





        