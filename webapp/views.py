from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response

from django.template import loader, RequestContext
from django.views.generic.edit import CreateView

from webapp.models import Recipe


def lista_recetas(request):
    recetas = Recipe.objects.all()
    template = loader.get_template('webapp/recipe_list_template.html')
    context = RequestContext(request, {
        'recetas': recetas
    })
    return HttpResponse(template.render(context))


def new_account(request):
    #TODO if user is authenticated redirect to main
    if request.method == 'POST':
        new_account_form = NewAccountForm(request.POST)
        if new_account_form.is_valid():
            #TODO validar que el nombre de usuario sea único
            # Extract the data from the form and create the User and Profile instance
            
            return HttpResponseRedirect('/thanks/')  # Redirect after POST
            #else -> render respone with the obtained form, with errors and stuff
    else:
        new_account_form = NewAccountForm()

    return render(request, 'webapp/newaccount.html', {'form': new_account_form})
