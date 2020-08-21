from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic

from . import models, forms

from extensions import sms_services, jalali


class SignUpView(generic.CreateView):
    model = models.User
    form_class = forms.SignUpForm
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super(SignUpView, self).get_form_kwargs()
        if self.form_class:
            kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        user = form.save()
        sms_services.request_send_verify_sms(user)
        # login(self.request, user)
        return redirect('Accounting:verify')


class VerifyView(generic.FormView):
    success_url = 'Accounting:profile'
    form_class = forms.VerifyForm
    template_name = 'verify.html'

    def get(self, request, *args, **kwargs):
        return super(VerifyView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = request.session['username']
            verification_code = form.cleaned_data['verification_code']
            try:
                user = models.User.object.get(username=username, verification_code=verification_code)
            except models.User.DoesNotExist:
                user = None
            if user is not None:
                if user.is_active:
                    user.verification_code = ''
                    user.save()
                    messages.success(request, 'شما با موفقیت وارد سیستم شدید')
                    login(self.request, user)
                    return redirect('Accounting:profile')
                else:
                    user.is_active = True
                    user.verification_code = ''
                    user.save()
                    messages.success(request, 'حساب کاربری شما با موفقیت فعال گردید')
                    return redirect('Accounting:profile')
            else:
                messages.error(request, 'حساب کاربری ای با این مشخصات یافت نشد!')
                return redirect('Accounting:index')
        else:
            return self.form_invalid(form)


class ProfileView(LoginRequiredMixin, generic.FormView):
    template_name = 'profile.html'
    form_class = forms.ProfileForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        user = models.User.object.get(username=self.request.user.username)
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        initial['date_of_birth'] = user.date_of_birth
        initial['gender'] = user.gender
        return initial

    def get(self, request, *args, **kwargs):
        return super(ProfileView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = models.User.object.get(username=self.request.user.username)

            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.gender = request.POST.get('gender')
            user.date_of_birth = jalali.Persian(request.POST.get('date_of_birth')).gregorian_string("{}-{}-{}")

            user.save()

            messages.success(request, 'تغییرات با موفقیت ذخیره شد.')
            return redirect('Accounting:profile')
        else:
            return self.form_invalid(form)


class LoginView(generic.FormView):
    template_name = 'login.html'
    form_class = forms.LoginForm

    def get(self, request, *args, **kwargs):
        return super(LoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            try:
                user = models.User.object.get(username=form.cleaned_data.get('username'))
            except models.User.DoesNotExist:
                user = None

            if user is not None:
                self.request.session['username'] = user.username
                sms_services.request_send_verify_sms(user)
                return redirect('Accounting:verify')
            else:
                messages.error(request, 'حساب کاربری ای با این مشخصات یافت نشد!')
                return redirect('Accounting:index')
        else:
            return self.form_invalid(form)


class LogoutView(LoginRequiredMixin, generic.RedirectView):
    url = reverse_lazy('Accounting:index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
