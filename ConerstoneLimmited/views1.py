from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.contrib.auth.models import User
from .forms import GoodsForm, ForeignSupplierForm, InspectorForm, InspectionForm, CommercialDocumentForm, ImportDocumentationFormForm, ValidationForm
from .models import Goods, ForeignSupplier, Inspector, Inspection, CommercialDocument, ImportDocumentationForm, Validation

def create_goods(request):
    if request.method == 'POST':
        form = GoodsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
        else:
            return HttpResponseBadRequest("Invalid form data")
    else:
        form = GoodsForm()

    return render(request, 'goods_form.html', {'form': form})

def create_foreign_supplier(request):
    if request.method == 'POST':
        form = ForeignSupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
        else:
            return HttpResponseBadRequest("Invalid form data")
    else:
        form = ForeignSupplierForm()

    return render(request, 'foreign_supplier_form.html', {'form': form})

def create_inspector(request):
    if request.method == 'POST':
        form = InspectorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
        else:
            return HttpResponseBadRequest("Invalid form data")
    else:
        form = InspectorForm()

    return render(request, 'inspector_form.html', {'form': form})

def create_inspection(request):
    if request.method == 'POST':
        form = InspectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
        else:
            return HttpResponseBadRequest("Invalid form data")
    else:
        form = InspectionForm()

    return render(request, 'inspection_form.html', {'form': form})

def create_commercial_document(request):
    if request.method == 'POST':
        form = CommercialDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_page')
        else:
            return HttpResponseBadRequest("Invalid form data")
    else:
        form = CommercialDocumentForm()

    return render(request, 'commercial_document_form.html', {'form': form})

def create_import_documentation_form(request):
    if request.method == 'POST':
        form = ImportDocumentationFormForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
        else:
            return HttpResponseBadRequest("Invalid form data")
    else:
        form = ImportDocumentationFormForm()

    return render(request, 'import_documentation_form_form.html', {'form': form})

def create_validation(request):
    if request.method == 'POST':
        form = ValidationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
        else:
            return HttpResponseBadRequest("Invalid form data")
    else:
        form = ValidationForm()

    return render(request, 'validation_form.html', {'form': form})

def view_dashboard(request):
    # Your dashboard view logic here
    return render(request, 'dashboard.html')

def edit_goods(request, goods_id):
    instance = get_object_or_404(Goods, id=goods_id)
    form = GoodsForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('success_page')
    return render(request, 'goods_form.html', {'form': form})

def delete_goods(request, goods_id):
    instance = get_object_or_404(Goods, id=goods_id)
    instance.delete()
    return redirect('success_page')

