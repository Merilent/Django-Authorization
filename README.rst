Django Custom Authorization 

Django custom Authorization base on django groups. This authorization applied to API controller.
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
3>	when you run your project before makemigrations authorizeapi and then migrate project. Below makemigrations command:
	python manage.py makemigrations authorizeapi

4>	Now applied Authorization decorator method on any api controller method:

from authorizeapi.permission import Authorize   # import authorizeapi

@api_view(['GET'])
@Authorize(['Admin'])  <-- 'Admin' as Group Name,You can assign multiple group names
def read(request):
	.....
	return HttpResponse()
	
5>	Before test your code, First Create group and assign to users. 

6>  In group you can add super group means super group can access child group permission.
	
