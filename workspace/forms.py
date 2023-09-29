from core.models import News
from django import forms


class NewsForm(forms.ModelForm):

    class Meta:
        model = News
        fields = (
            'name',
            'image',
            'description',
            'content',
            'category',
            'tags',
            'is_published',
        )
        # exclude = ('author',)
        # fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': '7'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': '7'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.CheckboxSelectMultiple(),
        }