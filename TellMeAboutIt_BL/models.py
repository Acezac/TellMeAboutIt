from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm

class Complaint(models.Model):
    subject = models.CharField(max_length=128)
    reason = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    rating = models.IntegerField(default=0, blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
    numberComments = models.IntegerField(default=0, blank=True, null=True)

    def __unicode__(self):
        return self.subject



class Comment(models.Model):
    complaint = models.ForeignKey(Complaint)
    content = models.CharField(max_length=128)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.content

class Rating(models.Model):
    user = models.ForeignKey(User)
    complaint_id = models.IntegerField(default=0, blank=True, null=True)

    def __unicode__(self):
        return self.complaint_id


# create a form for Complain
class ComplaintForm(forms.ModelForm):
    subject = forms.CharField(widget=forms.TextInput)
    reason = forms.CharField(widget=forms.TextInput)
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        # associate the model, Category, with the ModelForm
        model = Complaint
        fields = ('subject', 'description','reason')

    def __init__(self, *args, **kwargs):
        super(ComplaintForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['subject'].widget.attrs['width'] = 3
        self.fields['subject'].widget.attrs['placeholder'] = 'Tell me about'
        self.fields['description'].widget.attrs['rows'] = 4
        self.fields['description'].widget.attrs['placeholder'] = 'Tell the world your experience'
        self.fields['description'].widget.attrs['style'] = 'resize: none'
        self.fields['reason'].widget.attrs['placeholder'] = 'What made you complain??'

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)
    # These fields are optional
    picture = models.ImageField(upload_to='imgs', blank=True)

    def __unicode__(self):
        return self.user.username


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'email', 'password']:
            self.fields[fieldname].help_text = None

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['picture']

