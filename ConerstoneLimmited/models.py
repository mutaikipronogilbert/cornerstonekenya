from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import F
import datetime
import uuid


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=
        "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex],
                                    max_length=17,
                                    blank=True)
    address = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username


class Goods(models.Model):
    goods_id = models.CharField(max_length=20, unique=True)
    buyer = models.ForeignKey(User, on_delete =models.CASCADE)
    name = models.CharField(max_length=50, default=' ')
    price = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    description = models.TextField()
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    supplier = models.ForeignKey('ForeignSupplier', on_delete=models.CASCADE)
    inspection_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ForeignSupplier(models.Model):
    supplier_id = models.CharField(max_length=20, unique=True)
    contact_details = models.CharField(max_length=50)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    contact_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                r'^\+\d{1,20}$',
                'Enter a valid contact number starting with a + sign.'),
        ])

    def __str__(self):
        return self.name


class Recipient(models.Model):
    recipient_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    is_company = models.BooleanField(default=False)

    def __str__(self):
        return f"Recipient: {self.name} - Email: {self.email}"


class Inspector(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    inspector_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name} "


class Inspection(models.Model):
    VALIDATION_CHOICES = [('P', 'Pending'), ('A', 'Approved'), ('F', "Failed")]
    inspection_id = models.CharField(max_length=20, unique=True)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    inspector = models.ForeignKey(Inspector,
                                  on_delete=models.CASCADE,
                                  blank=False,
                                  null=False)
    inspection_date = models.DateField(auto_now_add=True)
    inspection_result = models.CharField(max_length=255,
                                         blank=False,
                                         null=False)
    inspection_result = models.CharField(max_length=255,
                                         blank=False,
                                         choices=VALIDATION_CHOICES)
    remarks = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return f"Inspection {self.inspection_id} - {self.goods}"


class CommercialDocument(models.Model):
    document_id = models.CharField(max_length=20, unique=True)
    # goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    document_name = models.CharField(max_length=20, unique=True)
    document = models.FileField(upload_to='commercial_documents/')

    def __str__(self):
        return f"Document {self.document_id} - {self.document_name}"


class ImportDocumentationForm(models.Model):
    form_id = models.CharField(max_length=20, unique=True)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    validation_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Form {self.form_id} - {self.goods}"


class Validation(models.Model):
    VALIDATION_CHOICES = [('P', 'Pending'), ('A', 'Approved'), ('F', "Failed")]
    validation_id = models.CharField(max_length=20, unique=True)
    validation_status = models.CharField(max_length=1,
                                         choices=VALIDATION_CHOICES)
    validation_date = models.DateField(auto_now=True)
    validated_by = models.CharField(max_length=100)

    def __str__(self):
        return f"Validation {self.validation_id} - {self.form}"


class ImportDocumentation(models.Model):
    document_id = models.CharField(max_length=20, unique=True)
    document = models.FileField(upload_to='commercial_documents/')


class Shipment(models.Model):
    SHIPMENT_CHOICES = [
        ('Sea', 'Sea Freight'),
        ('Air', 'Cargo Plane'),
        ('Road', 'Road Freight'),
        ('Rail', 'Rail Freight'),
    ]
    VALIDATION_CHOICES = [('Pending', 'Pending'), ('Aproved', 'Approved'),
                          ('Failed', "Failed")]
    shipment_id = models.CharField(max_length=20, unique=True)
    shipping_method = models.CharField(max_length=20, choices=SHIPMENT_CHOICES)
    port_of_loading = models.CharField(max_length=20)
    number_of_containers = models.PositiveIntegerField()
    port_of_discharge = models.CharField(max_length=20)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    shipper = models.ForeignKey(ForeignSupplier, on_delete=models.CASCADE)
    departure_date = models.DateField()
    arrival_date = models.DateField()
    shipment_status = models.CharField(max_length=20,
                                       choices=VALIDATION_CHOICES)

    def __str__(self):
        return f"Shipment {self.shipment_id} - {self.goods}"


class Validate(models.Model):
    validation_id = models.CharField(max_length=20, unique=True)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    validation_status = models.BooleanField(default=False)
    validation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Validation {self.validation_id} - {self.goods}"


class TaxPayment(models.Model):
    tax_id = models.CharField(max_length=20, unique=True)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateField()
    taxpayer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Tax payment of {self.amount} by {self.taxpayer.username}"


class ThirdPartyFees(models.Model):
    third_party_fee_id = models.CharField(max_length=20, unique=True)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payer = models.ForeignKey(User,  on_delete=models.CASCADE )
    def __str__(self):

        return self.description


class Transport(models.Model):

    transport_id = models.CharField(max_length=20, unique=True, editable=True)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    departure_date = models.DateField()
    arrival_date = models.DateField()
    transport_status = models.CharField(max_length=20)
    transport_type = models.CharField(max_length=20)
    transport_company = models.CharField(max_length=100)
    pickup_address = models.TextField()
    delivery_address = models.TextField()
    assigned_driver = models.CharField(max_length=50)
    supplier = models.ForeignKey(ForeignSupplier, on_delete=models.CASCADE)
    



    def generate_transport_id(self):
        current_date = datetime.datetime.now()
        month = current_date.strftime("%m")
        year = current_date.strftime("%Y")

        last_transport = Transport.objects.filter(
            transport_id__startswith=f"TR-{month}-{year}").order_by(
                '-transport_id').first()

        if last_transport:
            last_increment = int(last_transport.transport_id[-4:])
            new_increment = last_increment + 1
        else:
            new_increment = 1

        self.transport_id = f"TR-{month}-{year}-{new_increment:04d}"

    def __str__(self):
        return f"Transport {self.transport_id} - {self.goods}"
class DeliveryOrder(models.Model):
    DELIVERY_CHOICES = [
        ('D', 'Deliverd'),
        ('P', 'Pending'),
        ('I', 'Transit'),
    ]
    order_id = models.CharField(max_length=20, unique=True)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    shipper = models.ForeignKey(ForeignSupplier, on_delete=models.CASCADE)
    transporter = models.ForeignKey(Transport, on_delete=models.CASCADE)
    order_delivery_date = models.DateField(auto_now_add=True)
    delivery_address = models.TextField()
    recipient_name = models.CharField(max_length=100)
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_CHOICES)

    def __str__(self):
        return f"Delivery Order {self.order_id} - {self.goods}"


class DeliveryInvoice(models.Model):
    invoice_id = models.CharField(max_length=20, unique=True)
    invoice_date = models.DateField(auto_now_add=True)
    # goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    delivery_order = models.OneToOneField('DeliveryOrder',
                                          on_delete=models.CASCADE)
    tax_fee = models.ForeignKey(TaxPayment, on_delete=models.CASCADE)
    third_party_fees = models.ForeignKey('ThirdPartyFees',
                                         on_delete=models.CASCADE)
    goods_price = models.ForeignKey(Goods, on_delete=models.CASCADE)
    invoice_date = models.DateField()

    total_amount = models.DecimalField(max_digits=10,
                                       decimal_places=2,
                                       default=0)  # Default value set to 0
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)

    def calculate_total_amount(self):
        related_goods = self.goods_price
        total_tax_amount = TaxPayment.objects.filter(
            goods=related_goods).aggregate(
                total_amount=models.Sum('amount'))['total_amount'] or 0
        total_fees_amount = ThirdPartyFees.objects.filter(
            goods=related_goods).aggregate(
                total_amount=models.Sum('amount'))['total_amount'] or 0
        total_goods_price = related_goods.price if related_goods else 0
        total_amount = total_tax_amount + total_fees_amount + total_goods_price
        return total_amount

    def save(self, *args, **kwargs):
        self.total_amount = self.calculate_total_amount()
        super(DeliveryInvoice, self).save(*args, **kwargs)

    def __str__(self):
        return f"Delivery Invoice {self.invoice_id} - Order: {self.delivery_order.order_id}"


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user} - {self.activity_type}"


