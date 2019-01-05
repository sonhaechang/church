from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from accounts.models import Profile
from django.utils.translation import gettext_lazy as _

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'baptism', 'phone_number', 'birthday']
        for field_name in class_update_fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })

        self.fields['username'].label = _('아이디')
        self.fields['password1'].label = _('비밀번호')
        self.fields['baptism'].label = _('세례명')
        self.fields['phone_number'].label = _('전화번호')
        self.fields['birthday'].label = _('생년월일')
        self.fields['email'].help_text = _('비밀번호 분실시 필요하니 정확히 입력해주세요.')
        self.fields['birthday'].help_text = _('생년월일 (8자리 입력. 예 : 19680523)')
        self.fields['phone_number'].help_text = _('전화번호 ("-" 없이 11자리 입력해주세요.)')


    baptism = forms.CharField()
    phone_number = forms.CharField()
    birthday = forms.CharField()

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('last_name', 'first_name', 'email',)

    def save(self):
        user = super().save()
        profile = Profile.objects.create(
            user = user,
            baptism = self.cleaned_data['baptism'],
            phone_number = self.cleaned_data['phone_number'],
            birthday = self.cleaned_data['birthday'])
        return user


    # def clean_email(self):
    #     email = self.cleaned_data.get('email', '')
    #     if email:
    #         if get_user_model().objects.filter(email=email).exists():
    #             raise form.ValidationError('duplicated email')
    #         return email


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_fields = ['username', 'password']
        for field_name in class_update_fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['username'].label = _('아이디')
        self.fields['password'].label = _('비밀번호')



class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_fields = ['baptism', 'phone_number', 'birthday']
        for field_name in class_update_fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['baptism'].label = _('세례명')
        self.fields['birthday'].label = _('생년월일')
        self.fields['phone_number'].label = _('전화번호')

    class Meta:
        model = Profile
        fields = ['baptism', 'birthday', 'phone_number']


class EditProfileForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_fields = ['password', 'first_name', 'last_name', 'email']
        for field_name in class_update_fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = User
        fields = ['password', 'first_name', 'last_name', 'email']
