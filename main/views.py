from django.forms import modelformset_factory
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import NewsForm, ImageForm
from .models import *



def index(request):
    return render(request, 'index.html')


def blog_category_detail(request, slug):
    category = Category.objects.get(slug=slug)
    news = News.objects.filter(category_id=slug)
    return render(request, 'blog_category_detail.html', locals())


def news_detail(request, pk):
    new = get_object_or_404(News, pk=pk)
    image = new.get_image
    images = new.images.exclude(id=image.id)
    return render(request, 'news_detail.html', locals())


# @login_required(login_url='login')
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
    if request.method == "POST":
        new.delete()
        messages.add_message(request, messages.SUCCESS, 'The news was successfully deleted!')
        return redirect('home')
    return render(request, 'delete_news.html')
