from django.shortcuts import render,reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
import datetime
import json
import requests
import uuid
import os

from .models import Invoice

def donation_view(request):
    return render(request,'donate.html')

def exchanged_rate(amount):
    url = "https://www.blockonomics.co/api/price?currency=USD"
    r  = requests.get(url)
    response = r.json()
    return float(amount)/float(response['price'])

def create_payment(request):
    api_key = settings.API_KEY
    url = 'https://www.blockonomics.co/api/new_address'
    headers = {'Authorization': "Bearer " + api_key}
    r = requests.post(url, headers=headers)
    print(r.status_code)
    if r.status_code == 200:
        print("I AM WORKING")
        address = r.json()['address']
        bits = exchanged_rate(request.POST['usdamount'])
        order_id = uuid.uuid1()
        invoice = Invoice.objects.create(order_id=order_id,
        address = address, btcvalue = bits*1e8,amount=request.POST['usdamount'])
        print(invoice)
        return HttpResponseRedirect(reverse('payment:track_payment',kwargs={'pk':invoice.id}))
    else:
        print(r.status_code,r.text)
        return HttpResponse("Some Errors occured, Try Again!")

def track_invoice(request,pk):
    invoice_id = pk
    print('INVOICE WORKING')
    invoice = Invoice.objects.get(id=invoice_id)
    data = {
        'order_id' : invoice.order_id,
        'bits': invoice.btcvalue/1e8,
        'value': invoice.amount,
        'addr': invoice.address,
        'status':invoice.STATUS_CHOICES[invoice.status+1][1],
        'invoice_status': invoice.status,
    }
    if (invoice.recieved):
        data['paid'] = invoice.recieved/1e8
        if (int(invoice.btcvalue)<=int(invoice.recieved)):
            data['path'] = "Thank You for donating"
    else:
        data['paid'] = 0
    return render(request,'invoice.html',context=data)

def recieve_payment(request):
    
    if (request.method != 'GET'):
        return 
    
    txid  = request.GET.get('txid')
    value = request.GET.get('value')
    status = request.GET.get('status')
    addr = request.GET.get('addr')

    invoice = Invoice.objects.get(address = addr)
    
    invoice.status = int(status)
    if (int(status) == 2):
        invoice.received = value
    invoice.txid = txid
    invoice.save()
    return HttpResponse(200)