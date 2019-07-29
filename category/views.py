from django.shortcuts import render
from category.models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.db.models import Q


def category(request):
    user_type = request.session['user_type']
    id = request.session['id']

    filter_data = Filter_Master.objects.all()
    return render(request, 'category.html', {'filter_data': filter_data})


def category_list(request):
    category_data = Category_Master.objects.all()
    data_list = []
    for i in category_data:
        data_dic = {}
        data_dic['id'] = i.id
        data_dic['category_name'] = i.category_name
        data_dic['category_description'] = i.category_description
        if i.category_parent_id == 0:
            data_dic['category_parent_id'] = ''
        else:
            qs = Category_Master.objects.filter(id=int(i.category_parent_id)).values('category_name')
            data_dic['category_parent_id'] = qs[0]['category_name']
        data_list.append(data_dic)

    return render(request, 'category_list.html', {'category_data': data_list})


def get_category_list(request):
    user_type = request.session['user_type']
    id = request.session['id']

    start = request.GET.get('start')
    last = request.GET.get('length')
    value = request.GET.get('search')

    if value != 'none':
        slt_stmt = Category_Master.objects.filter(category_name__icontains=value)[int(start):(int(last)+int(start))]
        slt_count_temp = Category_Master.objects.filter(category_name__icontains=value)
        slt_count = len(slt_count_temp)
    else:
        slt_stmt = Category_Master.objects.all()[int(start):(int(last)+int(start))]
        slt_count_temp = Category_Master.objects.all()
        slt_count = len(slt_count_temp)
    doc_list1 = []
    inc = int(start)+1
    for i in slt_stmt:
        doc_list = []
        doc_list.append(str(inc) + '<input type="hidden" class="get-child" '
                                   'value="' + str(i.id) + '" readonly>')

        cat_gallery = Category_Gallery.objects.filter(Q(category_id=i.id) &
                                                      Q(category_featured_img=True)).values('category_image')
        if cat_gallery:
            img = cat_gallery[0]['category_image']
            doc_list.append('<img width="50px" src="/media/' + str(img) + '">' + ' ' +
                            '<a href="#" style="color: #1827d6;" id="view_img" onclick="view_data(' + str(i.id) +
                            ')">' + i.category_name + '</a>')
        else:
            doc_list.append('<a href="#" style="color: #1827d6;" id="view_img" onclick="view_data(' + str(i.id) +
                            ')">' + i.category_name + '</a>')

        doc_list.append('<a href="#" style="color: #1827d6;" id="view_img" onclick="get_img(' + str(i.id) +
                        ')">View Images</a>')

        if len(i.category_description) > 50:
            doc_list.append('<a data-toggle="collapse" data-target="#demo" '
                            'data-toggle="tooltip" title="' + i.category_description +
                            '">' + i.category_description[0:50] + '...</a>')
        else:
            doc_list.append('<a data-toggle="collapse" data-target="#demo"'
                            'data-toggle="tooltip" title="' + i.category_description +
                            '">' + i.category_description + '</a>')

        if i.category_parent_id == 0:
            doc_list.append('')
        else:
            cat_child_id = [x for x in i.category_parent_child_id.split(',')]
            qs2 = Category_Master.objects.filter(id__in=cat_child_id)
            output = "-->".join(q.category_name for q in qs2)
            if len(i.category_description) > 50:
                doc_list.append('<a data-toggle="tooltip"  title="' + output +
                                '">' + output[0:50] + '...</a>')
            else:
                doc_list.append('<a data-toggle="tooltip"  title="' + output +
                                '">' + output + '</a>')

        doc_list.append('<div class="action-area">'
                        '<a href="#"><i id="category_edit" '
                        'data-toggle="tooltip" data-placement="top" title="Edit Category"'
                        'onclick="set_modal_id(' + str(i.id) +
                        ')" class="fa fa-pencil-square-o fa-lg" aria-hidden="true"></i></a>'
                        '<a href="#"><i id="category_delete" '
                        'data-toggle="tooltip" data-placement="top" title="Delete Category"'
                        'onclick="delete_category(' + str(i.id) +
                        ')" class="fa fa-trash-o fa-lg" aria-hidden="true"></i></a>'                        
                        '<a href="#"><i id="category_view_filter" '
                        'data-toggle="tooltip" data-placement="top" title="View Filter"'
                        'onclick="view_filter(' + str(i.id) +
                        ')" class="fa fa-eye fa-lg" aria-hidden="true"></i></a>'
                        '</div>')

        doc_list1.append(doc_list)

        '''doc_list = []

        doc_list.append('<div id="demo" class="collapse sub-product-area">'
                        '<table class="table mb-0">'
                        '<tbody>'
                        '<tr data-toggle="collapse" data-target="#demo1">'
                        '<td scope="row">1</td>'
                        '<td>ABC </td>'
                        '<td>Lorem Ipsum is simply dummy text of the printing and typesetting industry.</td>'
                        '<td>Time period for Expiry</td>'
                        '<td>200 SAR</td>'
                        '<td>'
                        '<div class="action-area">'
                        '<div class="form-group">'
                        '<a href="#"><i class="fa fa-pencil-square-o fa-lg" aria-hidden="true"></i></a>'
                        '<a href="#"><i class="fa fa-trash-o fa-lg" aria-hidden="true"></i></a>'
                        '</div>'
                        '</div>'
                        '</td>'
                        '</tr>'
                        '<tr>'
                        '<td style="    padding: 0px !important;" colspan="6">'
                        '<div id="demo1" class="collapse sub-product-area">'
                        '<table class="table mb-0">'
                        '<tbody>'
                        '<tr>'
                        '<td scope="row">1</td>'
                        '<td>ABC </td>'
                        '<td>Lorem Ipsum is simply dummy text of the printing and typesetting industry.</td>'
                        '<td>Time period for Expiry</td>'
                        '<td>200 SAR</td>'
                        '<td>'
                        '<div class="action-area">'
                        '<div class="form-group">'
                        '<a href="#"><i class="fa fa-pencil-square-o fa-lg" aria-hidden="true"></i></a>'
                        '<a href="#"><i class="fa fa-trash-o fa-lg" aria-hidden="true"></i></a>'
                        '</div>'
                        '</div>'
                        '</td>'
                        '</tr><tr><td scope="row">8</td>'
                        '<td>ABC </td><td>Lorem Ipsum is simply dummy text of the printing and typesetting industry.</td>'
                        '<td>Time period for Expiry</td>'
                        '<td>200 SAR</td>'
                        '<td>'
                        '<div class="action-area">'
                        '<div class="form-group">'
                        '<a href="#"><i class="fa fa-pencil-square-o fa-lg" aria-hidden="true"></i></a>'
                        '<a href="#"><i class="fa fa-trash-o fa-lg" aria-hidden="true"></i></a>'
                        '</div>'
                        '</div>'
                        '</td>'
                        '</tr>'
                        '</tbody>'
                        '</table>'
                        '</div></td></tr>'
                        '<tr>'
                        '<td scope="row">8</td><td>ABC </td>'
                        '<td>Lorem Ipsum is simply dummy text of the printing and typesetting industry.</td>'
                        '<td>Time period for Expiry</td>'
                        '<td>200 SAR</td>'
                        '<td><div class="action-area"><div class="form-group">'
                        '<a href="#"><i class="fa fa-pencil-square-o fa-lg" aria-hidden="true"></i></a>'
                        '<a href="#"><i class="fa fa-trash-o fa-lg" aria-hidden="true"></i></a>'
                        '</div></div></td></tr></tbody></table></div>')'''

        inc += 1

    data = {'draw': request.GET.get('draw'), 'recordsTotal': slt_count, 'recordsFiltered': slt_count, 'data': doc_list1}
    return JsonResponse(data)


def get_category(request):
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

    return HttpResponse(json.dumps(data))


def category_operations(request):
    todayDateTime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    user_type = request.session['user_type']
    id = request.session['id']

    if request.method == 'POST':
        form = request.POST
        form1 = request.FILES

        print(form)
        print(form1)

        saved_id = form.get('saved_id')

        category = form.get('category')
        category_name = form.get('category_name')
        category_description = form.get('category_description')
        files = form1.getlist('upload_files[]')
        featured_img = form.getlist('featured_img[]')

        if saved_id:
            Category_Master.objects.filter(id=int(saved_id)).update(category_name=category_name,
                                                                    category_description=category_description,
                                                                    category_parent_id=category,
                                                                    category_user_type='Admin',
                                                                    category_updated_at=todayDateTime,
                                                                    category_updated_by=0)

            if category == '0':
                Category_Master.objects.filter(id=int(saved_id)).update(category_parent_child_id=int(saved_id))

            else:
                pc = Category_Master.objects.filter(id=int(category)).values('category_parent_child_id')
                Category_Master.objects.filter(id=int(saved_id)).update(category_parent_child_id=(str(pc[0]['category_parent_child_id'])
                                                                                                  + ',' + str(saved_id)))
            for i in range(len(files)):
                Category_Gallery.objects.create(category_id=int(saved_id), category_image=files[i])

            img_list = Category_Gallery.objects.filter(category_id=int(saved_id))
            count = 0

            for i in img_list:
                Category_Gallery.objects.filter(id=i.id).update(category_featured_img=featured_img[count])
                count += 1

        else:
            qs = Category_Master.objects.create(category_name=category_name,
                                                category_description=category_description,
                                                category_parent_id=category,
                                                category_user_type='Admin',
                                                category_created_by=0)

            if category == '0':
                Category_Master.objects.filter(id=qs.id).update(category_parent_child_id=qs.id)

            else:
                pc = Category_Master.objects.filter(id=int(category)).values('category_parent_child_id')
                Category_Master.objects.filter(id=qs.id).update(category_parent_child_id=(str(pc[0]['category_parent_child_id'])
                                                                                          + ',' + str(qs.id)))

            for i in range(len(files)):
                Category_Gallery.objects.create(category_id=qs.id, category_image=files[i],
                                                category_featured_img=featured_img[i])

        data_json = {
            'msg': 'Operation performed successfully'
        }

        return JsonResponse(data_json)


def get_saved_category(request):
    id = request.GET.get('id')
    data = []
    data1 = []
    qs = Category_Master.objects.filter(id=id)
    for i in qs:
        dict = {}
        dict['category_name'] = i.category_name
        dict['category_description'] = i.category_description
        dict['category_parent_id'] = i.category_parent_id
        data.append(dict)

    qs1 = Category_Gallery.objects.filter(category_id=id)
    for i in qs1:
        dict = {}
        dict['img_id'] = i.id
        dict['category_featured_img'] = i.category_featured_img
        dict['category_image'] = str(i.category_image)
        data1.append(dict)

    data_json = {
        'cat_list': data,
        'gal_list': data1,
    }

    return JsonResponse(data_json)


def category_delete(request):
    if request.method == 'GET':
        id = request.GET.get('id')

        try:
            Category_Master.objects.filter(id=int(id)).delete()
        except Exception as e:
            print(e)
            is_success = 0
        else:
            is_success = 1

        return HttpResponse(is_success)


def get_saved_img(request):
    id = request.GET.get('id')
    data = []
    qs = Category_Gallery.objects.filter(category_id=id)
    if qs:
        for i in qs:
            dict = {}
            dict['img_id'] = str(i.id)
            dict['category_image'] = str(i.category_image)
            data.append(dict)

    data_json = {
        'cat_gal_list': data,
    }

    return JsonResponse(data_json)


def del_img(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        Category_Gallery.objects.filter(id=int(id)).delete()
        return HttpResponse('Deleted successfully')


def get_filter_list(request):
    user_type = request.session['user_type']
    id = request.session['id']

    start = request.GET.get('start')
    last = request.GET.get('length')
    value = request.GET.get('category_id')
    if value != '':
        slt_stmt = Filter_Master.objects.filter(category_id=int(value))[int(start):(int(last)+int(start))]
        slt_count_temp = Filter_Master.objects.filter(category_id=int(value))
        slt_count = len(slt_count_temp)
    else:
        slt_stmt = Filter_Master.objects.all()[int(start):(int(last) + int(start))]
        slt_count_temp = Filter_Master.objects.all()
        slt_count = len(slt_count_temp)
    doc_list1 = []
    inc = int(start)+1
    for i in slt_stmt:
        doc_list = []
        filter_value = Filter_Value_Master.objects.filter(filter_id=i.id)
        option = ''
        if filter_value:
            for j in filter_value:
                option = option + '<option>' + j.filter_value + '</option>'
        doc_list.append(inc)
        doc_list.append(i.filter_name)
        if filter_value:
            doc_list.append('<select id=filter_value_id class="form-control">'
                            + option +
                            '</select>')
        else:
            doc_list.append('<select id=filter_value_id class="form-control">'
                            '<option value="">None</option>' 
                            '</select>')
        if i.filter_status:
            doc_list.append('Approved <i class="fa fa-check" aria-hidden="true" '
                            'title="Approved -> Reject It" '
                            'onclick="reject_approved(' + str(i.id) +
                            ')" style="color: green; cursor: pointer;"></i>')
        else:
            doc_list.append('Pending <i class="fa fa-times" aria-hidden="true" '
                            'title="Pending -> Approved It" '
                            'onclick="approve_rejected(' + str(i.id) +
                            ')" style=" cursor: pointer;"></i>')

        doc_list.append('<div class="action-area">'
                        '<a href="#"><i id="filter_edit" '
                        'data-toggle="tooltip" data-placement="top" title="Edit Filter"'
                        'onclick="set_edit_modal_id(' + str(i.id) +
                        ')" class="fa fa-pencil-square-o fa-lg" aria-hidden="true"></i></a>'
                        '<a href="#"><i id="filter_delete" '
                        'data-toggle="tooltip" data-placement="top" title="Delete Filter"'
                        'onclick="delete_filter(' + str(i.id) +
                        ')" class="fa fa-trash-o fa-lg" aria-hidden="true"></i></a>'
                        '<a href="#"><i id="add_filter_value" '
                        'data-toggle="tooltip" data-placement="top" title="Add Filter Value"'
                        'onclick="add_filter_value(' + str(i.id) +
                        ')" class="fa fa-plus fa-lg" aria-hidden="true"></i></a>'
                        '<a href="#"><i id="filter_value_list" '
                        'data-toggle="tooltip" data-placement="top" title="Filter Value List"'
                        'onclick="filter_value_list(' + str(i.id) +
                        ')" class="fa fa-list fa-lg" aria-hidden="true"></i></a>'
                        '</div>')

        doc_list1.append(doc_list)
        inc += 1

    data = {'draw': request.GET.get('draw'), 'recordsTotal': slt_count, 'recordsFiltered': slt_count, 'data': doc_list1}
    return JsonResponse(data)


def filter_operations(request):
    todayDateTime = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    user_type = request.session['user_type']
    id = request.session['id']

    if request.method == 'POST':
        form = request.POST

        category_saved_id = form.get('category_saved_id')
        id_type = form.get('id_type')
        filter_name = form.get('filter_name')

        if id_type == 'category_id':

            qs = Filter_Master.objects.create(filter_name=filter_name,
                                              filter_status=True,
                                              category_id=category_saved_id,
                                              filter_user_type='Admin',
                                              filter_created_by=0)

        else:

            Filter_Master.objects.filter(id=category_saved_id).update(filter_name=filter_name,
                                                                      filter_user_type='Admin',
                                                                      filter_updated_at=todayDateTime,
                                                                      filter_updated_by=0)

        data_json = {
            'msg': 'Operation performed successfully'
        }

        return JsonResponse(data_json)


def get_saved_filter(request):
    id = request.GET.get('id')
    data = []
    qs = Filter_Master.objects.filter(id=id)
    if qs:
        for i in qs:
            dict = {}
            dict['filter_name'] = i.filter_name
            data.append(dict)

    return HttpResponse(json.dumps(data))


def filter_delete(request):
    if request.method == 'GET':
        id = request.GET.get('id')

        try:
            Filter_Master.objects.filter(id=int(id)).delete()
        except Exception as e:
            print(e)
            is_success = 0
        else:
            is_success = 1

        return HttpResponse(is_success)


def get_filter_value_list(request):
    user_type = request.session['user_type']
    id = request.session['id']

    start = request.GET.get('start')
    last = request.GET.get('length')
    value = request.GET.get('filter_id')
    if value != '':
        slt_stmt = Filter_Value_Master.objects.filter(filter_id=int(value))[int(start):(int(last)+int(start))]
        slt_count_temp = Filter_Value_Master.objects.filter(filter_id=int(value))
        slt_count = len(slt_count_temp)
    else:
        slt_stmt = Filter_Value_Master.objects.all()[int(start):(int(last) + int(start))]
        slt_count_temp = Filter_Value_Master.objects.all()
        slt_count = len(slt_count_temp)
    doc_list1 = []
    inc = int(start)+1
    for i in slt_stmt:
        doc_list = []
        doc_list.append(inc)
        doc_list.append(i.filter_value)

        doc_list.append('<div class="action-area">'
                        '<a href="#"><i id="filter_edit" '
                        'data-toggle="tooltip" data-placement="top" title="Edit Filter"'
                        'onclick="set_filter_value_modal_id(' + str(i.id) +
                        ')" class="fa fa-pencil-square-o fa-lg" aria-hidden="true"></i></a>'
                        '<a href="#"><i id="filter_delete" '
                        'data-toggle="tooltip" data-placement="top" title="Delete Filter"'
                        'onclick="delete_filter_value(' + str(i.id) +
                        ')" class="fa fa-trash-o fa-lg" aria-hidden="true"></i></a>'
                        '</div>')

        doc_list1.append(doc_list)
        inc += 1

    data = {'draw': request.GET.get('draw'), 'recordsTotal': slt_count, 'recordsFiltered': slt_count, 'data': doc_list1}
    return JsonResponse(data)


def filter_value_operations(request):
    user_type = request.session['user_type']
    id = request.session['id']

    if request.method == 'POST':
        form = request.POST

        filter_type_id = form.get('filter_type_id')
        filter_saved_id = form.get('filter_saved_id')
        filter_value = form.get('filter_value_name')

        if filter_type_id == 'filter_id':
            qs = Filter_Value_Master.objects.create(filter_value=filter_value,
                                                    filter_id=filter_saved_id)
        else:
            Filter_Value_Master.objects.filter(id=filter_saved_id).update(filter_value=filter_value)

        data_json = {
            'msg': 'Operation performed successfully'
        }

        return JsonResponse(data_json)


def get_saved_filter_values(request):
    id = request.GET.get('id')
    data = []
    qs = Filter_Value_Master.objects.filter(id=int(id))
    if qs:
        for i in qs:
            dict = {}
            dict['filter_value'] = i.filter_value
            data.append(dict)

            print(data)

    return HttpResponse(json.dumps(data))


def filter_value_delete(request):
    if request.method == 'GET':
        id = request.GET.get('id')

        try:
            Filter_Value_Master.objects.filter(id=int(id)).delete()
        except Exception as e:
            print(e)
            is_success = 0
        else:
            is_success = 1

        return HttpResponse(is_success)


def approve_filter(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        qs = Filter_Master.objects.filter(id=int(id)).update(filter_status=True)
        return HttpResponse('Approved Successfullly.')


def reject_filter(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        qs = Filter_Master.objects.filter(id=int(id)).update(filter_status=False)
        return HttpResponse('Reject Successfullly.')
