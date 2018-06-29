from django.shortcuts import render
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
	'''
	if problems.number < (paginator.num_pages()-2) and problems.number > 3:
		end_index = problems.number+2
	elif problems.number <= 3:
		end_index = 5
	else:
		end_index = paginator.num_pages()
	'''

	page_range = range(start_index,end_index)

	context = {
		"problems": problems,
		"page_range": page_range,
	}
	template = 'codeit/problems.html'
	return render(request, template, context)