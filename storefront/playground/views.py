from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.

def get_home(request):
    #you receive a HTTP request as parameter when the function
    #is called. 
    if request.method == "GET":
        # template = loader.get_template('home.html')
        # return HttpResponse(template.render())
        return render(request,'home.html')

    elif request.method=="POST":
        # context = {'name':'Alice'}
        post_dict = request.POST #the form is returned as dictionary
        print(post_dict)
        address = post_dict['address']
        context = {'message':f'You entered: {address}'}
        return render(request,'home.html',context)
        # return HttpResponse(request.body)
    # return render(request,'hello.html')
    # return HttpResponse("Hello Universe!")
    


