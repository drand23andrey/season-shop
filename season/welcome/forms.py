# -*- coding: utf-8 -*-
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User



class LoginForm(forms.Form):

	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Логин'
		self.fields['password'].label = 'Пароль'

	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		if not User.objects.filter(username=username).exists():
			raise forms.ValidationError('Пользователь с данным логином не зарегистрирован в системе!')
		user = User.objects.get(username=username)
		if user and not user.check_password(password):
			raise forms.ValidationError('Неверный пароль!')

class RegistrationForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	password_check = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = [
			'username',
			'password',
			'password_check',
			'first_name',
			'last_name',
			'email',
		]

	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'Логин'
		self.fields['username'].help_text = 'Не более 150 символов. Только буквы, цифры и символы @/./+/-/_'
		self.fields['password'].label = 'Пароль'
		self.fields['password_check'].label = 'Повторите пароль'
		self.fields['first_name'].label = 'Имя'
		self.fields['last_name'].label = 'Фамилия'
		self.fields['email'].label = 'Ваша электронная почта*'


	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		password_check = self.cleaned_data['password_check']
		email = self.cleaned_data['email']
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError('Пользователь с данным логином уже зарегистрирован в системе!')
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Пользователь с данным почтовым адресом уже зарегистрирован!')
		if password != password_check:
			raise forms.ValidationError('Ваши пароли не совпадают! Попробуйте снова!')



class OrderForm(forms.Form):
	phone = forms.CharField()
	name = forms.CharField(required=False)
	comments = forms.CharField(widget=forms.Textarea, required=False)


	def __init__(self, *args, **kwargs):
		super(OrderForm, self).__init__(*args, **kwargs)
		self.fields['phone'].label = 'Телефон'
		self.fields['phone'].help_text = 'Пожалуйста, указывайте реальный номер телефона, по которому с Вами можно связаться'
			
		self.fields['name'].label = 'Ваше имя'
		self.fields['name'].help_text = 'Как к Вам обратиться? (Заполнять не обязательно)' 
				
		self.fields['comments'].label = 'Комментарии к заказу'
		self.fields['comments'].help_text = 'Здесь можно дополнить заказ товаром, не представленным на сайте, либо оставить сообщение менеджеру заказа'