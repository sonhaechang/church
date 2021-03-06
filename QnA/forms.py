from django import forms
from QnA.models import QnA, QnAComment
from django.utils.translation import gettext_lazy as _
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

class QnAForm(forms.ModelForm):
    content = forms.CharField(widget=SummernoteWidget())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_fields = ['title', 'content']
        for field_name in class_update_fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })

        self.fields['title'].label = _('제목')
        self.fields['content'].label = _('내용')

    class Meta:
        model = QnA
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = QnAComment
        fields = ['comment']

        widgets = {
            'comment': forms.Textarea(
                attrs={
                    'id': 'add-comment',
                    'class': 'form-control comment',
                    'placeholder': '댓글 달기...',
                    'rows': "3",
                    'cols': "100",
                }
            )
        }
