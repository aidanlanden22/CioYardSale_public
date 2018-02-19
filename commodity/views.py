from django.shortcuts import render
from .forms import CommodityForm, CommodityPicForm
from .models import Commodity
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

# Create your views here.
def sell(request):
    if request.method == 'POST':
        commodityForm = CommodityForm(request.POST)
        formErrors = {}
        formErrors.update(commodityForm.errors)
        if commodityForm.is_valid():
            com = commodityForm.save(commit=False)
            com.save()
            
            return HttpResponseRedirect(reverse('index'))
        
        return render(request, 'createcommodity.html', {'errors': formErrors, 'commodityForm': commodityForm})
    commodityForm = CommodityForm()
    #return render(request, 'sponsorsignup.html', {'sponsorForm': sponsorForm})