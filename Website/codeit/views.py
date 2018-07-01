from django.shortcuts import render, redirect
from codeit.models import Problem
from django.core.paginator import Paginator

def index(request):
	return render(request, 'codeit/index.html')
	
def list_problems(request):
	problems = Problem.objects.all()
	
	problems, page_range = get_pagination(request, problems, 12)

	context = {
		"problems": problems,
		"page_range": page_range,
		"optional_url": "",
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
		
		if title_query == None and problem_query == None and input_query == None \
			and output_query == None and time_limit_query == None:
				context = {"problems": []}
				return render(request, 'codeit/search/index.html', context)
		
		if title_query == "" and problem_query == "" and input_query == "" \
			and output_query == "" and time_limit_query == "":
				return redirect('/search')
		else:
			problems_ids = ranking(title_query,problem_query,input_query,output_query,time_limit_query)
			problems = Problem.objects.filter(id__in=problems_ids)
			
			problems, page_range = get_pagination(request, problems, 10)
			
			optional_url = "&title_box="+title_query+"&problem_box="+problem_query\
				+"&input_box="+input_query+"&output_box="+output_query+"&time_limit_box="+time_limit_query
			
			
			context = {
				"problems": problems,
				"page_range": page_range,
				"optional_url": optional_url,
			}
			return render(request, 'codeit/search/index.html', context)
		
	
	
def get_pagination(request, problems, objects_number):
	paginator = Paginator(problems,objects_number)

	page = request.GET.get('page')

	problems = paginator.get_page(page)

	start_index = None
	end_index = None
	if problems.number > 3 and problems.number < paginator.num_pages-2:
		start_index = problems.number-2
		end_index = problems.number+3
	elif problems.number <= 3:
		start_index = 1
		end_index = min(paginator.num_pages+1,6)
	else:
		start_index = paginator.num_pages-4
		end_index = paginator.num_pages+1

	page_range = range(start_index,end_index)
	
	yield problems
	yield page_range
	
	

def ranking(title_query,problem_query,input_query,output_query,time_limit_query):
	problems_ids = []
	for x in range(0,4):
		problems_ids.append(x)
	return problems_ids