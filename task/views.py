from typing import Any, Dict

from django.shortcuts import redirect

from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from task.models import Task

from django.db.models import Q


class CustomLoginView(LoginView):
    """
    provides a custom implementation for the login functionality in our To_Do web application.
    """
    template_name = 'task/login.html'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        """
        returns homepage URL to redirect to after a successful login.
        """
        return reverse_lazy('home')


class RegisterForm(FormView):
    """
    a form view that handles user registration.
    it uses the UserCreationForm form class provided by Django to display and process the registration form.
    """
    template_name = 'task/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form: Any) -> HttpResponse:
        """
        This method is responsible for processing the submitted form data,
        and logging the new user in if the form is valid.
        """
        if (user := form.save()) is not None:
            login(self.request, user)
        return super(RegisterForm, self).form_valid(form)

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """
        redirects the authenticated user to the success_url.
        """
        if self.request.user.is_authenticated:
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    """
    a class based view to display a list of tasks.
    """
    model = Task
    context_object_name = 'tasklist'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        this method is responsible for modifying the context data that will be passed to the template.
        it also filters data based on the current user tasks and the search inputs.
        """
        context = super().get_context_data(**kwargs)
        tasklist = context['tasklist'].filter(user=self.request.user)
        context['count'] = tasklist.filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            tasklist = tasklist.filter(
                Q(title__icontains=search_input) | Q(description__icontains=search_input)
            )

        context['search_input'] = search_input
        context['tasklist'] = tasklist

        return context


class TaskCreate(LoginRequiredMixin, CreateView):
    """
    a class based view that allows users to create new tasks.
    it requires the user to be logged in, and upon successful form submission,
    it assigns the current user as the owner of the task.

    """
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('home')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """
        This method is responsible for assigning the current user as the owner of the task.
        """
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    """
    This class is used to update a Task object(task).
    success_url: specifies the URL to redirect the user to homepage after a successful update.
    """
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('home')


class TaskDelete(LoginRequiredMixin, DeleteView):
    """
    a Django view that allows users to delete a specific Task object(task).
    success_url: specifies the URL to which the user will be redirected after successfully deleting the task.
    """
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('home')
