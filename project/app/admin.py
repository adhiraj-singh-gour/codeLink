from django.contrib import admin
from .models import *

admin.site.register(Userregister)

@admin.register(Contact)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'number', 'created_at')
    search_fields = ('name', 'email', 'number')
    list_filter = ('created_at',)


class TagAdmin(admin.TabularInline):                   #  
    model = Tag                                        #  
class PrerequisiteAdmin(admin.TabularInline):          #  
    model = Prerequisite                               #                                    
class LearningAdmin(admin.TabularInline):              #
    model = Learning                                   #
class VideoAdmin(admin.TabularInline):                 #
    model = Video                                      #

class CourseAdmin(admin.ModelAdmin):
    inlines = [TagAdmin,PrerequisiteAdmin,LearningAdmin,VideoAdmin]

admin.site.register(Course,CourseAdmin)
admin.site.register(Video)
admin.site.register(UserCourse)
