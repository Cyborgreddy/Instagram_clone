from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from .forms import SignInForm, PostForm, ReelForm
from .models import Post, Reel, Like, Comment
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# Create your views here.

def sign_in(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # redirect to home page after successful login
        else:
            error = 'Invalid username or password'

    return render(request, 'sign_in.html', {'error': error})

def signout(request):
    logout(request)
    return redirect('sign_in')

def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Account created successfully')
                return redirect('sign_in')  # redirect to sign-in page after successful sign-up
        else:
            messages.error(request, 'Passwords do not match')

    return render(request, 'sign_up.html')

def web(request):
    return render(request, 'web.html')

@csrf_protect
@login_required(login_url='sign_in')
def home(request):
    query = request.GET.get('q')
    posts = Post.objects.all().order_by('-created_at')
    reels = Reel.objects.all().order_by('-created_at')
    user_query = request.GET.get('user_query')

    if query:
        posts = posts.filter(caption__icontains(query))
        reels = reels.filter(caption__icontains(query))
    

    paginator_posts = Paginator(posts, 10)  # Show 10 posts per page
    paginator_reels = Paginator(reels, 10)  # Show 10 reels per page

    page_number_posts = request.GET.get('page_posts')
    page_number_reels = request.GET.get('page_reels')

    page_obj_posts = paginator_posts.get_page(page_number_posts)
    page_obj_reels = paginator_reels.get_page(page_number_reels)

    return render(request, 'home.html', {
        'query': query,
        'page_obj_posts': page_obj_posts,
        'page_obj_reels': page_obj_reels,
    })

@login_required(login_url='sign_in')
@require_POST
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return JsonResponse({'success': True, 'likes_count': post.likes.count(), 'liked': liked})

@login_required(login_url='sign_in')
def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all()
    is_liked = Like.objects.filter(user=request.user, post=post).exists()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', id=post.id)
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'form': form, 'is_liked': is_liked})

@login_required(login_url='sign_in')
def like_post(request, id):
    post = get_object_or_404(Post, id=id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('post_detail', id=post.id)

@login_required(login_url='sign_in')
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'post_list.html', {'page_obj': page_obj})

@login_required(login_url='sign_in')
def reel_list(request):
    reels = Reel.objects.all().order_by('-created_at')
    paginator = Paginator(reels, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'reel_list.html', {'page_obj': page_obj})

@login_required(login_url='sign_in')
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'add_post.html', {'form': form})

@login_required(login_url='sign_in')
def add_reel(request):
    if request.method == 'POST':
        form = ReelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('reel_list')
    else:
        form = ReelForm()
    return render(request, 'add_reel.html', {'form': form})

def user_search(request):
    user_query = request.GET.get('user_query')
    user = None
    posts = []
    reels = []

    if user_query:
        user = get_object_or_404(User, username=user_query)
        posts = Post.objects.filter(user=user)
        reels = Reel.objects.filter(user=user)

    paginator_posts = Paginator(posts, 10)
    paginator_reels = Paginator(reels, 10)
    page_number_posts = request.GET.get('page_posts')
    page_number_reels = request.GET.get('page_reels')
    page_obj_posts = paginator_posts.get_page(page_number_posts)
    page_obj_reels = paginator_reels.get_page(page_number_reels)

    context = {
        'user': user,
        'page_obj_posts': page_obj_posts,
        'page_obj_reels': page_obj_reels,
        'user_query': user_query,
    }

    return render(request, 'user_search.html', context)