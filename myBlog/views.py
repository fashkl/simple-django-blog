from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .forms import PostForm, PostEditForm, CategoryForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect


# Create your views here.

def like_post_view(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))


class HomeView(ListView):
    model = Post
    template_name = "home.html"
    ordering = ['-post_date']

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        return context


class ArticleDetailView(DetailView):
    model = Post
    template_name = "article_details.html"

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(ArticleDetailView, self).get_context_data(**kwargs)

        post_object = get_object_or_404(Post, id=self.kwargs.get('pk'))
        total_likes = post_object.total_likes()

        liked = False
        if post_object.likes.filter(id=self.request.user.id).exists():
            liked = True

        context['cat_menu'] = cat_menu
        context['total_likes'] = total_likes
        context['liked'] = liked
        return context


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'

    # fields = '__all__'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(AddPostView, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        return context


class UpdatePostView(UpdateView):
    model = Post
    form_class = PostEditForm
    template_name = 'update_post.html'

    # fields = ('title', 'title_tag', 'body')

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(UpdatePostView, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        return context


class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(DeletePostView, self).get_context_data(*args, **kwargs)
        context['cat_menu'] = cat_menu
        return context


def category_list_view(request):
    category_list = Category.objects.all()
    context = {'category_list': category_list}
    return render(request, 'category_list.html', context)


class AddCategoryView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'add_category.html'
    # fields = '__all__'


def category_view(request, category):
    category_posts = Post.objects.filter(category=category)
    return render(request, 'categories.html',
                  {'category': str(category).title().replace('-', ' '), 'category_posts': category_posts})
