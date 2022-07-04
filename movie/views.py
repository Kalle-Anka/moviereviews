from django.shortcuts import render
from django.utils.translation import gettext as _
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from .models import Movie, Review
from .forms import ReviewForm


# Home page.
def home(request):
    searchTerm = request.GET.get('searchMovie')
    movies = Movie.objects.all()
    return render(request, 'home.html',
                  {'searchTerm': searchTerm, 'movies': movies})


def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email':email})

# Elenco guide turistiche.
def scheda(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'scheda.html', {'searchTerm': searchTerm, 'movies': movies},)

# Dettaglio guida turistica.
def detail(request, movie_id):
    movie = get_object_or_404(Movie,pk=movie_id)
    reviews = Review.objects.filter(movie=movie)
    count = Review.objects.filter(movie=movie).count()
    if count == 0:
        errore = 'Ancora nessuna recensione.'
    else:
        errore = 'Ecco le recensione degli utenti'
    return render(request, 'detail.html', {'movie': movie, 'reviews': reviews, 'Errore': errore})



# Recensione guida turistica.
def createreview(request, movie_id):
    movie = get_object_or_404(Movie,pk=movie_id)
    if request.method == 'GET':
        return render(request, 'createreview.html', {'form': ReviewForm(), 'movie': movie})
    else:
        try:
            form = ReviewForm(request.POST)
            newReview = form.save(commit=False)
            newReview.user = request.user
            newReview.movie = movie
            newReview.save()
            return redirect('detail', newReview.movie.id)
        except ValueError:
            return render(request, 'createreview.html', {'form': ReviewForm(), 'error': 'bad data passed in '})

def updatereview(request, review_id):
    review = get_object_or_404(Review,pk=review_id,user=request.user)
    if request.method == 'GET':
        form = ReviewForm(instance=review)
        return render(request, 'updatereview.html',{'review': review,'form':form,})
    else:
        try:
            form = ReviewForm(request.POST,instance=review)
            form.save()
            return redirect('detail', review.movie.id)
        except ValueError:
            return render(request,'updatereview.html',{'review': review,'form':form,'error':'Bad data in form'})