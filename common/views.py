from django.shortcuts import render
from captcha.image import ImageCaptcha
from .models import Language
import random
import pyqrcode
from PIL import Image
from .models import Country, Language, City
from django.http import JsonResponse, HttpResponse
from datetime import datetime
import json
from django.db.models import Q


def generate_captcha(length=5):
    #set = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    set = '1234567890'
    gen_text = ''.join((random.choice(set)) for i in range(length))
    img = ImageCaptcha()
    image = img.generate_image(gen_text)
    image.save('media/captcha/captcha.jpg')
    return gen_text


def captcha(request):
    gen_text = generate_captcha()
    return render(request, 'captcha.html', {'gen_text': gen_text})


def qr_code(request):
    # url = pyqrcode.QRCode('Anand Yadav Btech', error='H')
    # url.png('test.png', scale=10)
    # im = Image.open('test.png')
    # im = im.convert("RGBA")
    # logo = Image.open('static/img/fynoo.png')
    # box = (135, 135, 235, 235)
    # im.crop(box)
    # region = logo
    # region = region.resize((box[2] - box[0], box[3] - box[1]))
    # im.paste(region, box)
    # im.show()

    qrobj = pyqrcode.create('Akhil Srivastava')
    with open('test.png', 'wb') as f:
        qrobj.png(f, scale=10)

    img = Image.open('test.png')
    width, height = img.size

    logo_size = 80

    logo = Image.open('static/img/fynoo.png')

    xmin = ymin = int((width / 2) - (logo_size / 2))
    xmax = ymax = int((width / 2) + (logo_size / 2))

    logo = logo.resize((xmax - xmin, ymax - ymin))

    img.paste(logo, (xmin, ymin, xmax, ymax))

    img.show()


def add_country(request):
    if request.method == 'POST':
        form = request.POST
        country_name = form.get('country_name')
        country_code = form.get('country_code')
        saved_id = form.get('update_country')
        # user_id = request.session["id"]
        # user_type = request.session["user_type"]
        todayDateTime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        if saved_id:
            Country.objects.filter(id=int(saved_id)).update(country_name=country_name, country_code= country_code,
                                                             updated_at=todayDateTime)

            json_data = {
                'msg': 'updated successfully',
            }

            return JsonResponse(json_data)

        else:
            add_curr = Country.objects.create(country_name=country_name, country_code= country_code,
                                              )

            json_data = {
                'id': add_curr.id,
                'msg': 'created',
            }

            return JsonResponse(json_data)

    else:
        pass

        return render(request, 'countries.html')


def get_country_list(request):
    start = request.GET.get('start')
    last = request.GET.get('length')
    value = request.GET.get('search')

    if value != 0:
        slt_stmt = Country.objects.filter(country_name__icontains=value)[int(start):(int(last) + int(start))]
        slt_count = Country.objects.filter(country_name__icontains=value).count()
    else:
        slt_stmt = Country.objects.all()[int(start):(int(last) + int(start))]
        slt_count = Country.objects.all().count()

    doc_list1 = []
    inc = int(start) + 1
    for i in slt_stmt:
        doc_list = []
        doc_list.append(inc)

        doc_list.append('<a>' + i.country_name + '</a>')

        doc_list.append('<a>' + i.country_code + '</a>')

        doc_list.append('<div class="action-area">'
                        '<a href="#"><i data-toggle="tooltip" data-placement="top" title="Delete Country"'
                        'class="fa fa-trash-o fa-lg" onclick="country_delete(' + str(i.id) + ')" '
                        'class="fa fa-trash fa-lg" aria-hidden="true"></i></a>'
                        '<a href="#"><i data-toggle="modal" onclick="update_record(' + str(i.id) + ')" '
                        'data-target="#inlineForm" class="fa fa-pencil-square-o fa-lg"'
                        'aria-hidden="true"></i></a></div>')

        doc_list1.append(doc_list)
        inc += 1

    data = {'draw': request.GET.get('draw'), 'recordsTotal': slt_count, 'recordsFiltered': slt_count, 'data': doc_list1}
    return JsonResponse(data)


def country_delete(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        try:
            Country.objects.filter(id=int(id)).delete()
        except Exception as e:
            print(e)
            is_success = 0
        else:
            is_success = 1

        return HttpResponse(is_success)


def get_saved_country(request):
    id = request.GET.get('id')
    data = []
    qs = Country.objects.filter(id=id)
    if qs:
        for i in qs:
            dictt = {}
            dictt['id'] = i.id
            dictt['country_name'] = i.country_name
            dictt['country_code'] = i.country_code

            data.append(dictt)

    return HttpResponse(json.dumps(data))


def add_language(request):
    countries = Country.objects.all()
    if request.method == 'POST':
        form = request.POST
        country = form.get('country')
        language_name = form.get('language_name')
        language_code = form.get('language_code')
        writing_mode = form.get('writing_mode')
        saved_id = form.get('update_language')
        user_id = request.session["id"]
        user_type = request.session["user_type"]
        todayDateTime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        if saved_id:
            Language.objects.filter(id=int(saved_id)).update(country_id=country, language_name=language_name,
                                                             language_code=language_code, writing_mode=writing_mode,
                                                             updated_by=user_id, updated_at=todayDateTime)

            json_data = {
                'msg': 'updated successfully',
            }

            return JsonResponse(json_data)

        else:
            add_curr = Language.objects.create(country_id=country, language_name=language_name,writing_mode=writing_mode,
                                               language_code=language_code, created_by=user_id, user_type=user_type)

            json_data = {
                'id': add_curr.id,
                'msg': 'created',
            }

            return JsonResponse(json_data)

    else:
        pass

        return render(request, 'languages.html', {'countries':countries})


def get_language_list(request):
    start = request.GET.get('start')
    last = request.GET.get('length')
    value = request.GET.get('search')

    if value != 0:
        slt_stmt = Language.objects.filter(language_name__icontains=value)[int(start):(int(last) + int(start))]
        slt_count = Language.objects.filter(language_name__icontains=value).count()
    else:
        slt_stmt = Language.objects.all()[int(start):(int(last) + int(start))]
        slt_count = Language.objects.all().count()

    doc_list1 = []
    inc = int(start) + 1
    for i in slt_stmt:
        doc_list = []
        doc_list.append(inc)

        doc_list.append('<a>' + i.language_name + '</a>')

        doc_list.append('<a>' + i.language_code + '</a>')

        country = Country.objects.filter(id=int(i.country_id)).values('country_name', 'country_code')
        print(country)

        doc_list.append(country[0]['country_name'])

        doc_list.append(i.writing_mode)

        doc_list.append('<div class="action-area">'
                        '<a href="#"><i data-toggle="tooltip" data-placement="top" title="Delete Language"'
                        'class="fa fa-trash-o fa-lg" onclick="language_delete(' + str(i.id) + ')" '
                        'class="fa fa-trash fa-lg" aria-hidden="true"></i></a>'
                        '<a href="#"><i data-toggle="modal" onclick="update_record(' + str(i.id) + ')" '
                        'data-target="#inlineForm" class="fa fa-pencil-square-o fa-lg"'
                        'aria-hidden="true"></i></a></div>')

        doc_list1.append(doc_list)
        inc += 1

    data = {'draw': request.GET.get('draw'), 'recordsTotal': slt_count, 'recordsFiltered': slt_count, 'data': doc_list1}
    return JsonResponse(data)


def language_delete(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        try:
            Language.objects.filter(id=int(id)).delete()
        except Exception as e:
            print(e)
            is_success = 0
        else:
            is_success = 1

        return HttpResponse(is_success)


def get_saved_language(request):
    id = request.GET.get('id')
    data = []
    qs = Language.objects.filter(id=id)
    if qs:
        for i in qs:
            country = Country.objects.filter(id=int(i.country_id)).values('country_name', 'id')
            dictt = {}
            dictt['id'] = i.id
            dictt['language_name'] = i.language_name
            dictt['language_code'] = i.language_code
            dictt['country_name'] = country[0]['country_name']
            dictt['country_id'] = country[0]['id']
            dictt['writing_mode'] = i.writing_mode

            data.append(dictt)

    return HttpResponse(json.dumps(data))


def add_city(request):
    countries = Country.objects.all()
    languages = Language.objects.values('language_code', 'id', 'writing_mode')
    if request.method == 'POST':
        form = request.POST
        country = form.get('country')
        city_name = form.get('city_name')
        saved_id = form.get('update_city')
        # user_id = request.session["id"]
        # user_type = request.session["user_type"]
        todayDateTime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        # lang_code = request.session["cu_language"]
        # lqs = Language.objects.filter(language_code=lang_code).values('id')
        # lqs = lqs[0]['id']
        translate_id = form.get('translatect')
        language = form.get('languages')

        if saved_id:
            City.objects.filter(id=int(saved_id)).update(country_id=country, city_name=city_name,
                                                         updated_at=todayDateTime)

            json_data = {
                'msg': 'updated successfully',
            }

            return JsonResponse(json_data)

        elif translate_id:
            City.objects.create(primary_city_id=int(translate_id), country_id=country, city_name=city_name,
                                language_id=int(language))

            return HttpResponse('Translated Successfully !!')

        else:
            add_city = City.objects.create(country_id=country, city_name=city_name)

            City.objects.filter(id=add_city.id).update(primary_city_id=add_city.id)

            json_data = {
                'id': add_city.id,
                'msg': 'created',
            }

            return JsonResponse(json_data)

    else:
        pass

        return render(request, 'cities.html', {'countries':countries, 'languages':languages})


def get_city_list(request):
    start = request.GET.get('start')
    last = request.GET.get('length')
    value = request.GET.get('search')
    lang_code = request.session["cu_language"]
    lqs = Language.objects.filter(language_code=lang_code).values('id')
    lqs = lqs[0]['id']
    listt = []
    abc = City.objects.filter(language_id=lqs).values_list('primary_city_id', flat=True).distinct()
    for obj in range(len(abc)):
        listt.append(abc[obj])
    abc2 = City.objects.values_list('primary_city_id', flat=True).distinct()
    listt2 = []
    for obj in range(len(abc2)):
        listt2.append(abc2[obj])
    main_list = list(set(listt2) - set(listt))
    abc3 = City.objects.filter(id__in=main_list).values_list('id', flat=True).distinct()
    listt3 = []
    for obj in range(len(abc3)):
        listt3.append(abc3[obj])
    q = Q(language_id=lqs) | Q(id__in=listt3)

    if value != 0:
        slt_stmt = City.objects.filter(q, city_name__icontains=value).order_by('id')[int(start):(int(last) + int(start))]
        slt_count = City.objects.filter(q, city_name__icontains=value).count()
    else:
        slt_stmt = City.objects.filter(q)[int(start):(int(last) + int(start))]
        slt_count = City.objects.filter(q).count()

    doc_list1 = []
    inc = int(start) + 1
    for i in slt_stmt:
        doc_list = []
        doc_list.append(inc)

        doc_list.append('<a>' + i.city_name + '</a>')

        country = Country.objects.filter(id=int(i.country_id)).values('country_name', 'country_code')

        doc_list.append(country[0]['country_name'])

        doc_list.append(country[0]['country_code'])

        doc_list.append('<div class="action-area">'
                        '<a><i data-toggle="tooltip" data-placement="top" title="Delete City"'
                        'class="fa fa-trash-o fa-lg" onclick="city_delete(' + str(i.id) + ')" '
                        'class="fa fa-trash fa-lg" aria-hidden="true"></i></a>'
                        '<a><i data-toggle="modal" onclick="update_record(' + str(i.id) + ')" '
                        'data-target="#inlineForm" class="fa fa-pencil-square-o fa-lg"'
                        'aria-hidden="true"></i></a><a><i data-toggle="modal" onclick="translate_record('
                        + str(i.primary_city_id) + ', ' + str(i.id) + ')" '
                        'data-id="' + str(i.id) + '" data-target="#inlineForm" class="fa fa-globe"'
                        'aria-hidden="true" id="record_' + str(i.primary_city_id) + '"></i></a></div>')

        doc_list1.append(doc_list)
        inc += 1

    data = {'draw': request.GET.get('draw'), 'recordsTotal': slt_count, 'recordsFiltered': slt_count, 'data': doc_list1}
    return JsonResponse(data)


def city_delete(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        try:
            City.objects.filter(id=int(id)).delete()
        except Exception as e:
            print(e)
            is_success = 0
        else:
            is_success = 1

        return HttpResponse(is_success)


def get_saved_city(request):
    id = request.GET.get('id')
    data = []
    qs = City.objects.filter(id=id)
    if qs:
        for i in qs:
            lang_l = City.objects.filter(primary_city_id=i.id).values_list('language_id', flat=True).distinct()
            lang_list = []
            for lng in lang_l:
                lang_list.append(lng)
            print(lang_list)
            country = Country.objects.filter(id=int(i.country_id)).values('country_name', 'id', 'country_code')
            dictt = {}
            dictt['id'] = i.id
            dictt['city_name'] = i.city_name
            dictt['country_name'] = country[0]['country_name']
            dictt['country_id'] = country[0]['id']
            dictt['country_code'] = country[0]['country_code']
            dictt['lang_list'] = lang_list

            data.append(dictt)

    return HttpResponse(json.dumps(data))


def all_lang(request):
    languages = Language.objects.all()

    return render(request, 'lng_dropdown.html', {'languages': languages})