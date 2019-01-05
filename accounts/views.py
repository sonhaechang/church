from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, get_user_model
from django.shortcuts import redirect, render, resolve_url
from accounts.forms import SignupForm, EditProfileForm, ProfileForm, LoginForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.forms import PasswordChangeForm
from accounts.models import Profile
from django.urls import reverse_lazy

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            django_login(request, user) # 로그인 처리
            return redirect(settings.LOGIN_URL)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html', {'form': form,})


def login(request):
    if request.method == 'POST':
        # 로그인 성공 후 이동할 URL. 주어지지 않으면 None
        next = request.GET.get('next')

        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Django의 auth앱에서 제공하는 login함수를 실행해 앞으로의 요청/응답에 세션을 유지한다
            django_login(request, user)
            # next가 존재하면 해당 위치로, 없으면 Post목록 화면으로 이동
            return redirect(next if next else 'profile')
        # 인증에 실패하면 login_form에 non_field_error를 추가한다
        form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다')
    else:
        form = LoginForm()
    return render(request, 'accounts/login_form.html', {'form': form})


@login_required
def profile(request):
    profile = Profile.objects.all()
    # args = {'user': request.user}
    return render(request, 'accounts/profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        pform = ProfileForm(request.POST, instance=request.user.profile)

        if form.is_valid() and pform.is_valid():
            form.save()
            pform.save()
            return redirect('/accounts/profile')
    else:
        form = EditProfileForm(instance=request.user)
        pform = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/edit_profile.html', {
        'form': form,
        'pform': pform,
    })


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


class MyPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('login')
    template_name = 'accounts/password_reset_form.html'
    # email_template_name = '...'

    def form_valid(self, form):
        messages.info(self.request, 'Your password change email has been sent.')
        return super().form_valid(form)


class MyPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('login')
    template_name = 'accounts/password_reset_confirm.html'
    # email_template_name = '...'

    def form_valid(self, form):
        messages.info(self.request, 'Your password has been successfully set.')
        return super().form_valid(form)
