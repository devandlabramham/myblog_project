from django.shortcuts import render,redirect,get_object_or_404
from django.utils import timezone
from blog.models import Post,Comment
from django.views.generic import (TemplateView,ListView,
                                    DetailView,CreateView,
                                    UpdateView,DeleteView,)

from django.contrib.auth.mixins import LoginRequiredMixin
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    # define how you want grab list for that create method in PostListView
    # SQLquerey set, PostListView
    def get_queryset(self):
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('published_date')

class PostDetailView(DetailView):
    model = Post

# we need to import mixins for Class Based Views we need to import them
class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

#to delete a post
class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    #where to return on success delete
    #but for that we neewd reverse_lazy
    success_url = reverse_lazy('post_list')

#before publishing they should go to drafts
class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_draft_list.html'
    model = Post

    #queryset for SQLquerey
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')

#########################################
#########################################


#publish POST
@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)


# for this we need to import get_object_or_404 & redirect

@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})

#Approval comment

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

#views function
@login_required
def comment_remove(request,pk):
    commnent = get_object_or_404(Commnent,pk=pk)
    post_pk = commnent.post.pk
    commnent.delete()
    return redirect('post_detail',pk=post_pk)
