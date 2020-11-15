from django.shortcuts import render,redirect,get_object_or_404


# Create your views here.

from django.forms import ModelForm
from cats.models import Breed,Cat

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.http import HttpResponse
from django.template.loader import render_to_string

# Create the form class.
class BreedForm(ModelForm):
    class Meta:
        model = Breed
        fields = '__all__'

class CatListView(LoginRequiredMixin,View):
    def get(self,request):
        bc=Breed.objects.all().count()
        cl=Cat.objects.all()
        context={'breed_count':bc,'cat_list':cl}
        return render(request,'cats/cat_list.html',context)

class BreedListView(LoginRequiredMixin,View):
    def get(self,request):
        bl=Breed.objects.all()
        context={'breed_list':bl}
        return render(request,'cats/breed_list.html',context)

class BreedCreate(LoginRequiredMixin,View):
    template='cats/breed_form.html'
    success_url=reverse_lazy('cats:all')
    def get(self,request):
        form =BreedForm()
        context={'form':form}
        return render(request,self.template,context)

    def post(self,request):
        form=BreedForm(request.POST)
        if not form.is_valid():
            context={'form':form}
            return render(request,self.template,context)
        breed=form.save()
        return redirect(self.success_url)

class BreedUpdate(LoginRequiredMixin,View):
    model=Breed
    template='cats/breed_form.html'
    success_url=reverse_lazy('cats:all')
    def get(self,request,pk):
        breed=get_object_or_404(self.model,pk=pk)
        form =BreedForm(instance=breed)
        context={'form':form}
        return render(request,self.template,context)

    def post(self,request,pk):
        breed=get_object_or_404(self.model,pk=pk)
        form=BreedForm(request.POST,instance=breed)
        if not form.is_valid():
            context={'form':form}
            return render(request,self.template,context)
        breed=form.save()
        return redirect(self.success_url)

class BreedDelete(LoginRequiredMixin,View):
    model=Breed
    template='cats/breed_confirm_delete.html'
    success_url=reverse_lazy('cats:all')
    def get(self,request,pk):
        breed=get_object_or_404(self.model,pk=pk)
        form =BreedForm(instance=breed)
        context={'form':form}
        return render(request,self.template,context)

    def post(self,request,pk):
        breed=get_object_or_404(self.model,pk=pk)
        breed.delete()
        return redirect(self.success_url)

class CatCreate(LoginRequiredMixin,CreateView):
    model=Cat
    fields='__all__'
    success_url=reverse_lazy('cats:all')

class CatUpdate(LoginRequiredMixin,UpdateView):
    model=Cat
    fields='__all__'
    success_url=reverse_lazy('cats:all')

class CatDelete(LoginRequiredMixin,DeleteView):
    model=Cat
    fields='__all__'
    success_url=reverse_lazy('cats:all')
