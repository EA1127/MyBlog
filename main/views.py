from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView

from .forms import NewsForm, ImageForm, CommentForm
from .models import *


def index(request):
    return render(request, 'index.html', {'economy': 'economy',
                                          'politics': 'politics',
                                          'fashion': 'fashion',
                                          'showbusiness': 'showbusiness',
                                          'itworld': 'itworld',
                                          'lifehacks': 'lifehacks'})


def see_all_news(request):
    news = News.objects.all()
    paginator = Paginator(news, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'see_all_news.html', {'page_obj': page_obj})


class MainPageView(ListView):
    model = News
    template_name = 'index.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_template_names(self):
        template_name = super(MainPageView, self).get_template_names()
        search = self.request.GET.get('q')
        filter_ = self.request.GET.get('filter')

        if search:
            template_name = 'search.html'
        elif filter_:
            template_name = 'fresh.html'
        else:
            template_name = 'search.html'
        return template_name

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('q')
        filter_ = self.request.GET.get('filter')
        if search:
            context['news'] = News.objects.filter(Q(title__icontains=search)|Q(content__icontains=search))
        elif filter_:
            start_date = timezone.now() - timedelta(hours=24)
            context['news'] = News.objects.filter(created__gte=start_date)
        else:
            context['news'] = News.objects.none()
        return context


def blog_category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    news = News.objects.filter(category_id=slug)
    return render(request, 'blog_category_detail.html', locals())


def news_detail(request, pk):
    new = get_object_or_404(News, pk=pk)
    image = new.get_image
    images = new.images.exclude(id=image.id)
    comments = new.comments.filter(active=True)
    is_favorite = False

    if new.favorites.filter(id=request.user.id).exists():
        is_favorite = True

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = new
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'news_detail.html', locals())


@login_required(login_url='login')
def add_news(request):
    ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=6)
    if request.method == "POST":
        news_form = NewsForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        if news_form.is_valid() and formset.is_valid():
            new = news_form.save()

            for form in formset.cleaned_data:
                image = form['image']
                Image.objects.create(image=image, new=new)
            return redirect(new.get_absolute_url())
    else:
        news_form = NewsForm()
        formset = ImageFormSet(queryset=Image.objects.none())
    return render(request, 'add_news.html', locals())


def update_news(request, pk):
    new = get_object_or_404(News, pk=pk)
    if request.user == new.user:
        ImageFormSet = modelformset_factory(Image, form=ImageForm, max_num=6)
        news_form = NewsForm(request.POST or None, instance=new)
        formset = ImageFormSet(request.POST or None, request.FILES or None, queryset=Image.objects.filter(new=new))
        if news_form.is_valid() and formset.is_valid():
            new = news_form.save()

            for form in formset:
                image = form.save(commit=False)
                image.new = new
                image.save()
            return redirect(new.get_absolute_url())
        return render(request, 'update_news.html', locals())
    else:
        return HttpResponse('<h1>403 Forbidden</h1>')


def delete_news(request, pk):
    new = get_object_or_404(News, pk=pk)
    if request.user == new.user:
        if request.method == "POST":
            new.delete()
            messages.add_message(request, messages.SUCCESS, 'The posted news was successfully deleted!')
            return redirect('home')
        return render(request, 'delete_news.html')
    else:
        return HttpResponse('<h1>403 Forbidden</h1>')


def add_to_favorites(request, pk):
    new = get_object_or_404(News, pk=pk)
    if new.favorites.filter(id=request.user.id).exists():
        new.favorites.remove(request.user)
    else:
        new.favorites.add(request.user)
    return HttpResponseRedirect(new.get_absolute_url())


def favorite_posts_list(request):
    user = request.user
    favorite_posts = user.favorites.all()
    context = {
        'favorite_posts': favorite_posts,
    }
    return render(request, 'favorite_posts_list.html', context)
