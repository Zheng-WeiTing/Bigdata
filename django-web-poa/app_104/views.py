from django.shortcuts import render

def home(request):
   return render(request, '104/home.html')  # 對應 104/templates/home.html