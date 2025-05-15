from django.contrib import admin

# Register your models here.
from tasks.models import Collection, Task


class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug"]


admin.site.register(Task)
admin.site.register(Collection, MessageAdmin)
