Django Custom Authorization 

The Django custom Authorization is base on django groups. This authorization applied to API controller.
suppose specific Api access to specific group of the user then your refer to this packages.

Below step for installation and configuration:
1>	First download authorizeapi package in git repository.
	Install package on the terminal using command:
	pip install django-authorizeapi-1.0.tar.gz [downloaded path]
2>	Now changes in default setting py : 
	INSTALLED_APPS = [
						‘authorizeapi’   <-- add package name
					]
	MIDDLEWARE = [
				# 'django.middleware.csrf.CsrfViewMiddleware',   <-- Comment this package
				]
    Now Added below code in the setting py:
    CACHE_MIDDLEWARE_SECONDS = 31449600 #(approximately 1 year, in seconds)
    # django cache data store in default RAM memory using MemcachedCache. here MemcachedCache configurations
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = "default"
3>  Install required packages:
    pip install python-memcached
4>	when you run your project before makemigrations authorizeapi and then migrate project. Below makemigrations command:
	python manage.py makemigrations authorizeapi

5>	Now applied Authorization decorator method on any api controller method:

from authorizeapi.permission import Authorize   # import authorizeapi

@api_view(['GET'])
@Authorize(['Admin'])  <-- 'Admin' as Group Name,You can assign multiple group names
def read(request):
	.....
	return HttpResponse()
	
6>	Before test your code, First Create group and assign to users.

7>  In group you can add super group means super group can access child group permission.
	
