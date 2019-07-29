from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from category.models import *
from product.models import *
from common.models import *
from accounts.models import *
import datetime
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from category.models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from currency.models import *
# Create your views here.
from product.serializers import ProductInfoSerializer


def redirect_to_login(request):
    """this will redirect on user login page"""

    return HttpResponseRedirect('/accounts/login/')

def addproduct(request):
    user_type = request.session['user_type']
    bo_id = request.session['id']

    if request.method == "POST":
        form = request.POST
        form1 = request.FILES
        print(form)
        print(form1)
        pass
        pro_name = form.get('pro_name')
        pro_sku = form.get('pcode')
        pro_cat = form.get('pro_cat')
        #pro_brand = form.get('pro_brand')
        pro_brand = ''
        pro_price = form.get('pro_price')
        pro_price_ciurrency = form.get('pro_price_ciurrency')
        online_pro_qty = form.get('online_pro_qty')
        offline_pro_qty = form.get('offline_pro_qty')
        pro_vat = form.get('pro_vat')

        pro_featured = form.get('pro_featured')
        pro_cod = form.get('pro_cod')
        pro_shipping_price = form.get('pro_shipping_price')
        pro_exchange_period = form.get('pro_exchange_period')
        pro_weight = form.get('pro_weight')
        pro_image = form1.getlist('upload_files[]')
        pro_details = form.get('pro_details')
        featured_image=form.getlist('featured_img[]')
        pro_specification = form.get('pro_specification')
        pro_bo = form.get('pro_bo')
        today_date = datetime.date.today()
        operator_id = request.session["id"]
        lang = request.session["cu_language"]
        proid = form.get('proid')
        if proid:
            qs = Productmaster.objects.filter(id=int(proid)).update(pro_bo_id=bo_id,
                                              pro_name=pro_name,
                                              pro_bo_sku=pro_sku,
                                              pro_cat_id=pro_cat,
                                              pro_brand=pro_brand,
                                              pro_price=pro_price,
                                              pro_price_currency_id=pro_price_ciurrency,
                                              online_pro_qty=online_pro_qty,
                                              offline_pro_qty=offline_pro_qty,
                                              pro_vat=pro_vat,
                                              pro_weight=pro_weight,
                                              pro_desc=pro_details,
                                              pro_spec=pro_specification,
                                              pro_shipping_price=pro_shipping_price,
                                              pro_cod=pro_cod,
                                              pro_exchange_offer=pro_exchange_period,
                                              pro_featured=pro_featured,
                                              pro_status='0',
                                              pro_add_date=today_date)
            if pro_image:
                Productimage.objects.filter(pro_id=proid).delete()
                for s in range(len(pro_image)):
                    sq = Productimage.objects.create(pro_id=proid,
                                                     bo_id=pro_bo,
                                                     pro_image=pro_image[s],
                                                     featured_image=featured_image[s],
                                                     image_added_by=operator_id)
            pa = Productquantity_history.objects.create(pro_id=proid,online_qty=online_pro_qty,offline_qty=offline_pro_qty)
            pp = Productprice_history.objects.create(pro_id=proid,price=pro_price)

            log_stmt = Log_conversation.objects.create(content_id=proid, content_table='product_master', operation='Update',
                                                       operator_id=operator_id, operator_type='', operation_lang=lang)
            return HttpResponse('Operation perform successfully.')

        else:
            qs = Productmaster.objects.create(pro_bo_id=bo_id,
                                              pro_name=pro_name,
                                              pro_bo_sku=pro_sku,
                                              pro_cat_id=pro_cat,
                                              pro_brand=pro_brand,
                                              pro_price=pro_price,
                                              pro_price_currency_id=pro_price_ciurrency,
                                              online_pro_qty=online_pro_qty,
                                              offline_pro_qty=offline_pro_qty,
                                              pro_vat=pro_vat,
                                              pro_weight=pro_weight,
                                              pro_desc=pro_details,
                                              pro_spec=pro_specification,
                                              pro_shipping_price=pro_shipping_price,
                                              pro_cod=pro_cod,
                                              pro_exchange_offer=pro_exchange_period,
                                              pro_featured=pro_featured,
                                              pro_status=0,
                                              pro_add_date=today_date)
            for s in range(len(pro_image)):
                sq = Productimage.objects.create(pro_id=qs.id,
                                                 bo_id=pro_bo,
                                                 pro_image=pro_image[s],
                                                 featured_image=featured_image[s],
                                                 image_added_by=operator_id)

            pa = Productquantity_history.objects.create(pro_id=qs.id, online_qty=online_pro_qty,offline_qty=offline_pro_qty)
            pp = Productprice_history.objects.create(pro_id=qs.id, price=pro_price)

            log_stmt = Log_conversation.objects.create(content_id=qs.id, content_table='product_master',
                                                       operation='Insert',
                                                       operator_id=operator_id, operator_type='', operation_lang=lang)
            return HttpResponse('Operation perform successfully.')



    else:
        bo_id = request.session['id']
        print(bo_id)
        slt_stmt = Productmaster.objects.filter(pro_bo_id=bo_id)
        pro_count = len(slt_stmt)
        # get subscription plan details

        # get subscription plan details end

        # get currency start
        currency_data = []
        cu_stmt = Currency.objects.all().values('id','country_name','currency','currency_code')
        if cu_stmt:
            for cu_stmt in cu_stmt:
                cur_dict = {}
                cur_dict['id'] = cu_stmt['id']
                cur_dict['currency_name'] = cu_stmt['country_name']
                cur_dict['currency'] = cu_stmt['currency']
                cur_dict['currency_code'] = cu_stmt['currency_code']
                currency_data.append(cur_dict)

        # get currency end

        bo_data = []
        bo_stmt = CustomUser.objects.filter(is_active=True).values('id','email','username')
        if bo_stmt:
            for bo_stmt1 in bo_stmt:
                stmt_dict = {}
                stmt_dict['bo_id'] = bo_stmt1['id']
                stmt_dict['bo_email'] =  bo_stmt1['email']
                stmt_dict['bo_username'] =  bo_stmt1['username']
                bo_data.append(stmt_dict)


        data = []
        qs = Category_Master.objects.all().values('id', 'category_parent_child_id')
        if qs:
            for qs1 in qs:
                dict = {}
                arr = [int(x) for x in qs1['category_parent_child_id'].split(',')]
                qs2 = Category_Master.objects.filter(id__in=arr)
                output = "-->".join(q.category_name for q in qs2)
                dict['id'] = qs1['id']
                dict['category_display'] = output
                data.append(dict)

    return render(request,'product_bank.html',{'category': data,'bo_data':bo_data, 'pro_count':pro_count,'currency_data':currency_data})

@login_required
def get_product_list(request):
    start = request.GET.get('start')
    last = request.GET.get('length')
    value = request.GET.get('search')
    drop = request.GET.get('search')
    proname = request.GET.get('proname')
    procategory = request.GET.get('procategory')
    probo = request.GET.get('probo')
    prostatus = request.GET.get('prostatus')
    if value != 'none':
        if drop == 'name':
            q_object = Q(pro_name__icontains=proname)
        elif drop == 'category':
            q_object = Q(pro_cat_id=procategory)
        elif drop == 'boname':
            q_object = Q(pro_bo_id=probo)
        elif drop == 'status':
            q_object = Q(pro_status=prostatus)

        slt_stmt = Productmaster.objects.filter(q_object)[int(start):(int(last) + int(start))]
        cq = Productmaster.objects.filter(q_object).annotate(number_of_entries=Count('id'))
        slt_count = len(cq)

    else:
        slt_stmt = Productmaster.objects.all()[int(start):(int(last) + int(start))]
        cq = Productmaster.objects.annotate(number_of_entries=Count('id'))
        slt_count = len(cq)
    doc_list1 = []
    inc = int(start) + 1
    for i in slt_stmt:
        doc_list = []
        doc_list.append(inc)
        doc_list.append(i.pro_bo_sku)

        pro_gallery = Productimage.objects.filter(Q(pro_id=int(i.id)) &
                                                  Q(featured_image=True)).values('pro_image')
        if pro_gallery:
            img = pro_gallery[0]['pro_image']
            doc_list.append('<img width="50px" src="/media/' + str(
                img) + '">' + ' ' + '<a href="#" style="color: #1827d6;" id="view_img" onclick="view_data(' + str(
                i.id) + ')">' + i.pro_name + '</a>')

        else:
            doc_list.append('<a href="#" style="color: #1827d6;" id="view_img" onclick="view_data(' + str(
                i.id) + ')">' + i.pro_name + '</a>')

        #doc_list.append(i.pro_name)
        pro_gallery = Productimage.objects.filter(pro_id=int(i.id)).values('pro_image')

        if pro_gallery:
            img = pro_gallery[0]['pro_image']
            doc_list.append('<img width="30px" src="/media/' + str(img) + '">')
        else:
            doc_list.append('<img width="30px" src="">')

        category = Category_Master.objects.filter(id=i.pro_cat_id).values('id','category_name')
        doc_list.append(category[0]['category_name'])
        doc_list.append(i.online_pro_qty)
        doc_list.append(i.offline_pro_qty)
        doc_list.append(i.pro_price)
        currency_stmt = Currency.objects.filter(id=i.pro_price_currency_id).values('currency_code')
        doc_list.append(currency_stmt[0]['currency_code'])
        doc_list.append(i.pro_vat)
        bo_name = CustomUser.objects.filter(id=i.pro_bo_id).values('username')
        if bo_name:
            doc_list.append(bo_name[0]['username'])
        else:
            doc_list.append('')
        doc_list.append(i.pro_add_date)

        if i.pro_status == 0:
            doc_list.append('<div class="btn-group btn-group-sm" role="group" aria-label="Basic example">'
                            '<button type="button" class="btn btn-secondary"'
                            'onclick="change_status(' + str(i.id) + ')">Publish</button>'
                            '<button type="button" class="btn btn-primary"'
                            'onclick="change_status(' + str(i.id) + ')">Unpublish</button></div>')
        else:
            doc_list.append('<div class="btn-group btn-group-sm" role="group" aria-label="Basic example">'
                            '<button type="button" class="btn btn-primary"'
                            'onclick="change_status(' + str(i.id) + ')">Publish</button>'
                            '<button type="button" class="btn btn-secondary"'
                            'onclick="change_status(' + str(i.id) + ')">Unpublish</button></div>')

        doc_list.append('<a href="javascript:void(0)" title="Edit Peoduct"><i id="product_edit" onclick="edit_product(' + str(i.id) +
                        ')" class="fa fa-pencil-square-o fa-lg" aria-hidden="true"></i></a>&nbsp;'
                        '<a href="javascript:void(0)" title="Delete Peoduct"><i id="product_delete" onclick="delete_product(' + str(i.id) +
                        ')" class="fa fa-trash-o fa-lg" aria-hidden="true"></i></a>')
        doc_list1.append(doc_list)
        inc += 1

    data = {'draw': request.GET.get('draw'), 'recordsTotal': slt_count, 'recordsFiltered': slt_count, 'data': doc_list1}
    return JsonResponse(data)

@login_required
@csrf_exempt
def get_filter_list(request):
    value = request.GET.get('id')
    slt_stmt = Filter_Master.objects.filter(category_id=int(value))

    doc_list = []
    inc = 1
    for i in slt_stmt:
        doc_dict = {}
        filter_value = Filter_Value_Master.objects.filter(filter_id=i.id)
        print(filter_value)
        option = ''
        if filter_value:
            for j in filter_value:
                option = option + '<option value="'+str(j.id)+'">' + j.filter_value + '</option>'
        doc_dict['attr_value']= option
        doc_dict['attr_name']= i.filter_name
        doc_dict['attr_id']= i.id

        doc_list.append(doc_dict)
        inc += 1

   # print(doc_list)

    data = {'data': doc_list}
    return JsonResponse(data)

@login_required
def edit_product(request):
    id = request.GET.get('id')
    qs = Productmaster.objects.filter(id=int(id))
    doc_list = []
    for i in qs:
        doc_dict = {}
        doc_dict['product_bo'] = i.pro_bo_id
        doc_dict['product_name'] = i.pro_name
        doc_dict['product_sku'] = i.pro_bo_sku
        doc_dict['product_cat_id'] = i.pro_cat_id
        doc_dict['product_price'] = i.pro_price
        doc_dict['online_product_qty'] = i.online_pro_qty
        doc_dict['offline_product_qty'] = i.offline_pro_qty
        doc_dict['pro_price_currency'] = i.pro_price_currency_id
        doc_dict['product_vat'] = i.pro_vat
        doc_dict['product_weight'] = i.pro_weight
        doc_dict['product_desc'] = i.pro_desc
        doc_dict['product_spec'] = i.pro_spec
        doc_dict['product_shipping_price'] = i.pro_shipping_price
        doc_dict['product_cod'] = i.pro_cod
        doc_dict['product_exchange_period'] = i.pro_exchange_offer
        doc_dict['product_featured'] = i.pro_featured
        doc_dict['pro_id'] = i.id
        doc_list.append(doc_dict)

    doc_list2 = []
    qs2 = Productimage.objects.filter(pro_id=int(id))
    for i in qs2:
        doc_dict = {}
        doc_dict['gall_id'] = i.id
        doc_dict['featured_image'] = str(i.featured_image)
        doc_dict['product_img'] = str(i.pro_image)
        doc_list2.append(doc_dict)


    doc_list1 = []
    qs1 = Productattributs_values.objects.filter(pro_id=int(id))
    for i in qs1:
        doc_dict = {}
        doc_dict['attr_id'] = i.attr_id
        a = Filter_Master.objects.filter(id=i.attr_id).values('filter_name')
        doc_dict['attr_val'] = a[0]['filter_name']
        doc_dict['attr_unit'] = i.attr_unit
        doc_dict['attr_qty'] = i.quantity
        doc_list1.append(doc_dict)

    data_json = {
        'product_list': doc_list,
        'product_gall': doc_list2,
        'product_attr': doc_list1,

    }

    return JsonResponse(data_json)


@login_required
def delete_product(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        Productmaster.objects.filter(id=int(id)).delete()
        Productimage.objects.filter(pro_id=int(id)).delete()
        Productattributs_values.objects.filter(pro_id=int(id)).delete()
        operator_id=request.session['id']
        lang = request.session["cu_language"]
        user_type = request.session['user_type']
        log_stmt = Log_conversation.objects.create(content_id=id, content_table='Productmaster', operation='Delete',
                                                   operator_id=operator_id, operator_type=user_type, operation_lang=lang)
        return HttpResponse('Deleted Successfullly.')


@login_required
def change_status(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        print("hello")
        print(id)
        qs = Productmaster.objects.filter(id=int(id)).values('pro_status')

        if qs[0]['pro_status'] == 0:
            Productmaster.objects.filter(id=int(id)).update(pro_status=1)
            is_success = 1
        else:
            Productmaster.objects.filter(id=int(id)).update(pro_status=0)
            is_success = 0

        return HttpResponse(is_success)

@login_required
@csrf_exempt
def getattributename(request):
    if request.method == 'GET':
        attrname = request.GET.get('attrname')
        catid = request.GET.get('catid')

        # get attr start
        value = request.GET.get('catid')
        slt_stmt = Filter_Master.objects.filter(Q(category_id=int(value)) &
                                                           Q(filter_name__icontains=attrname))
        doc_list = []
        inc = 1
        for i in slt_stmt:
            doc_dict = {}
            doc_dict['attr_name'] = i.filter_name
            doc_dict['id'] = i.id

            doc_list.append(doc_dict)
            inc += 1

        # print(doc_list)

        data = {'data': doc_list}
        # get atttr end

        data_json = {}
        return JsonResponse(data)

def getattributevalue(request):
    if request.method == 'GET':
        attrid = request.GET.get('attrid')
        catid = request.GET.get('catid')

       # slt_stmt = Filter_Master.objects.filter(category_id=int(value))
        slt_stmt = Filter_Master.objects.filter(Q(category_id=int(catid)) &
                                                Q(id=attrid))

        doc_list = []
        inc = 1
        for i in slt_stmt:
            doc_dict = {}
            filter_value = Filter_Value_Master.objects.filter(filter_id=i.id)
            print(filter_value)
            option = ''
            if filter_value:
                for j in filter_value:
                    option = option + '<option value="' + str(j.id) + '">' + j.filter_value + '</option>'
            doc_dict['attr_value'] = option
            doc_list.append(doc_dict)
            inc += 1

        data = {'data': doc_list}
        return JsonResponse(data)


class ProductViewSet(APIView):

    def get(self, request, pro_cat_id=None):
        if pro_cat_id == None:
            queryset = Productmaster.objects.all()
        else:
            queryset = Productmaster.objects.filter(pro_cat_id=pro_cat_id)

        serializer_class = ProductInfoSerializer(queryset, many=True)

        return Response(serializer_class.data, status=status.HTTP_200_OK)
