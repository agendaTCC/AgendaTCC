from django.contrib import admin
from django.conf import settings
from models import Splash, Imagens

class ImagensAdmin(admin.TabularInline):
    model = Imagens
    
class SplashAdmin(admin.ModelAdmin):
    inlines = [ImagensAdmin,]
    class Media:
        js = ['/media/js/tiny_mce/tiny_mce.js', '/media/js/textareas.js']
    
    
    
admin.site.register(Splash,SplashAdmin)