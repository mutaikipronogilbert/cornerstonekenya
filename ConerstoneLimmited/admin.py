from django.contrib import admin
from .models import Validation, Inspection, Recipient, Inspector, CommercialDocument, ImportDocumentation, Shipment, Validate, TaxPayment, ThirdPartyFees, Transport, DeliveryOrder, DeliveryInvoice,Goods

class CornerstoneAdminArea(admin.AdminSite):
  site_header = 'Cornerstone Admin Area'
  site_title = 'Cornerstone Admin Area'
  index_title = 'Welcome to Cornerstone Admin Area'

cornerstone_admin = CornerstoneAdminArea(name='cornerstone')


from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import SimpleListFilter
from .models import Inspection

class ValidationChoicesFilter(SimpleListFilter):
    title = _('Validation Status')
    parameter_name = 'validation_status'

    def lookups(self, request, model_admin):
        return (
            ('P', _('Pending')),
            ('A', _('Approved')),
            ('F', _('Failed')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'P':
            return queryset.filter(inspection_result='P')
        elif self.value() == 'A':
            return queryset.filter(inspection_result='A')
        elif self.value() == 'F':
            return queryset.filter(inspection_result='F')

class InspectionAdmin(admin.ModelAdmin):
    list_display = ('inspection_id', 'goods', 'inspector', 'inspection_date', 'inspection_result')
    search_fields = ('goods__description', 'inspector__first_name')  
    date_hierarchy = 'inspection_date'
    list_filter = (ValidationChoicesFilter,)


class ValidationAdmin(admin.ModelAdmin):
    list_display = ('validation_id', 'form', 'validation_date', 'validated_by')
    search_fields = ['validation_id', 'validation_date', 'validated_by']  
    list_filter = (ValidationChoicesFilter,)
    date_hierarchy = 'validation_date'
    ordering = ('validation_date',)


# class InspectionAdmin(admin.ModelAdmin):
#     list_display = ('inspection_id', 'goods', 'inspector', 'inspection_date', 'inspection_result')
#     list_filter = ('')
#     search_fields = ('goods__description', 'inspector')
#     date_hierarchy = 'inspection_date'


admin.site.register(Inspection, InspectionAdmin)
admin.site.register(Goods)
admin.site.register(Recipient)
admin.site.register(Inspector)
admin.site.register(CommercialDocument)
admin.site.register(ImportDocumentation)
admin.site.register(Shipment)
admin.site.register(Validate)
admin.site.register(TaxPayment)
admin.site.register(ThirdPartyFees)
admin.site.register(Transport)
admin.site.register(DeliveryOrder)
admin.site.register(DeliveryInvoice)  

