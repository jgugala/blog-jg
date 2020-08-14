from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic

from .forms import SignInForm, PostAddForm, PostPhotoFormSet
from .models import Post


# class-based view
class PostsList(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Post.objects.order_by('-created_on')
        user = self.request.user
        if query:
            queryset = queryset.filter(title__icontains=query)
        if not user.is_superuser:
            queryset = queryset.filter(status=1)

        return queryset


class PostDetails(generic.DetailView):
    model = Post
    template_name = 'post_details.html'

    # Performing extra work
    # The last common pattern we’ll look at involves doing some extra work before or after calling the generic view.
    def get_object(self, queryset=None):
        obj = super(PostDetails, self).get_object(queryset=queryset)
        if obj.status != 1 and not self.request.user.is_superuser:
            raise PermissionDenied
        return obj

    # Adding extra context
    # Often you need to present some extra information beyond that provided by the generic view.
    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     # Add in a QuerySet of all the books
    #     context['book_list'] = Post.objects.all()
    #     return context


class PostCreate(UserPassesTestMixin, generic.CreateView):
    model = Post
    template_name = 'post_add.html'
    login_url = '/sign-in'
    form_class = PostAddForm

    def test_func(self):
        return self.request.user.is_superuser

    # return an instance of the form to be used in this view
    def get_form(self, *args, **kwargs):
        form = super(PostCreate, self).get_form(*args, **kwargs)
        form.fields['author'].queryset = User.objects.filter(is_active=True)
        return form

    def get_context_data(self, **kwargs):
        data = super(PostCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['photos_formset'] = PostPhotoFormSet(self.request.POST, self.request.FILES)
        else:
            data['photos_formset'] = PostPhotoFormSet()
        return data

    # def get_success_url(self):
    #     return reverse('post_details', args=[self.object.slug])

    # setting an initial data to the form
    # def get_initial(self, *args, **kwargs):
    #     # Get the initial dictionary from the superclass method
    #     initial = super(PostCreate, self).get_initial()
    #     initial['content'] = 'bla, bla, bla'
    #     return initial

    # passing an additional arg to the form
    # def get_form_kwargs(self, *args, **kwargs):
    #     kwargs = super(PostCreate, self).get_form_kwargs()
    #     user = self.request.user
    #     kwargs['author'] = User.objects.filter(username=user.username) if user.is_superuser else User.objects
    #     return kwargs

    # This method is called when valid form data has been POSTed.
    # It should return an HttpResponse.
    def form_valid(self, form):
        context = self.get_context_data()
        photos_formset = context['photos_formset']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            post = form.save()
            if photos_formset.is_valid():
                photos_formset.instance = post
                photos_formset.save()
        return super(PostCreate, self).form_valid(form)


class PostUpdate(PostCreate, generic.UpdateView):
    pass


class PostDelete(UserPassesTestMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('home')
    login_url = '/sign-in'
    template_name = 'post_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_superuser


# function-based view
def sign_in(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignInForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                # log a user in and redirect to a new URL:
                login(request, user)
                next_param = request.POST.get('next')
                redirect_url = '/' if not next_param else next_param
                return HttpResponseRedirect(redirect_url)
            else:
                form.add_error(None, ValidationError(
                    _('Your username and password didn\'t match. Please try again.'),
                    code='invalid_credentials'
                ))

    # if a GET (or any other method) we'll create a blank form (or redirect if already logged in)
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        else:
            form = SignInForm()

    return render(request, 'sign_in.html', {'form': form})


def sign_out(request):
    logout(request)

    return redirect('home')

