from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

# Create your models here.
class ProjectSetting(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),)
    
    title =models.CharField(max_length=200)
    keyword=models.CharField(max_length=200)
    description=models.TextField()
    address=models.CharField(max_length=200)
    phone=models.CharField(max_length=18)
    fax=models.CharField(blank=True,max_length=50)
    email=models.EmailField(blank=True,null=True,max_length=100)
    smptserver=models.CharField(max_length=100)
    smptemail=models.EmailField(blank=True,null=True,max_length=100)
    smptpassword=models.CharField(blank=True,max_length=50)
    smptport=models.CharField(blank=True,max_length=150)
    icon=models.ImageField(blank=True,null=True,upload_to='icon/')
    about_icon=models.ImageField(blank=True,null=True,upload_to='icon/')
    title_icon=models.ImageField(blank=True,null=True,upload_to='icon/')
    facebook=models.CharField(blank=True,max_length=100)
    instagram=models.CharField(blank=True,max_length=100)
    address=models.TextField()
    contact=models.TextField()
    reference=models.TextField()
    status=models.CharField(max_length=50,choices=STATUS)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    team1=models.ImageField(blank=True,null=True,upload_to='icon/')
    team2=models.ImageField(blank=True,null=True,upload_to='icon/')
    team3=models.ImageField(blank=True,null=True,upload_to='icon/')
    team4=models.ImageField(blank=True,null=True,upload_to='icon/')
    team5=models.ImageField(blank=True,null=True,upload_to='icon/')
    user=models.ImageField(blank=True,null=True,upload_to='icon/')


    def __str__(self):
        return self.title
        
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to='shop/images', default="")

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=111, default="")


    def __str__(self):
        return self.name+"\'s Product"





class OrderUpdate(models.Model):
    update_id=models.AutoField(primary_key=True)
    order_id=models.IntegerField(default="")
    update_desc=models.CharField(max_length=5000)
    timesetup=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."




class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(blank=True,max_length=20)
    address=models.CharField(blank=True,max_length=250)
    city=models.CharField(blank=True,max_length=25)
    country=models.CharField(blank=True,max_length=30)
    image=models.ImageField(blank=True,upload_to='user_img')

    def __str__(self):
        return self.user.username


    def user_name(self):
        return self.user.first_name+' '+ self.user.last_name+'['+self.user.username+']'

    def  image_tag(self):
        return mark_safe('<img src="{}" heights="50" width="50" />'.format(self.image.url))
    image_tag.short_description='Image'

    def imageUrl(self):
        if self.image:
            return self.image.url
        else:
            return ""










