from django.shortcuts import render, redirect
from codeit.models import Problem
from django.core.paginator import Paginator

def index(request):
	return render(request, 'codeit/index.html')
def list_problems(request):
	problems = Problem.objects.all()

	paginator = Paginator(problems,11)

	page = request.GET.get('page')

	problems = paginator.get_page(page)

	start_index = None
	end_index = None
	if problems.number > 3 and problems.number < paginator.num_pages-2:
		start_index = problems.number-2
		end_index = problems.number+3
	elif problems.number <= 3:
		start_index = 1
		end_index = 6
	else:
		start_index = paginator.num_pages-4
		end_index = paginator.num_pages+1

	page_range = range(start_index,end_index)

	context = {
		"problems": problems,
		"page_range": page_range,
	}
	template = 'codeit/problems/problems.html'
	return render(request, template, context)
	
def search(request):
	title_query = None
	problem_query = None
	input_query = None
	output_query = None
	time_limit_query = None
	if request.method == "GET":
		title_query = request.GET.get('title_box', None)
		problem_query = request.GET.get('problem_box', None)
		input_query = request.GET.get('input_box', None)
		output_query = request.GET.get('output_box', None)
		time_limit_query = request.GET.get('time_limit_box', None)
		
	'''	
	if request.method == "POST":
		title_query = request.POST.get('title_box', None)
		problem_query = request.POST.get('problem_box', None)
		input_query = request.POST.get('input_box', None)
		output_query = request.POST.get('output_box', None)
		time_limit_query = request.POST.get('time_limit_box', None)
		print(title_query, problem_query)
	
	
		return redirect('/')'''
	
	#print(title_query, problem_query)
	
	return render(request, 'codeit/search/index.html')