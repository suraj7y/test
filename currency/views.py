from django.shortcuts import render
from .models import Currency
from common.models import Country
from django.http import JsonResponse, HttpResponse
import json
from datetime import datetime

# Create your views here.


def add_currency(request):
    if request.method == 'POST':
        form = request.POST
        country = form.get('country')
        currency_name = form.get('currency_name')
        currency_code = form.get('currency_code')
        saved_id = form.get('update_currency')
        user_id = request.session["id"]
        user_type = request.session["user_type"]
        todayDateTime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        if saved_id:
            Currency.objects.filter(id=int(saved_id)).update(country_name_id=int(country), currency=currency_name,
                                                             currency_code=currency_code, updated_by=user_id,
                                                             updated_at=todayDateTime)

            json_data = {
                'msg': 'updated successfully',
            }

            return JsonResponse(json_data)

        else:
            add_curr = Currency.objects.create(country_name_id=int(country), currency=currency_name,
                                               currency_code=currency_code, created_by=user_id, user_type=user_type)

            json_data = {
                'id': add_curr.id,
                'msg': 'created',
            }

            return JsonResponse(json_data)

    else:
        currency = Currency.objects.values_list('id', 'currency_code', 'currency').distinct()
        countries = Country.objects.all()

        return render(request, 'currency.html', {'currency': currency, 'countries': countries})


def get_currency_list(request):
    start = request.GET.get('start')
    last = request.GET.get('length')
    value = request.GET.get('search')

    if value != 0:
        slt_stmt = Currency.objects.filter(currency__icontains=value)[int(start):(int(last) + int(start))]
        slt_count = Currency.objects.filter(currency__icontains=value).count()
    else:
        slt_stmt = Currency.objects.all()[int(start):(int(last) + int(start))]
        slt_count = Currency.objects.all().count()

    doc_list1 = []
    inc = int(start) + 1
    for i in slt_stmt:
        doc_list = []
        doc_list.append(inc)

        doc_list.append('<a>' + i.currency + '</a>')

        doc_list.append('<a>' + i.currency_code + '</a>')

        country_name = Country.objects.filter(id=int(i.country_name_id)).values('country_name')

        doc_list.append('<a>' + country_name[0]['country_name'] + '</a>')

        doc_list.append('<div class="action-area">'
                        '<a href="#"><i data-toggle="tooltip" data-placement="top" title="Delete Currency"'
                        'class="fa fa-trash-o fa-lg" onclick="currency_delete(' + str(i.id) + ')" '
                        'class="fa fa-trash fa-lg" aria-hidden="true"></i></a>'
                        '<a href="#"><i data-toggle="modal" onclick="update_record(' + str(i.id) + ')" '
                        'data-target="#inlineForm" class="fa fa-pencil-square-o fa-lg"'
                        'aria-hidden="true"></i></a></div>')

        doc_list1.append(doc_list)
        inc += 1

    data = {'draw': request.GET.get('draw'), 'recordsTotal': slt_count, 'recordsFiltered': slt_count, 'data': doc_list1}
    return JsonResponse(data)


def currency_delete(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        try:
            Currency.objects.filter(id=int(id)).delete()
        except Exception as e:
            print(e)
            is_success = 0
        else:
            is_success = 1

        return HttpResponse(is_success)


def get_saved_currency(request):
    id = request.GET.get('id')
    data = []
    qs = Currency.objects.filter(id=id)
    if qs:
        for i in qs:
            country_name = Country.objects.filter(id=int(i.country_name_id)).values('country_name')

            dictt = {}
            dictt['id'] = i.id
            dictt['currency'] = i.currency
            dictt['currency_code'] = i.currency_code
            dictt['country_id'] = i.country_name_id
            dictt['country_name'] = country_name[0]['country_name']

            data.append(dictt)

    return HttpResponse(json.dumps(data))