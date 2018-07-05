from django.shortcuts import render, redirect
from codeit.models import Problem
from django.core.paginator import Paginator
from Ranker import ranker

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
	
	page = request.GET.get('page')
	print(page)
	
	if request.method == "GET":
		title_query = request.GET.get('title_box', None)
		problem_query = request.GET.get('problem_box', None)
		input_query = request.GET.get('input_box', None)
		output_query = request.GET.get('output_box', None)
		time_limit_query = request.GET.get('time_limit_box', None)
		free_query = request.GET.get('free_box', None)
		
		if title_query == None and problem_query == None and input_query == None \
			and output_query == None and time_limit_query == None and free_query == None:
				context = {
					"problems": [],
					"show_no_results": False,
				}
				return render(request, 'codeit/search/index.html')
		
		if title_query == "" and problem_query == "" and input_query == "" \
			and output_query == "" and time_limit_query == "" and free_query == "":
				return redirect('/search')
		else:
			if title_query == None:
				title_query = ""
			if problem_query == None:
				problem_query = ""
			if input_query == None:
				input_query = ""
			if output_query == None:
				output_query = ""
			if time_limit_query == None:
				time_limit_query = ""
			if free_query == None:
				free_query = ""
			problems_ids = ranker.ranking(problem_query,input_query,output_query,time_limit_query,title_query,free_query)
			problems = []
			for prob_id in problems_ids:
				problems.append(Problem.objects.get(pk=prob_id))
				
			#problems = Problem.objects.filter(id__in=problems_ids)
			
			problems, page_range = get_pagination(request, problems, 10)
			
			optional_url = "&title_box="+title_query+"&problem_box="+problem_query\
				+"&input_box="+input_query+"&output_box="+output_query+"&time_limit_box="\
				+time_limit_query+"&free_box="+free_query
			
			
			context = {
				"problems": problems,
				"page_range": page_range,
				"optional_url": optional_url,
				"show_no_results": True,
			}
			return render(request, 'codeit/search/index.html', context)
			
def about(request):
	return render(request,'codeit/aboutus.html')
	
	
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
	
	