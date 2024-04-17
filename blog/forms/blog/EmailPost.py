from django import forms
from ...models import  Comment

#formulario basico
class EmailPostFrom(forms.Form):
    name = forms.CharField(max_length=250)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(required=False, widget=forms.Textarea) 

#formulario aplificado
class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ("name","email","body",)
