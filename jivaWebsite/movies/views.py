from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from movies.models import *


def movies_index(request):
    movies_list = dy2018_info.objects.all()
    try:
    	with open('/tmp/dy2018_worker_checkin') as f:
    		last_checked = f.read()
    except:
    	last_checked = 'Not yet'
    return render(request, 'movies/movies_index.html', {'movies_list': movies_list, 'last_checked':last_checked})

def get_movie_link(request):
	context = {}
	context['error_msg'] = ''
	context['result'] = ''
	try:
		movie_hash = request.GET.get('q')
	except:
		context['error_msg'] = "no such movie hash"
	else:
		context['movie_info'] = dy2018_info.objects.get(hash=movie_hash)
		context['result'] = dy2018_links.objects.filter(hash=movie_hash)
	return render(request, 'movies/movie_links.html', context)