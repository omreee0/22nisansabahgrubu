from django import forms
from .models import * 


class YorumForm(forms.ModelForm):
    class Meta:
        model = Yorum
        fields = ['text','rating']

    def __init__(self,*args ,**kwargs):
        super(YorumForm,self).__init__(*args,**kwargs)

        self.fields['text'].widget.attrs.update({
            'rows':4,
            'class':'form-control',
            'placeholder':'Yorumunuzu buraya yazın'
        })

        self.fields['rating'].widget.attrs.update({
            'min':1,
            'max':5,
            'class':'form-control',
            'placeholder':'Puanınızı seçin'
        })