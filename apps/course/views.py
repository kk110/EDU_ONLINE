from django.shortcuts import render

# Create your views here.
def courseList(request):
    return render(request,'course-list.html')

def teacherList(request):
    return render(request,'teachers-list.html')

def orgList(request):
    return render(request,'org-list.html')
