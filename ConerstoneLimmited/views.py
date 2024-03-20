from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View, DetailView,ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login as auth_login
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse, FileResponse, HttpResponse ,HttpResponseForbidden
from .forms import GoodsForm, ForeignSupplierForm, CommercialDocumentForm,TransportForm ,TaxPaymentForm , ThirdPartyFeesForm           
from .models import Goods, ForeignSupplier, CommercialDocument,Transport,TaxPayment , Shipment,Activity,ThirdPartyFees
from django.contrib import messages
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import logout as auth_logout
from django.urls import reverse
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormMixin
import re
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator

class CustomLoginView(LoginView):
    def form_valid(self, form):
        user = form.get_user()
        messages.success(self.request, f'Welcome, {user.username}!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password. Please try again.')
        return super().form_invalid(form)
    def get_success_url(self):
    # Redirect to the desired URL after successful login
       return '/'



def home(request):
    # Fetch data from the Shipment model or any other relevant models
    shipments = Shipment.objects.all()  
    recent_activities = Activity.objects.order_by('-timestamp')[:5] 


    # Pass data to the template
    return render(request, 'index.html', {'shipments': shipments, 'recent_activities': recent_activities})

@login_required(login_url='/login/')
def logout(request):
   auth_logout(request)
   return redirect(reverse('login')) 


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        # Create a new user object and save it
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password1
        )

        # Log the user in
        auth_login(request, user)

        messages.success(
            request,
            'Account created successfully. You are now logged in.'
        )
        return redirect('login')  

    return render(request, 'signup.html')

def goods_list(request):
    # Retrieve goods that belong to the signed-in user
    user_goods = Goods.objects.filter(buyer=request.user)

    return render(request, 'goods_list.html', {'goods': user_goods})



class EditDeleteSupplierView(LoginRequiredMixin, View):
    login_url = '/login/'
    template_name = 'supplier_form.html'

    def get(self, request, supplier_id):
        supplier = get_object_or_404(ForeignSupplier, supplier_id=supplier_id)
        form = ForeignSupplierForm(instance=supplier)
        return render(request, self.template_name, {
            'form': form,
            'supplier': supplier
        })

    def post(self, request, supplier_id):
        supplier = get_object_or_404(ForeignSupplier, supplier_id=supplier_id)
        form = ForeignSupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
        else:
            return render(request,
                          'supplier_form.html', {
                              'form': form,
                              'supplier': supplier
                          },
                          status=400)


class DeleteSupplierView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, supplier_id):
        supplier = get_object_or_404(ForeignSupplier, supplier_id=supplier_id)
        return render(request, 'delete_supplier.html', {'supplier': supplier})

    def post(self, request, supplier_id):
        supplier = get_object_or_404(ForeignSupplier, supplier_id=supplier_id)
        supplier.delete()
        return redirect('supplier_list')


class CreateUpdateSupplierView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, supplier_id=None):
        if supplier_id:
            supplier = get_object_or_404(ForeignSupplier,
                                         supplier_id=supplier_id)
        else:
            supplier = None

        form = ForeignSupplierForm(instance=supplier)
        return render(request, 'supplier_form.html', {
            'form': form,
            'supplier': supplier
        })

    def post(self, request, supplier_id=None):
        if supplier_id:
            supplier = get_object_or_404(ForeignSupplier,
                                         supplier_id=supplier_id)
        else:
            supplier = None

        form = ForeignSupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
        else:
            return render(request,
                          'supplier_form.html', {
                              'form': form,
                              'supplier': supplier
                          },
                          status=400)

@login_required(login_url='/login/') 
class ViewSupplierDetailView(DetailView):
    model = ForeignSupplier
    template_name = 'view_supplier.html'
    context_object_name = 'supplier'
    pk_url_kwarg = 'supplier_id'




def supplier_list(request):
    suppliers = ForeignSupplier.objects.all()
    return render(request, 'supplier_list.html', {'suppliers': suppliers})



@login_required(login_url='/login/')
def create_goods(request):
    user = request.user 
    if request.method == 'POST':
        form = GoodsForm(user, request.POST)
        form.request = request  # Set the request attribute
        if form.is_valid():
            new_good = form.save()
            description = f"Created a new Good: {new_good.name}"
            activity = Activity.objects.create(user=user, description=description)
            activity.save()
            return redirect('goods_list')
        else:
            print(form.errors)
            return HttpResponseBadRequest("Invalid form data")
    else:
        form = GoodsForm(user=user)

    return render(request, 'goods_form.html', {'form': form})


@login_required(login_url='/login/')
def edit_goods(request, goods_id):
    goods = get_object_or_404(Goods, goods_id=goods_id)

    if request.method == 'POST':
        user = request.user 
        form = GoodsForm(user,request.POST, instance=goods)
        if form.is_valid():
            new_good = form.save()
           
            description = f"Created a new Good: {new_good.name}"  # Adjust based on your Good model fields
  
            activity = Activity.objects.create(user=user, description=description)
            activity.save()

            return redirect('goods_list')
        else:
            print(form.errors)
            return HttpResponseBadRequest("Invalid form data")
    else:
        form = GoodsForm(user=user)

    return render(request, 'goods_form.html', {'form': form})


@login_required(login_url='/login/')
def delete_goods(request, goods_id):
    goods = get_object_or_404(Goods, goods_id=goods_id)

    if request.method == 'POST':
        goods.delete()
        return redirect('goods_list')
    else:
        return HttpResponseNotAllowed(['POST'])


@login_required(login_url='/login/')
def view_goods(request, goods_id):
    goods = get_object_or_404(Goods, goods_id=goods_id)
    
    return render(request, 'goods_detail.html', {'goods': goods})

@login_required(login_url = '/login/')
def upload_document(request):
    if request.method == 'POST':
        form = CommercialDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document_id = form.cleaned_data['document_id']
            # goods = form.cleaned_data['goods']
            document_name = form.cleaned_data['document_name']
            document = form.cleaned_data['document']

            new_document = CommercialDocument(
                document_id=document_id,
                # goods_name= goods,
                document_name=document_name,
                document=document)
            new_document.save()

            messages.success(request, 'Document uploaded successfully.')
            return redirect('document_list')  # Redirect to success page
        else:
            # print(form.errors)
            messages.error(request, form.errors)
            return render(request,
                          'CommercialDoc.html', {'form': form},
                          status=400)
    else:
        form = CommercialDocumentForm()

    return render(request, 'CommercialDoc.html', {'form': form})

@login_required(login_url='/login/')
def delete_document(request, document_id):
    document = get_object_or_404(CommercialDocument, document_id=document_id)
    document.delete()
    messages.success(request, 'Document deleted successfully.')
    return HttpResponseRedirect('/documents/')  # Redirect to documents page

@login_required(login_url='/login/')
def update_document(request, document_id):
    document = get_object_or_404(CommercialDocument, document_id=document_id)
    if request.method == 'POST':
        form = CommercialDocumentForm(request.POST,
                                      request.FILES,
                                      instance=document)
        if form.is_valid():
            form.save()
            messages.success(request, 'Document updated successfully.')
            return redirect('document_list')  # Redirect to documents page
        else:
            print(form.errors)
            messages.error(request,
                           'Failed to update document. Please check the  .',
                           form.errors)
            return render(request,
                          'update_document.html', {
                              'form': form,
                              'document_id': document_id
                          },
                          status=400)
    else:
        form = CommercialDocumentForm(instance=document)

    return render(
        request, 'update_document.html', {
            'form': form,
            'document_id': document.document_id,
            'document_name': document.document_name,
            'document': document.document
        })

@login_required(login_url='/login/')
def get_document(request, document_id):
    document = get_object_or_404(CommercialDocument, document_id=document_id)
    # Here, you can construct the response data as needed for displaying or using the document details
    data = {
        'document_id': document.document_id,
        'document_name': document.document_name,
        # 'Document':document.document,
        # 'goods_name ' : document.goods_name,
    }
    return JsonResponse(data)

@login_required(login_url='/login/')
def document_list(request):
    documents = CommercialDocument.objects.all()
    return render(request, 'document_list.html', {'documents': documents})
@login_required(login_url='/login/')
def serve_document(request, filename):
    document_path = os.path.join(settings.MEDIA_ROOT, 'commercial_documents',
                                 filename)
    if os.path.exists(document_path):
        if filename.lower().endswith('.pdf'):
            # Return a PDF file response for direct download
            with open(document_path, 'rb') as document_file:
                response = FileResponse(document_file)
                response[
                    'Content-Disposition'] = 'attachment; filename="' + os.path.basename(
                        document_path) + '"'

                print(response)
                return response
        elif filename.lower().endswith('.docx'):
            # Redirect to the Office Online Viewer for preview
            office_viewer_url = 'https://view.officeapps.live.com/op/embed.aspx?src='
            return HttpResponse(
                f'<iframe src="{office_viewer_url}{document_path}" width="600px" height="400px"></iframe>'
            )
        else:
            # For other file types, provide a download link
            with open(document_path, 'rb') as document_file:
                response = FileResponse(document_file)
                response[
                    'Content-Disposition'] = f'attachment; filename="{filename}"'
                return response
    else:
        return HttpResponse("File not found", status=404)


#Trannsport views 

@login_required(login_url='/login/')
def create_transport(request):
    user = request.user
    if request.method == 'POST':
        form = TransportForm(user,request.POST)
        if form.is_valid():
            transport = form.save()
            messages.success(request, 'Transport created successfully.')
            return redirect('edit_transport', pk=transport.pk)
        else:
            messages.error(request, 'Invalid form submission. Please check the data.')
    else:
        form = TransportForm(user)

    return render(request, 'create_transport.html', {'form': form})

def edit_transport(request, pk):
    transport = get_object_or_404(Transport, pk=pk)
    user = request.user
    if request.method == 'POST':
        form = TransportForm(user,request.POST, instance=transport)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transport updated successfully.')
            return redirect('edit_transport', pk=pk)
        else:
            messages.error(request, 'Invalid form submission. Please check the data.')
    else:
        form = TransportForm(user,instance=transport)

    return render(request, 'edit_transport.html', {'form': form, 'transport': transport})

def delete_transport(request, pk):
    transport = get_object_or_404(Transport, pk=pk)

    if request.method == 'POST':
        transport.delete()
        messages.success(request, 'Transport deleted successfully.')
        return redirect('transport_list')

    return render(request, 'delete_transport.html', {'transport': transport})




def transport_list(request):
    # Step 1: Retrieve the goods that belong to the signed-in user
    user_goods = Goods.objects.filter(buyer=request.user)

    # Step 2: Filter the Transport objects based on the goods
    transports = Transport.objects.filter(goods__in=user_goods)

    return render(
        request,
        'transport_list.html',
        {'transports': transports}
    )


# third-party


@login_required
def tax_payment_list(request):
    # Only show tax payments belonging to the logged-in user
    tax_payments = TaxPayment.objects.filter(taxpayer=request.user)
    return render(request, 'tax_payment_list.html', {'tax_payments': tax_payments})

@login_required
def create_or_update_tax_payment(request, tax_id=None):
    user = request.user
    if tax_id:
        tax_payment = get_object_or_404(TaxPayment, tax_id=tax_id)

        # Check if the logged-in user has permission to edit this tax payment
        if request.user != tax_payment.taxpayer:
            return HttpResponseForbidden("You don't have permission to edit this tax payment.")
    else:
        tax_payment = None

    if request.method == 'POST':
        form = TaxPaymentForm(request.POST, instance=tax_payment,request =request)
        if form.is_valid():
            new_tax_payment = form.save(commit=False)
            new_tax_payment.taxpayer = request.user
            new_tax_payment.save()
            return redirect('tax_payment_list')
    else:
        form = TaxPaymentForm(user,instance=tax_payment,request=request)

    return render(request, 'create_or_update_tax_payment.html', {'form': form, 'tax_payment': tax_payment})

@login_required
def delete_tax_payment(request, tax_id):
    tax_payment = get_object_or_404(TaxPayment, tax_id=tax_id)

    # Check if the logged-in user has permission to delete this tax payment
    if request.user != tax_payment.taxpayer:
        return HttpResponseForbidden("You don't have permission to delete this tax payment.")

    if request.method == 'POST':
        tax_payment.delete()
        return redirect('tax_payment_list')

    return render(request, 'delete_tax_payment.html', {'tax_payment': tax_payment})


# third party fees


   

@login_required
def third_party_fees_list(request):
    third_party_fees_list = ThirdPartyFees.objects.filter(payer=request.user)
    return render(request, 'third_party_fee_list.html', {'third_party_fees_list': third_party_fees_list})


@login_required
def create_or_update_third_party_fee(request, third_party_fee_id=None):
    user =request.user
    if third_party_fee_id:
        third_party_fee = get_object_or_404(ThirdPartyFees, third_party_fee_id=third_party_fee_id)

        # Check if the logged-in user has permission to edit this third-party fee
        if request.user != third_party_fee.payer:
            raise PermissionDenied("You don't have permission to edit this third-party fee.")
    else:
        third_party_fee = None

    if request.method == 'POST':
        
        form = ThirdPartyFeesForm(user,request.POST, instance=third_party_fee , request =request)
        if form.is_valid():
            new_third_party_fee = form.save()
            new_third_party_fee.payer = request.user
            new_third_party_fee.save()
            messages.success(request, 'Third-Party Fee saved successfully.')
            return redirect('third_party_fees_list')
    else:
        form = ThirdPartyFeesForm(user,instance=third_party_fee ,request=request)

    return render(request, 'create_or_update_third_party_fee.html', {'form': form, 'third_party_fee': third_party_fee})


@login_required
def delete_third_party_fee(request, third_party_fee_id):
    third_party_fee = get_object_or_404(ThirdPartyFees, third_party_fee_id=third_party_fee_id)

    # Check if the logged-in user has permission to delete this third-party fee
    if request.user != third_party_fee.goods.user:
        return HttpResponseForbidden("You don't have permission to delete this third-party fee.")

    if request.method == 'POST':
        third_party_fee.delete()
        messages.success(request, 'Third-Party Fee deleted successfully.')
        return redirect('third_party_fees_list')

    return render(request, 'delete_third_party_fee.html', {'third_party_fee': third_party_fee})
