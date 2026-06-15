from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.ControlUsers)
class UserAdmin(admin.ModelAdmin):
    list_display=('email','first_name','last_name','email','phon','slug')
    list_display_links=('email',)
    list_editable=('phon',)
    search_fields=('first_name','last_name' )
    readonly_fields=('slug',)
    list_filter=('email',)
    list_per_page=15

admin.site.register(models.UserProfile)

admin.site.register(models.Post)
class RegisterAdmin(admin.ModelAdmin):
    list_display=('first_name','last_name','email','age','phon', 'password')
    list_display_links=('email',)
    search_fields=('first_name','last_name' )
    list_filter=('email',)
    list_per_page=15
class RitsepAdmin(admin.ModelAdmin):
    list_display=('title','author','craeted_at')
    list_display_links=('title',)
    search_fields=('title','content' )
    readonly_fields=('slug',)
    list_filter=('author',)
    list_per_page=15


class PostAdminn(admin.ModelAdmin):
    list_display=('title','author','craeted_at')
    list_display_links=('title',)
    search_fields=('title','content' )
    readonly_fields=('slug',)
    list_filter=('author',)
    list_per_page=15
    
admin.site.register(models.Comment)
admin.site.register(models.Likes)

