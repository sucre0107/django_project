import random
from app1.utils.encrypt import md5
from app1.models import Administrator, Customer
from django.shortcuts import render, redirect, HttpResponse, reverse, HttpResponseRedirect, Http404
from django.middleware.csrf import get_token

# 利用django进行表单验证
from django import forms
from django.core.exceptions import ValidationError
from django.forms import widgets

# 1.定义类,继承forms.Form,
class LoginForm(forms.Form):
    role = forms.ChoiceField(
        required=True,  # 此处默认为True，如果不写，那么就是在form中就是必填项
        choices=(("2", "客户"), ("1", "管理员")),  # 在html标签中 2 是value, 客户是显示的内容，1是value，管理员是显示的内容
        # 添加正则表达式，要求含有英文字母和数字，且长度为6-12位
        # widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "用户名", "pattern": "[a-zA-Z0-9]{6,12}"})
        widget=forms.Select(attrs={
            "class": "w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline",
            "placeholder": "用户名"})
    )
    username = forms.CharField(
        required=True,
        # 添加正则表达式，要求含有英文字母和数字，且长度为6-12位
        validators=[],
        widget=forms.TextInput(attrs={
            "class": "w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline",
            "placeholder": "用户名"})
    )
    password = forms.CharField(
        required=True,
        # 添加正则表达式，要求含有英文字母,英文标点符号或者下划线和数字，且长度为6-12位
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline",
            "placeholder": "密码", "pattern": "[a-zA-Z0-9_.,？]{6,12}"}, render_value=True)
    )  # render_value=True,即使我们输错密码，先前输入的密码仍然会显示在输入框中

    # 自定义字段的校验规则
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError('用户名不能为空')
        return username

    def clean_password(self):
        # 预先对密码进行加密，视图函数中的加密就可以省略了
        password = md5(self.cleaned_data.get('password'))
        if not password:
            raise ValidationError('密码不能为空')
        return password


class SmsFormLogin(forms.Form):
    role = forms.ChoiceField(
        required=True,  # 此处默认为True，如果不写，那么就是在form中就是必填项
        choices=(("2", "客户"), ("1", "管理员")),  # 在html标签中 2 是value, 客户是显示的内容，1是value，管理员是显示的内容
        widget=forms.Select(attrs={
            "class": "w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline"})
    )
    mobile = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            # "id": "mobile_nums",
            "class": "w-full px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline",
            "placeholder": "手机号码",
            "pattern": "[0-9]{11}"}
        )
    )

    sms_code = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "class": " px-3 py-2 text-sm leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline",
            "placeholder": "验证码",
            "pattern": "[0-9]{6}"}
        )
    )

    # 自定义字段的校验规则
    def clean_mobile_nums(self):
        mobile_nums = self.cleaned_data.get('mobile_nums')
        if not mobile_nums:
            raise ValidationError('手机号码不能为空')
        # 判断手机号码是否已经注册
        if self.cleaned_data.get('role') == '1':
            obj = Administrator.objects.filter(mobile_nums=mobile_nums).first()
        else:
            obj = Customer.objects.filter(mobile_nums=mobile_nums).first()
        if not obj:
            raise ValidationError('手机号码未注册')

        return mobile_nums

    def clean_sms_code(self):
        sms_code = self.cleaned_data.get('sms_code')
        if not sms_code:
            raise ValidationError('验证码不能为空')
        return sms_code


def login(request):
    # 如果是get请求，直接返回登录页面
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {"form": form})
    form = LoginForm(data=request.POST)
    # 对表单进行格式校验
    if not form.is_valid():
        return render(request, 'login.html', {"form": form, 'error': form.errors})
    # 第一种获取方式
    # role = request.POST.get('role')
    # username = request.POST.get('username')
    # password = request.POST.get('password')

    # 第二种获取方式
    role = form.cleaned_data.get('role')
    username = form.cleaned_data.get('username')
    password = form.cleaned_data.get('password')

    print(username, password, role)
    # 格式校验成功，去数据库校验
    # 当登陆用户是管理员
    # if role == 'administer':
    #     obj = Administrator.objects.filter(active=1, username=username, password=password).first()
    #     if obj:
    #         return HttpResponse("管理员登录成功")
    #     else:
    #         return render(request, 'login.html', {'error': '用户名或密码错误'})
    # obj = Customer.objects.filter(active=1, username=username, password=password).first()
    # # 当登陆用户是用户
    # if obj:
    #     request.session['user_info'] = {'username': username, 'role': role, 'id': obj.id}
    # else:
    #     return render(request, 'login.html', {'error': '用户名或密码错误'})
    # return HttpResponse("用户登录成功")

    # 另外一种写法
    if role == '1':
        obj = Administrator.objects.filter(active=1).filter(**form.__dict__).first()
    else:
        obj = Customer.objects.filter(active=1).filter(**form.__dict__).first()
    if obj:
        if role == '1':
            request.session['user_info'] = {'username': username, 'role': role, 'id': obj.id}
            return HttpResponse("管理员登录成功")
        else:
            request.session['user_info'] = {'username': username, 'role': role, 'id': obj.id}
            return HttpResponse("用户登录成功")
    return render(request, 'login.html', {'error': '用户名或密码错误', 'form': form})


def login_sms(request):
    # 如果是get请求，直接返回登录页面
    if request.method == 'GET':
        form = SmsFormLogin()
        return render(request, 'login_sms.html', {"form": form})
    form = LoginForm(data=request.POST)
    # 对表单进行格式校验
    if not form.is_valid():
        return render(request, 'login_sms.html', {"form": form, 'error': form.errors})
    role = form.cleaned_data.get('role')
    mobile = form.cleaned_data.get('mobile')
    sms_code = form.cleaned_data.get('sms_code')
    print(mobile, sms_code, role)
    # 格式校验成功，去数据库校验
    # 当登陆用户是管理员
    if role == '1':
        obj = Administrator.objects.filter(mobile=mobile, sms_code=sms_code, active=1).first()
    else:
        obj = Customer.objects.filter(mobile=mobile, sms_code=sms_code, active=1).first()
    if obj:
        if role == '1':
            request.session['user_info'] = {'mobile': mobile, 'username': obj.username, 'role': role, 'id': obj.id}
            return HttpResponse("管理员登录成功")
        else:
            request.session['user_info'] = {'mobile': mobile, 'username': obj.username, 'role': role, 'id': obj.id}
            return HttpResponse("用户登录成功")
    return render(request, 'login_sms.html', {'error': '验证码或者手机号错误', 'form': form})


def send_sms_code(request):
    mobile_nums = request.GET.get('mobile_nums')
    print(mobile_nums)
    # 生成随机验证码
    # sms_code = random.randint(100000, 999999)
    # print(sms_code)
    sms_code = str(1234565) #测试用

    return HttpResponse("发送验证码成功")


def register(request):
    return render(request, 'register.html')
