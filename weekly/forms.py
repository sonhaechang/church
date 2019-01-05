from django import forms
from weekly.models import WeeklyComment


class CommentForm(forms.ModelForm):
    class Meta:
        model = WeeklyComment
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
