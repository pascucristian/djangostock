from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages


# Create your views here.
def home(request):
    import requests
    import json

# pk_d70f7407e71045bebe58e195b1c9c32b   iexcloud
#7f67acd2f1ceb748efc775d690ad6ee0  marketstack

    if request.method == 'POST':
        ticker = request.POST['ticker_symbol']
        params = {
            'access_key': '7f67acd2f1ceb748efc775d690ad6ee0', 
            'limit':1
        }
        #api_result = requests.get('http://api.marketstack.com/v1/tickers/'+ticker+'/eod', params)
        api_result = requests.get('http://api.marketstack.com/v1/tickers/'+ticker+'/eod', params)


        try:
            api = json.loads(api_result.content)

        except Exception as e:
            api= "Error..."
        return render(request, 'home.html',{'api': api})
    else:

        return render(request, 'home.html',{'ticker': "Enter a Ticker Symbol"})


def about(request):
    return render(request, 'about.html',{})

def add_stock(request):
    import requests
    import json

    if request.method == 'POST':
        form=StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request,("Stock has been added"))
            return redirect('add_stock')

    else:
        ticker=Stock.objects.all()
        output=[]
        for ticker_item in ticker:
            params = {
                'access_key': '7f67acd2f1ceb748efc775d690ad6ee0', 
                'limit':1
            }
            api_result = requests.get('http://api.marketstack.com/v1/tickers/'+str(ticker_item)+'/eod', params)

            try:
                api = json.loads(api_result.content)
                output.append(api)
            except Exception as e:
                api= "Error..."

        return render(request, 'add_stock.html',{'ticker':ticker,'output':output})

def delete(request, stock_id):
    item= Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock has been deleted"))
    return redirect(delete_stock)

def delete_stock(request):
    ticker=Stock.objects.all()
    return render(request, 'delete_stock.html',{'ticker':ticker})