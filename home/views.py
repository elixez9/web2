from django.shortcuts import render, redirect
from django.views import View
from pyexpat.errors import messages
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CreateUpdateForm
from django.utils.text import slugify


class HomeView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/home.html', {'posts': posts})


class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = Post.objects.get(pk=post_id, slug=post_slug)
        return render(request, 'home/post.html', {'post': post})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
        else:
            messages.error(request, 'You are not authorized to delete this post')
            return redirect('home')


def game(request):
    return render(request, 'home/game.html')


class PostUpdateView(LoginRequiredMixin, View):
    form_class = CreateUpdateForm

    def setup(self, request, *args, **kwargs):  #وصل شدن به دیتابیس
        self.post_instance = Post.objects.get(pk=kwargs['post_id'])  #گرفتن اطلاعات
        super().setup(self, request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        post = self.post_instance
        if not post.user.id == request.user.id:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, post_id):
        post = self.post_instance  #وصل شدن به دیتابیس  در همه متد ها استفاده شده
        form = self.form_class(instance=post)
        return render(request, 'home/update.html', {'form': form})

    def post(self, request, post_id):  #اپدیت کردن پست و سیو ان
        post = self.post_instance
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)  #نگه داشتن سیو های قبلی و اضافه کردن مقادیر جدید
            new_post.slug = slugify(form.cleaned_data['body'][:30])  #عوض کردن اسلاگ نسبت به اپدیت
            new_post.save()  #سیو دوباره
            return redirect('home:post_d', post.id, post.slug)


class PostCreateView(LoginRequiredMixin, View):
    form_class = CreateUpdateForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'home/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:30])
            new_post.user = request.user
            new_post.save()

