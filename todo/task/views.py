from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateTaskForm, SignUpForm, ProfileEditForm
from .models import *
from django.http import Http404, HttpResponseNotFound
from django.template import RequestContext


# Головна сторінка
class Index(TemplateView):
    template_name = "task/index.html"


# Список усіх завдань
class LookMyTasks(LoginRequiredMixin, ListView):
    template_name = "task/MyTasks.html"
    model = Task
    context_object_name = "tasks"

    # Фільтруємо по юзеру, виконуємо гет запит для поля з пошуком записів.
    # Рахуємо кількість виконаних задач, які є в списку
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks"] = context['tasks'].filter(user=self.request.user).order_by('complete', '-pk')
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__contains=search_input)
        context['search_input'] = search_input
        context['done'] = Task.objects.filter(user=self.request.user, complete__exact=True).count()
        context['all'] = Task.objects.filter(user=self.request.user).count()
        return context


# Створення завдання
class CreateTask(LoginRequiredMixin, CreateView):
    template_name = "task/CreateTask.html"
    form_class = CreateTaskForm
    success_url = reverse_lazy('task_page')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreateTask, self).form_valid(form)


# Видалення завдання
class DeleteTask(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task/DeleteTask.html'
    success_url = reverse_lazy('task_page')

    # Перевіряємо чи має доступ юзер до цієї сторінки(щоб через посилання не можна було зайти на чужі завдання)
    # Якщо це не він, піднімаємо помилку
    def get_object(self, queryset=None):
        obj = super(DeleteTask, self).get_object()
        if obj.user != self.request.user:
            raise Http404("Точно працює")
        return obj


# Ономлення завдання
class UpdateTask(LoginRequiredMixin, UpdateView):
    template_name = 'task/CreateTask.html'
    model = Task
    form_class = CreateTaskForm
    success_url = reverse_lazy('task_page')

    # Так само як і DeleteTask
    def get_object(self, queryset=None):
        obj = super(UpdateTask, self).get_object()
        if obj.user != self.request.user:
            raise Http404("Точно працює")
        return obj


# Позначити як виконане(або не виконано)
def complete(request, pk):
    # Перевірка юзера
    if request.user != Task.objects.get(pk=pk).user:
        raise Http404
    data = get_object_or_404(Task, pk=pk)
    person = get_object_or_404(CustomUser, username=data.user)
    # Виконали/не виконали
    # Додаємо і віднімаємо + зберігаємо для того, щоб при видаленні завдання не втрачався бал
    if not data.complete:
        data.complete = True
        person.score += 1
    else:
        data.complete = False
        person.score -= 1
    person.save()
    data.save()
    return redirect('task_page')


# Login
class LoginAccount(LoginView):
    template_name = "task/Login.html"
    fields = "__all__"

    def get_success_url(self):
        return reverse_lazy('main_page')


# Registration
class RegisterAccount(FormView):
    template_name = "task/Registration.html"
    form_class = SignUpForm
    success_url = reverse_lazy("main_page")

    # Якщо зареєструвалися, виходимо зі старого аккаунту і переходимо на новий
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            logout(self.request)
            login(self.request, user)
        return super(RegisterAccount, self).form_valid(form)


# Власний профіль
class ProfileCheck(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "task/ProfileCheck.html"
    context_object_name = "profile"

    # Перевірка юзера/піднімаємо помилку
    def get_object(self, queryset=None):
        obj = super(ProfileCheck, self).get_object(queryset=queryset)
        if obj.username != self.request.user.username:
            raise Http404("Точно працює")
        return obj


# Редагування профілю
class ProfileEdit(LoginRequiredMixin, UpdateView):
    template_name = "task/ProfileEdit.html"
    model = CustomUser
    form_class = ProfileEditForm
    success_url = reverse_lazy('main_page')

    # Перевірка юзера/піднімаємо помилку
    def get_object(self, queryset=None):
        obj = super(ProfileEdit, self).get_object(queryset=queryset)
        if obj.username != self.request.user.username:
            raise Http404("Точно працює")
        return obj


# Рейтингова сторінка
class Rating(ListView):
    template_name = "task/Rating.html"
    context_object_name = "user_rating"
    model = CustomUser

    # видаємо перших 20 людей по балах(+ імені)
    def get_context_data(self, *, object_list=None, **kwargs):
        all_user = CustomUser.objects.all()
        context = super().get_context_data(**kwargs)
        context['user_rating'] = context['user_rating'].order_by('-score', '-username')[:20]
        if self.request.user.is_authenticated:
            context['you_position'] = list(context['user_rating']).index(self.request.user) + 1
        return context


# Перевірити чийсь профіль з рейтингу
class CheckSomebodyProfile(DetailView):
    template_name = "task/CheckSomebodyProfile.html"
    model = CustomUser
    context_object_name = 'profile'


# Підгружаємо свій темплейт для 404 помилки
def page_not_found_view(request, exception):
    return render(request, 'NoPermissionPage.html', status=404)


# Видалення всіх записів, які виконані зі списку
def delete_all_completed_tasks(request):
    if request.method == "POST":
        # Беремо всі записи даного юзера, які виконані і видаляємо
        Task.objects.filter(user=request.user, complete=True).delete()
        return redirect('task_page')
    return render(request, 'task/DeleteDoneTasks.html')
