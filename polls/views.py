
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import HttpResponse
import os
from sklearn.preprocessing import MinMaxScaler


from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .models import Value, Attribute

#afrah
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import pickle
test_data_preprocessed = pd.read_csv('/home/afrahmousa/Downloads/test_preprocessed.csv')
test_data_preprocessed = test_data_preprocessed.drop(['Unnamed: 0'],axis =1)
test_data_preprocessed = test_data_preprocessed.iloc[:,:].values

#afrah

class IndexView(generic.ListView):

    template_name = 'polls/classfication.html'
    context_object_name = 'latest_attribute_list'

    def get_queryset(request):
        """Return the last five published questions."""

        return Attribute.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date'
                )[:5]

    def home(request):

        return render(request, 'polls/classfication.html')
        


def mlmodels(request):

        if 'gNB' in request.POST:
            gaussian = \
                pickle.load(open('/home/afrahmousa/Downloads/gnbmodel.pkl'
                            , 'rb'))
            y_pred = gaussian[-1].predict(test_data_preprocessed)
            output = pd.DataFrame(y_pred)
            output.to_csv('gaussianNB.csv')

            filename = 'gaussianNB.csv'
            response = HttpResponse(open(filename, 'rb').read(),
                                    content_type='text/csv')
            response['Content-Length'] = os.path.getsize(filename)
            response['Content-Disposition'] = 'attachment; filename=%s' \
                % 'gaussianNB.csv'
            return response

        if 'knn' in request.POST:
            knn = \
                pickle.load(open('/home/afrahmousa/Downloads/KNNmodel.pkl'
                            , 'rb'))
            y_pred = knn[-1].predict(test_data_preprocessed)
            output = pd.DataFrame(y_pred)
            output.to_csv('knn.csv')

            filename = 'knn.csv'
            response = HttpResponse(open(filename, 'rb').read(),
                                    content_type='text/csv')
            response['Content-Length'] = os.path.getsize(filename)
            response['Content-Disposition'] = 'attachment; filename=%s' \
                % 'knn.csv'
            return response

        if 'dtree' in request.POST:
            dtree = \
                pickle.load(open('/home/afrahmousa/Downloads/dtreemodel.pkl'
                            , 'rb'))
            y_pred = dtree[0].predict(test_data_preprocessed)
            output = pd.DataFrame(y_pred)
            output.to_csv('dtree.csv')

            filename = 'dtree.csv'
            response = HttpResponse(open(filename, 'rb').read(),
                                    content_type='text/csv')
            response['Content-Length'] = os.path.getsize(filename)
            response['Content-Disposition'] = 'attachment; filename=%s' \
                % 'dtree.csv'
            return response        
    
        
    
    
    

    #afrah

    
def home1(request):

        return render(request, 'polls/doclassification.html')

 # custom method for generating predictions
def getPredictions(bond_length_1, angle_1, bond_length_2, angle_2,bond_length_3, angle_3,bond_length_4, angle_4,bond_length_5, angle_5,bond_length_6, angle_6,bond_length_7, angle_7,bond_length_8, angle_8,bond_length_9, angle_9,bond_length_10):
    import pickle
   # sc = MinMaxScaler(feature_range=(0,1))
    model = pickle.load(open("/home/afrahmousa/Downloads/KNNmodel.pkl", "rb"))
    scaled = pickle.load(open("/home/afrahmousa/Downloads/Scaler.pkl", "rb"))
    prediction = model[0].predict([[bond_length_1, angle_1, bond_length_2, angle_2,bond_length_3, angle_3,bond_length_4, angle_4,bond_length_5, angle_5,bond_length_6, angle_6,bond_length_7, angle_7,bond_length_8, angle_8,bond_length_9, angle_9,bond_length_10]])
    
    if prediction == 1:
        return "simple random  walk"
    elif prediction == 2:
        return "directed random walk"
    elif prediction == 3:
        return "persistent random walk"
    else:
        return "error"   
  # our result page view
def result(request):

    bond_length_1 = float(request.GET['bond_length_1'])
    angle_1 = float(request.GET['angle_1'])
    bond_length_2= float(request.GET['bond_length_2'])
    angle_2 = float(request.GET['angle_2'])
    bond_length_3 = float(request.GET['bond_length_3'])
    angle_3= float(request.GET['angle_3'])
    bond_length_4 = float(request.GET['bond_length_4'])
    angle_4 = float(request.GET['angle_4'])
    bond_length_5= float(request.GET['bond_length_5'])
    angle_5 = float(request.GET['angle_5'])
    bond_length_6= float(request.GET['bond_length_6'])
    angle_6 = float(request.GET['angle_6'])
    bond_length_7= float(request.GET['bond_length_7'])
    angle_7 = float(request.GET['angle_7'])
    bond_length_8= float(request.GET['bond_length_8'])
    angle_8 = float(request.GET['angle_8'])
    bond_length_9= float(request.GET['bond_length_9'])
    angle_9= float(request.GET['angle_9'])
    bond_length_10= float(request.GET['bond_length_10'])
    

    result = getPredictions(bond_length_1,angle_1,bond_length_2,angle_2,bond_length_3,angle_3,bond_length_4,
    angle_4,bond_length_5,angle_5,bond_length_6,angle_6,bond_length_7,angle_7,bond_length_8
    ,angle_8,bond_length_9,angle_9,bond_length_10)
    t=[bond_length_1,bond_length_2,bond_length_3,bond_length_4,
    bond_length_5,bond_length_6,bond_length_7,bond_length_8,
    bond_length_9]
    s=[angle_1,angle_2,angle_3,angle_4,angle_5,angle_6,angle_7,
    angle_8,angle_9]
    fig, ax = plt.subplots()
    ax.plot(t, s)
    ax.set(xlabel='x', ylabel='y',title='Random Walk Class:  '+result)
    ax.grid()
    fig.savefig("plot.png")
    plt.show()
    
   
   

    return render(request, 'polls/result.html', {'result':result})  

class DetailView(generic.DetailView):
    model = Attribute
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any attributes that aren't published yet.
        """
        return Attribute.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Attribute
    template_name = 'polls/results.html'

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
    
def vote(request, attribute_id):
    attribute= get_object_or_404(Attribute, pk=attribute_id)
    try:
        selected_value = attribute.attribute_set.get(pk=request.POST['value'])
    except (KeyError, value.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'attribute': attribute,
            'error_message': "You didn't select a value.",
        })
    else:
        selected_value.votes += 1
        selected_value.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(attribute.id,)))
def results(request, attribute_id):
    attribute = get_object_or_404(Attribute, pk=attribute_id)
    return render(request, 'polls/results.html', {'attribute': attribute})
def vote(request, attribute_id):
    return HttpResponse("You're voting on attribute %s." % attribute_id)
    
def index(request):
    latest_attribute_list = Attribute.objects.order_by('-pub_date')[:5]
    context = {'latest_attribute_list': latest_attribute_list}
    return render(request, 'polls/classfication.html', context)
    
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, '/home/afrahmousa/site/polls/templates/polls/index.html', {'form': form})
    
