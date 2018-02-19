from django.db import models
#from djmoney.models.fields import MoneyField

class Commodity(models.Model):
    #link commodity to the cio selling it
    #CIO = models.ForeignKey('CIO', null=True, blank=True, on_delete=models.SET_NULL)
    
    GOOD_OR_SERVICE = (
    ('G', 'Good'),
    ('S', 'Service'),
    )
    
    g_or_s = models.CharField(max_length=1, choices=GOOD_OR_SERVICE, default='G')
    
    title = models.CharField(
        max_length=250,
        default='',
        verbose_name='Commodity Title'
    )
    
    #add the ability to have more than one picture later?
    picture = models.ImageField(upload_to='commodity_pics/', default='commodity_pics/noimage.jpg', blank=True, null=True)
    
    description = models.CharField(
        max_length=500,
        default='',
        verbose_name='Commodity Description',
        blank = False
    )
    
    quantity = models.IntegerField(
        default=1,
        verbose_name='Quatity of items to be sold or services to be offered'
    )
    
   # price = MoneyField(
#        decimal_places=2,
#        default=0,
#        default_currency='USD',
#        max_digits=11,
#)
    
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    date_posted = models.DateTimeField(
        auto_now_add=True, 
        blank=True
    )
    
    date_expires = models.DateTimeField()