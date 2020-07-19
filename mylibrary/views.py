from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.db.models import Q
from mylibrary.models import User, Book, Borrow, Log
from mylibrary.forms import LoginForm, RegisterForm, SearchForm
from datetime import datetime, timedelta
import hashlib


class IndexView(View):
    """
    主页
    """
    def get(self, request):
        return redirect('/login/')


class LoginView(View):
    """
    登录
    """
    def get(self, request):
        if request.session.get('is_login', None):
            return redirect('/home/')
        login_form = LoginForm()
        return render(request, 'login.html', locals())

    def post(self, request):
        login_form = LoginForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            user_id = login_form.cleaned_data['user_id']
            password = login_form.cleaned_data['password']
            user = User.objects.filter(id=user_id).first()
            if user and user.password == hashcode(password, user_id):
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                Log.objects.create(user_id=user_id, action='登录')
                return redirect('/home/')
            else:
                message = '用户名或密码错误！'
        return render(request, 'login.html', locals())


class LogoutView(View):
    """
    登出
    """
    def get(self, request):
        if request.session.get('is_login', None):
            Log.objects.create(user_id=request.session['user_id'], action='登出')
            request.session.flush()
            messages.success(request, '登出成功！')
        return redirect('/login/')


class RegisterView(View):
    """
    注册
    """
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', locals())

    def post(self, request):
        register_form = RegisterForm(request.POST)
        message = '请检查填写的内容！'
        if register_form.is_valid():
            user_name = register_form.cleaned_data['user_name']
            user_id = register_form.cleaned_data['user_id']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            if password1 == password2:
                same_id_users = User.objects.filter(id=user_id)
                if same_id_users:
                    message = '该学号已被注册！'
                else:
                    User.objects.create(id=user_id, name=user_name, password=hashcode(password1, user_id))
                    Log.objects.create(user_id=user_id, action='注册')
                    messages.success(request, '注册成功！')
                    return redirect('/login/')
            else:
                message = '两次输入的密码不一致！'
        return render(request, 'register.html', locals())


class HomeView(View):
    """
    个人中心
    """
    def get(self, request):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login/')

        user_id = request.session['user_id']
        borrow_entries = Borrow.objects.filter(user_id=user_id)
        return render(request, 'home.html', locals())


class SearchView(View):
    """
    借书
    """
    def get(self, request):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login/')

        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            keyword = search_form.cleaned_data['keyword']
            books = Book.objects.filter(Q(name__icontains=keyword) | Q(author__icontains=keyword) | Q(publisher__icontains=keyword))
            if not books:
                message = '未查询到相关书籍！'
        return render(request, "search.html", locals())


class BorrowView(View):
    """
    借书操作
    """
    def get(self, request):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login/')

        user_id = request.session['user_id']
        book_id = request.GET.get('book_id')
        books = Book.objects.filter(id=book_id, is_available=True)
        if books:
            book = books.first()
            borrow_time = datetime.now()
            return_ddl = borrow_time + timedelta(days=90)
            Borrow.objects.create(user_id=user_id, book_id=book_id, borrow_time=borrow_time, return_ddl=return_ddl)
            book.is_available = False
            book.save()
            Log.objects.create(user_id=user_id, book_id=book_id, action='借书')
            messages.success(request, '借书成功！')
        else:
            messages.error(request, '借书失败：此书不存在或已借出！')
        return redirect('/search/')


class ReturnView(View):
    """
    还书操作
    """
    def get(self, request):
        if not request.session.get('is_login', None):
            messages.error(request, '请先登录！')
            return redirect('/login/')

        user_id = request.session['user_id']
        book_id = request.GET.get('book_id')
        borrow_entries = Borrow.objects.filter(user_id=user_id, book_id=book_id)
        if borrow_entries:
            borrow_entry = borrow_entries.first()
            delta = -(borrow_entry.borrow_time - datetime.now())  # 负天数不足一天算一天
            exceed_days = delta.days - 90
            if exceed_days > 0:
                fine = exceed_days * 0.5
                messages.warning(request, '已逾期 {} 天，需缴纳罚金 {} 元！'.format(exceed_days, fine))
            borrow_entry.delete()
            book = Book.objects.get(id=book_id)
            book.is_available = True
            book.save()
            Log.objects.create(user_id=user_id, book_id=book_id, action='还书')
            messages.success(request, '还书成功！')
        else:
            messages.error(request, '还书失败：您未借过此书！')
        return redirect('/home/')


class TestView(View):
    """
    for test
    """
    def get(self, request):
        search_form = SearchForm()
        return render(request, 'test.html', locals())


def hashcode(s, salt='17373252'):
    s += salt
    h = hashlib.sha256()
    h.update(s.encode())
    return h.hexdigest()
