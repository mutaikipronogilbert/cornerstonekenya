from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from django.urls import path
from . import views as views
from .views import (
    CreateUpdateSupplierView,
    EditDeleteSupplierView,
    DeleteSupplierView,
    ViewSupplierDetailView,
    logout,
    CustomLoginView
)
from .models import TaxPayment, ThirdPartyFees
from .forms import TaxPaymentForm, ThirdPartyFeesForm
urlpatterns = [
    path('', views.home, name='home'),
    path('goods', views.goods_list, name='goods_list'),
    path('goods/create', views.create_goods, name='create_goods'),
    path('goods/<str:goods_id>/', views.view_goods, name='view_goods'),
    path('goods/<str:goods_id>/edit/', views.edit_goods, name='edit_goods'),
    path('goods/<str:goods_id>/delete/',
         views.delete_goods,
         name='delete_goods'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('suppliers/create/',
         CreateUpdateSupplierView.as_view(),
         name='create_foreign_supplier'),
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/<str:supplier_id>/',
         EditDeleteSupplierView.as_view(),
         name='edit_delete_foreign_supplier'),
    path('suppliers/<str:supplier_id>/delete/',
         DeleteSupplierView.as_view(),
         name='delete_foreign_supplier'),
    path('suppliers/view/<str:supplier_id>/',
         ViewSupplierDetailView,
         name='view_foreign_supplier'),
    path('suppliers/<str:supplier_id>/update/',
         CreateUpdateSupplierView.as_view(),
         name='update_foreign_supplier'),
    path('upload/', views.upload_document, name='upload_document'),
    path('document/<str:document_id>/delete/',
         views.delete_document,
         name='delete_document'),
    path('document/<str:document_id>/update/',
         views.update_document,
         name='update_document'),
    path('document/<str:document_id>/',
         views.get_document,
         name='get_document'),
    path('documents/', views.document_list, name='document_list'),
    path('documents/<path:filename>/', views.serve_document,
         name='serve_document'),
#transport
      path('transport/create/', views.create_transport, name='create_transport'),
      path('transport/<int:pk>/edit/', views.edit_transport, name='edit_transport'),
      path('transport/<int:pk>/delete/', views.delete_transport, name='delete_transport'),  
         path('transport/list/', views.transport_list, name='transport_list'),
#tax

    path('tax-payments/', views.tax_payment_list, name='tax_payment_list'),
    path('tax-payment/create/', views.create_or_update_tax_payment, name='create_tax_payment'),
    path('tax-payment/<str:tax_id>/edit/', views.create_or_update_tax_payment, name='edit_tax_payment'),
    path('tax-payment/<str:tax_id>/delete/', views.delete_tax_payment, name='delete_tax_payment'),
# third party fee

    path('third-party-fees/list/', views.third_party_fees_list, name='third_party_fees_list'),
    path('third-party-fees/create/', views.create_or_update_third_party_fee, name='create_third_party_fee'),
    path('third-party-fees/<str:third_party_fee_id>/edit/', views.create_or_update_third_party_fee,
         name='edit_third_party_fee'),
    path('third-party-fees/<str:third_party_fee_id>/delete/', views.delete_third_party_fee,
         name='delete_third_party_fee'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
