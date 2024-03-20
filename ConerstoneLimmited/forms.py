from django import forms
# from .models import Goods, ForeignSupplier, Inspector, Inspection, CommercialDocument, ImportDocumentation, Validation, Recipient,
# Shipment,Validate, TaxPayment, ThirdPartyFees,Transport, DeliveryOrder,DeliveryInvoice
from .models import Validation, Inspection, Recipient, Inspector, CommercialDocument, ImportDocumentation, Shipment, Validate, TaxPayment, ThirdPartyFees, Transport, DeliveryOrder, DeliveryInvoice, Goods, ForeignSupplier
from bootstrap_datepicker_plus.widgets import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
import uuid
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User

# class GoodsForm(forms.ModelForm):
#     class Meta:
#         model = Goods
#         fields = '__all__'



# class GoodsForm(forms.ModelForm):
#     class Meta:
#         model = Goods
#         exclude = ['goods_id', 'buyer'] 



#     def __init__(self, user, *args, **kwargs):
#         super(GoodsForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_method = 'post'
#         self.helper.add_input(Submit('submit', 'Create'))
#         self.helper.layout = Layout(
#             Field('name', css_class='form-control-sm'),
#             Field('price', css_class='form-control-sm'),
#             Field('description', css_class='form-control-sm'),
#             Field('weight', css_class='form-control-sm'),
#             Field('quantity', css_class='form-control-sm'),
#             Field('supplier', css_class='form-control-sm'),
#         )
#         # Set the initial value of the buyer field
#         self.initial['buyer'] = user.id



class GoodsForm(forms.ModelForm):
    class Meta:
        model = Goods  # Make sure you specify the model
        exclude = ['goods_id', 'buyer'] 

    def __init__(self, user, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(GoodsForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Create'))
        self.helper.layout = Layout(
            Field('name', css_class='form-control-sm'),
            Field('price', css_class='form-control-sm'),
            Field('description', css_class='form-control-sm'),
            Field('weight', css_class='form-control-sm'),
            Field('quantity', css_class='form-control-sm'),
            Field('supplier', css_class='form-control-sm'),
        )

        if self.request and hasattr(self.request, 'user_id'):
            self.fields['buyer'] = forms.ModelChoiceField(
                queryset=User.objects.filter(username=user.username),
                widget=forms.HiddenInput(),
                initial=self.request.user
            )

    def clean(self):
        cleaned_data = super().clean()

    def save(self, commit=True):
        instance = super().save(commit=False)

        current_date = datetime.now()
        month_year_str = current_date.strftime('%b-%Y').upper()
        unique_id = str(uuid.uuid4().int)[:4].zfill(4)
        instance.goods_id = f'IMP-{month_year_str}-{unique_id}'

        # if self.request and hasattr(self.request, 'user_id'):
        instance.buyer = self.request.user

        if commit:
            instance.save()

        return instance




   
    
#     def clean(self):
#         cleaned_data = super().clean()
#         # cleaned_data['buyer'] = self.initial['buyer']  # Set the buyer to the logged-in user


#     def save(self, commit=True):
#         instance = super().save(commit=False)

#         # Generate goods_id using the desired format
#         current_date = datetime.now()
#         month_year_str = current_date.strftime('%b-%Y').upper()
#         unique_id = str(uuid.uuid4().int)[:4].zfill(4)  
#         instance.goods_id = f'IMP-{month_year_str}-{unique_id}'
        
#         # Set the buyer to the logged-in user if available
#         user = getattr(self, 'request', None)
#         if user and hasattr(user, 'user_id'):
#             instance.buyer = user
#         else:
#             raise ValueError("Request object or user information is missing.")

#         if commit:
#             instance.save()

#         return instance


class ForeignSupplierForm(forms.ModelForm):
    class Meta:
        model = ForeignSupplier
        fields = '__all__'


class InspectorForm(forms.ModelForm):
    class Meta:
        model = Inspector
        fields = '__all__'


class InspectionForm(forms.ModelForm):
    class Meta:
        model = Inspection
        fields = '__all__'


class CommercialDocumentForm(forms.ModelForm):
    class Meta:
        model = CommercialDocument
        fields = ['document_id', 'document_name', 'document']

    def clean_document_id(self):
        document_id = self.cleaned_data['document_id']
        # Example: Check if document_id is alphanumeric and has a specific length
        if not document_id.isalnum():
            raise forms.ValidationError(
                "Document ID should contain only alphanumeric characters.")
        if len(
                document_id
        ) < 8:  # Assuming the document_id should have a length of 8 characters
            raise forms.ValidationError(
                "Document ID should be 8 characters long.")
        return document_id

    def clean_document_name(self):
        document_name = self.cleaned_data['document_name']
        # Example: Ensure document_name is not empty and doesn't exceed a certain length
        if not document_name:
            raise forms.ValidationError("Document Name cannot be empty.")
        if len(
                document_name
        ) > 50:  # Assuming the maximum length of the document name should be 50 characters
            raise forms.ValidationError(
                "Document Name should not exceed 50 characters.")
        return document_name

    def clean_document(self):
        document = self.cleaned_data['document']
        # Example: Check if the uploaded document has a specific file extension
        allowed_extensions = ['pdf', 'docx',
                              'xlsx']  # Example allowed extensions
        if not document.name.lower().endswith(tuple(allowed_extensions)):
            raise forms.ValidationError(
                "Invalid file format. Allowed formats: PDF, DOCX, XLSX.")
        return document


class ImportDocumentationFormForm(forms.ModelForm):
    class Meta:
        model = ImportDocumentation
        fields = '__all__'


class ValidationForm(forms.ModelForm):
    class Meta:
        model = Validation
        fields = '__all__'


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = '__all__'


# class ImportDocumentationFormForm(forms.ModelForm):
#   class Meta:
#       model = ImportDocumentationForm
#       fields = '__all__'


class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = '__all__'


class ValidateForm(forms.ModelForm):
    class Meta:
        model = Validate
        fields = '__all__'


class TaxPaymentForm(forms.ModelForm):
    class Meta:
        model = TaxPayment
        fields = '__all__'


class ThirdPartyFeesForm(forms.ModelForm):
    class Meta:
        model = ThirdPartyFees
        fields = '__all__'




class TransportForm(forms.ModelForm):
    TRANSPORT_CHOICES = [
        ('Sea', 'Sea Freight'),
        ('Air', 'Cargo Plane'),
        ('Road', 'Road Freight'),
        ('Rail', 'Rail Freight'),
    ]
    TRANSPORT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('OnTransit', 'Transit'),
        ('Delivered', 'Delivered'),
    ]

    transport_type = forms.ChoiceField(choices=TRANSPORT_CHOICES)
    transport_status = forms.ChoiceField(choices=TRANSPORT_STATUS_CHOICES)
    departure_date = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'))
    arrival_date = forms.DateField(widget=DatePickerInput(format='%Y-%m-%d'))

    class Meta:
        model = Transport
        exclude = ['transport_id']  # Exclude the non-editable field

    def __init__(self,user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Create'))
        self.helper.layout = Layout(
            Field('goods'),
            Field('departure_date'),
            Field('arrival_date'),
            Field('transport_status'),
            Field('transport_type'),
            Field('transport_company'),
            Field('pickup_address', rows=2),
            Field('delivery_address', rows=1),
            Field('assigned_driver'),
            Field('supplier'),
        )
        self.fields['goods'].queryset = self.fields['goods'].queryset.filter(buyer=user)

    def clean(self):
        cleaned_data = super().clean()
        departure_date = cleaned_data.get('departure_date')
        arrival_date = cleaned_data.get('arrival_date')

        if departure_date and arrival_date and departure_date >= arrival_date:
            raise forms.ValidationError("Arrival date must be greater than departure date.")

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Generate transport_id using the desired format
        current_date = datetime.now()
        month_year_str = current_date.strftime('%b-%Y').upper()
        unique_id = str(uuid.uuid4().int)[:4].zfill(4)  
        instance.transport_id = f'TR-{month_year_str}-{unique_id}'

        if commit:
            instance.save()

        return instance



# forms.py


class TaxPaymentForm(forms.ModelForm):
    class Meta:
        model = TaxPayment
        fields = ['goods', 'amount', 'date_paid']
        widgets = {
            'date_paid': DatePickerInput(format='%Y-%m-%d'),
        }

    def __init__(self,user, *args, **kwargs):
        self.request =kwargs.pop('request',None)
        super(TaxPaymentForm,self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

        self.fields['goods'].queryset = self.fields['goods'].queryset.filter(buyer=user)

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')

        # Validate that the amount is positive
        if amount and amount <= 0:
            raise forms.ValidationError('Amount must be a positive number.')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.taxpayer =self.request.user
        # Generate tax_id using the desired format
        current_date = datetime.now()
        day_month_str = current_date.strftime('%d-%b').upper()
        unique_id = str(uuid.uuid4().int)[:4].zfill(4)
        instance.tax_id = f'TX-{day_month_str}-{unique_id}'

        # Set the taxpayer as the logged-in user
        instance.taxpayer = self.request.user

        if commit:
            instance.save()

        return instance


# third party fee

class ThirdPartyFeesForm(forms.ModelForm):
    class Meta:
        model = ThirdPartyFees
        fields = ['goods', 'description', 'amount']

    def __init__(self,user, *args, **kwargs):
        self.request =kwargs.pop('request',None)
        super(ThirdPartyFeesForm,self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
        self.helper.layout = Layout(
            Field('goods'),
            Field('description'),
            Field('amount'),
        )
        self.fields['goods'].queryset = self.fields['goods'].queryset.filter(buyer=user)

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')

        # Add custom cleaning logic if needed
        if amount and amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.payer =self.request.user
        # Generate third_party_fee_id using the desired format
        current_date = timezone.now()
        year_month_str = current_date.strftime('%Y-%b').upper()
        unique_id = str(uuid.uuid4().int)[:4].zfill(4)
        instance.third_party_fee_id = f'TPF-{year_month_str}-{unique_id}'
         # Set the feepayer as the logged-in user
        instance.payer = self.request.user      

        if commit:
            instance.save()

        return instance
    


class DeliveryOrderForm(forms.ModelForm):
    class Meta:
        model = DeliveryOrder
        fields = '__all__'


class DeliveryInvoiceForm(forms.ModelForm):
    class Meta:
        model = DeliveryInvoice
        fields = '__all__'
