from django.contrib import admin

# Register your models here.
from .models import Product, Contact, Order, OrderUpdate,ProjectSetting,UserProfile
admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(OrderUpdate)
admin.site.register(ProjectSetting)
class UserProfileAdmin(admin.ModelAdmin):
	list_display=['user','country','image_tag']
	list_filter=['user',]

admin.site.register(UserProfile,UserProfileAdmin)
