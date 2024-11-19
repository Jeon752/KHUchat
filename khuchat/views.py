from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # 'home.html' 템플릿을 렌더링

#from django.http import HttpResponse

#def home(request):
#    return HttpResponse("Hi")  # "Hi"라는 텍스트를 직접 반환
