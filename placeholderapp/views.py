from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from .forms import ImageForm
import hashlib
import os
from django.views.decorators.http import etag
from django.core.urlresolvers import reverse

def generate_etag(request, width, height):
	content = 'Placeholder: {0} x {1}'.format(width, height)
	return hashlib.sha1(content.encode('utf-8')).hexdigest()

# Create your views here.
@etag(generate_etag)
def placeholder(request, width, height):
	form = ImageForm({'height': height, 'width': width})
	if form.is_valid():
		image = form.generate()
		return HttpResponse(image, content_type='image/png')
	else:
		return HttpResponseBadRequest('Invalid Image Request')


def index(request):
	example = reverse('placeholder', kwargs={'width': 50, 'height':50})
	context = {
		'example': request.build_absolute_uri(example)
	}
	return render(request, 'placeholderapp/home.html', context)


