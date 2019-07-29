from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
#from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import CustomUser, VerificationCode
import socket
from common.views import *
from common.models import *
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time
from datetime import timedelta
import base64
import urllib

# Create your views here.


# def index(request):
#     return render(request,'verification.html')


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))


def verification(request):
    if request.method == 'POST':
        form = request.POST
        verification_code_1 = form.get('verification_code_1')
        verification_code_2 = form.get('verification_code_2')
        verification_code_3 = form.get('verification_code_3')
        verification_code_4 = form.get('verification_code_4')

        user_name = form.get('user_id')
        verify = VerificationCode.objects.filter(user_id=user_name).values('verification_code', 'start_time',
                                                                           'end_time', 'verification_status')

        print(verify)
        end_time = verify[0]['end_time']
        print(end_time)
        date_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        pattern = '%Y-%m-%d %H:%M:%S'
        current_time = int(time.mktime(time.strptime(date_time, pattern)))
        verification_code = verify[0]['verification_code']
        verification_code_first = verification_code[0]
        verification_code_second = verification_code[1]
        verification_code_third = verification_code[2]
        verification_code_fourth = verification_code[3]

        if (verification_code_1 == verification_code_first and verification_code_2 == verification_code_second and
            verification_code_3 == verification_code_third and verification_code_4 == verification_code_fourth and
            current_time < int(end_time)):

            VerificationCode.objects.filter(user_id=user_name).update(verification_status=1)

            CustomUser.objects.filter(username=user_name).update(is_active=True)

            data_json = {
                'id': 1,
                'msg': 'verification successful'
            }

            return JsonResponse(data_json)

        else:

            data_json = {
                'id': 0,
                'msg': 'verification failed',
            }

            return JsonResponse(data_json)

    else:
        userid = request.GET.get('userid')

    return render(request, 'verification.html', {'userid': userid})


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def sendemail_verification(request, emailid, user_id):
    sender_email = "some@gmail.com"
    receiver_email = emailid
    password = 'xxxxxxx'

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email

    set = '1234567890'
    gen_text = ''.join((random.choice(set)) for i in range(4))

    date_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    pattern = '%Y-%m-%d %H:%M:%S'
    verify_start_date = int(time.mktime(time.strptime(date_time, pattern)))
    verify_end_date = int(verify_start_date) + (10 * 60)

    VerificationCode.objects.create(user_id=user_id, verification_code=gen_text, start_time=verify_start_date,
                                    end_time=verify_end_date)

    # Create the plain-text and HTML version of your message
    text = """\
    Dear Customer,
    You have register successfully. Click <a href="http://127.0.0.1:8000/accounts/verification/" style="color:green;">here</a>  to verify your accunt.
    Thanks & Regards:
    Fynoo Team
    www.fynoo.com"""
    html = """\
    <html>
      <body>
        <p>Dear Customer,<br>
           """+gen_text+""" is the One Time Password (OTP) for account verification.<br />
           Click <a href="http://127.0.0.1:8000/accounts/verification/" style="color:green;">here</a> to verify your account.<br>
           Thanks & Regards <br />
           Fynoo Team
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

    return render(request, 'verification.html')


def resendemail_verification(request, emailid, user_id):
    sender_email = "some@gmail.com"
    receiver_email = emailid
    password = 'xxxxxxx'

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email

    set = '1234567890'
    gen_text = ''.join((random.choice(set)) for i in range(4))

    date_time = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    pattern = '%Y-%m-%d %H:%M:%S'
    verify_start_date = int(time.mktime(time.strptime(date_time, pattern)))
    verify_end_date = int(verify_start_date) + (10 * 60)

    VerificationCode.objects.filter(user_id=user_id).update(verification_code=gen_text, start_time=verify_start_date,
                                                            end_time=verify_end_date)

    # Create the plain-text and HTML version of your message
    text = """\
    Dear Customer,
    You have register successfully. Click <a href="http://127.0.0.1:8000/accounts/verification/" style="color:green;">here</a>  to verify your accunt.
    Thanks & Regards:
    Fynoo Team
    www.fynoo.com"""
    html = """\
    <html>
      <body>
        <p>Dear Customer,<br>
           """+gen_text+""" is the One Time Password (OTP) for account verification.<br />
           Click <a href="http://127.0.0.1:8000/accounts/verification/" style="color:green;">here</a> to verify your account.<br>
           Thanks & Regards <br />
           Fynoo Team
        </p>
      </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )

    return render(request, 'verification.html')


def register(request):
    if request.method == 'POST':
        form = request.POST
        form1 = request.FILES

        created_by = 'Admin'
        active = False
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)

        if 'bo_userid' in request.POST:
            userid = form.get('bo_userid')
            name = form.get('bo_name')
            country = form.get('bo_country')
            city = form.get('bo_city')
            mob_country_code = form.get('bo_cm_code')
            mobile_no = form.get('bo_mobile')
            email = form.get('bo_email')
            password = form.get('bo_password')
            user_type = form.get('user_type_bo')
            boid = form.get('boid')

            if boid:
                CustomUser.objects.filter(id=int(boid)).update(username=userid, name=name, email=email,
                                                               mobile_code=mob_country_code, mobile_number=mobile_no,
                                                               password=password, country_id=country, city_id=city)

                data_json = {
                    'id': boid,
                    'msg': 'User Updated Successfully',
                }

                return JsonResponse(data_json)

            else:
                if not CustomUser.objects.filter(username=userid).exists() | CustomUser.objects.filter(
                        email=email).exists():
                    CustomUser.objects.create_user(fynoo_id='F101', username=userid, name=name, email=email,
                                                   mobile_code=mob_country_code, mobile_number=mobile_no,
                                                   password=password, country_id=country, city_id=city,
                                                   created_by=created_by, systemip=IPAddr, system_name=hostname,
                                                   user_type=user_type)

                    sendemail_verification(request, email, userid)

                    data_json = {
                        'id': 1,
                        'msg': 'BO created successfully',
                        'userid': userid,
                    }

                    return JsonResponse(data_json)

                else:
                    data_json = {
                        'id': 0,
                        'msg': 'Username or Email Already exists',
                    }

                    return JsonResponse(data_json)

        if 'ai_userid' in request.POST:
            ai_userid = form.get('ai_userid')
            ai_gender = form.get('ai_gender')
            ai_dob = form.get('ai_dob')
            ai_education = form.get('ai_education')
            ai_major = form.get('ai_major')
            ai_country = form.get('ai_country')
            ai_city = form.get('ai_city')
            ai_mobile_no = form.get('ai_mobile')
            ai_email = form.get('ai_email')
            ai_password = form.get('ai_password')
            ai_bank_name = form.get('ai_bankname');
            ai_iban_no = form.get('ai_iban')
            ai_maroof_link = form.get('ai_marooflink')
            ai_ai_img = form1.get('agent_image')
            aid = form.get('aid')
            ai_user_type = form.get('user_type_ai')

            if aid:
                CustomUser.objects.filter(id=int(aid)).update(mobile_number=ai_mobile_no, country_id=ai_country,
                                                              city_id=ai_city, email=ai_email, gender=ai_gender, dob=ai_dob,
                                                              education=ai_education, major=ai_major, bank_name=ai_bank_name,
                                                              iban_no=ai_iban_no, maroof_link=ai_maroof_link)

                if ai_ai_img != '':
                    qs = CustomUser.objects.get(id=int(aid))
                    qs.profile_image = request.FILES['agent_image']
                    qs.save()

                    data_json = {
                        'id': aid,
                        'msg': 'User Updated Successfully',
                        }

                    return JsonResponse(data_json)

            else:
                if not CustomUser.objects.filter(username=ai_userid).exists() | CustomUser.objects.filter(email=ai_email).exists():
                    CustomUser.objects.create_user(fynoo_id='FAI101', username=ai_userid, email=ai_email,
                                                   mobile_number=ai_mobile_no, password=ai_password, country_id=ai_country,
                                                   city_id=ai_city, profile_image=ai_ai_img, gender=ai_gender, dob=ai_dob,
                                                   bank_name=ai_bank_name, iban_no=ai_iban_no, maroof_link=ai_maroof_link,
                                                   is_active=active, created_by=created_by, systemip=IPAddr,
                                                   system_name=hostname, user_type=ai_user_type)

                    sendemail_verification(request, ai_email, ai_userid)

                    data_json = {
                        'id': 1,
                        'msg': 'Individual Agent created successfully',
                        'userid': ai_userid,
                    }

                    return JsonResponse(data_json)

                else:
                    data_json = {
                        'id': 0,
                        'msg': 'Username or Email Already exists',
                        }

                    return JsonResponse(data_json)

        if 'ac_email' in request.POST:
            ac_country = form.get('ac_country')
            ac_city = form.get('ac_city')
            ac_mobile_no = form.get('ac_mobile')
            ac_email = form.get('ac_email')
            ac_password = form.get('ac_password')
            ac_bank_name = form.get('ac_bank')
            ac_iban_no = form.get('ac_iban')
            ac_maroof_link = form.get('ac_maroof')
            ac_ac_img = form1.get('ac_img')
            ac_user_type = form.get('user_type_ac')
            acid = form.get('acid')

            if acid:
                CustomUser.objects.filter(id=int(acid)).update(email=ac_email, mobile_number=ac_mobile_no, password=ac_password,
                                                               country_id=ac_country, city_id=ac_city, bank_name=ac_bank_name,
                                                               iban_no=ac_iban_no, maroof_link=ac_maroof_link,
                                                               )

                if ac_ac_img != '':
                    qs = CustomUser.objects.get(id=int(acid))
                    qs.profile_image = request.FILES['ac_img']
                    qs.save()

                data_json = {
                    'id': acid,
                    'msg': 'User Updated Successfully',
                }

                return JsonResponse(data_json)
            else:
                if not CustomUser.objects.filter(username=ac_email).exists() | CustomUser.objects.filter(
                        email=ac_email).exists():
                    CustomUser.objects.create_user(fynoo_id='FAC101', username=ac_email, email=ac_email,
                                                   mobile_number=ac_mobile_no, password=ac_password,
                                                   country_id=ac_country, city_id=ac_city, profile_image=ac_ac_img,
                                                   bank_name=ac_bank_name, iban_no=ac_iban_no, maroof_link=ac_maroof_link,
                                                   is_active=active, created_by=created_by, systemip=IPAddr,
                                                   system_name=hostname, user_type=ac_user_type)

                    sendemail_verification(request, ac_email, ac_email)

                    data_json = {
                        'id': 1,
                        'msg': 'Company Agent created successfully',
                        'userid': ac_email,
                    }

                    return JsonResponse(data_json)

                else:
                    data_json = {
                        'id': 0,
                        'msg': 'Username or Email Already exists',
                    }
                    return JsonResponse(data_json)

    else:
        countries = Country.objects.all()
        cities = City.objects.all()
        captcha = generate_captcha()

        print(countries)
        return render(request, 'register.html', {'countries': countries, 'cities': cities, 'captcha': captcha})


def user_login(request):
    if request.method == 'POST':
        form = request.POST
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        verify = VerificationCode.objects.filter(user_id=username).values('verification_status')
        verification_status = verify[0]['verification_status']
        print(verification_status)

        if user and verification_status == '1':
            login(request, user)
            qs = CustomUser.objects.filter(username=user).values('id', 'username', 'fynoo_id', 'company_name', 'name',
                                                                 'email', 'user_type')

            request.session['id'] = qs[0]['id']
            request.session['username'] = qs[0]['username']
            request.session['fynoo_id'] = qs[0]['fynoo_id']
            request.session['company_name'] = qs[0]['company_name']
            request.session['name'] = qs[0]['name']
            request.session['email'] = qs[0]['email']
            request.session["cu_language"] = 'EN'
            request.session['user_type'] = qs[0]['user_type']

            data_json = {
                'status': 1,
                'msg': 'login success'

             }
            return JsonResponse(data_json)

        elif verification_status != '1':
            user_email = CustomUser.objects.filter(username=username).values('email')
            user_email_new = user_email[0]['email']
            resendemail_verification(request, user_email_new, username)
            data_json = {
                'status': 0,
                'msg': 'Your account is not active.',
                'userid': username,

            }
            return JsonResponse(data_json)

        elif not user:
            data_json = {
                'status': 2,
                'msg': 'Incorrect credentials',
             }

            return JsonResponse(data_json)

    else:
        pass

        return render(request, 'login.html')


def forgot_password(request):
    if request.method == 'POST':

        email = request.POST.get('email')

        if CustomUser.objects.filter(email=email).exists():
            sender_email = "some@gmail.com"
            receiver_email = email
            password = 'xxxxxx'

            message = MIMEMultipart("alternative")
            message["Subject"] = "multipart test"
            message["From"] = sender_email
            message["To"] = receiver_email

            set = '1234567890'
            gen_text = ''.join((random.choice(set)) for i in range(8))

            CustomUser.objects.filter(email=email).update(forgot_password_pin=gen_text)

            # Create the plain-text and HTML version of your message
            text = """\
                Dear Customer,
                You have requested to update password. Click <a href="http://127.0.0.1:8000/accounts/reset_password?pin="""+ gen_text +"""/" style="color:green;">here</a>  to verify your accunt.
                Thanks & Regards:
                Fynoo Team
                www.fynoo.com"""
            html = """\
                <html>
                    <body>
                        <p>Dear Customer,
                            You have requested to update password. Click <a href="http://127.0.0.1:8000/accounts/reset_password?pin="""+ gen_text +"""/" style="color:green;">here</a>  to verify your accunt.
                            Thanks & Regards:
                            Fynoo Team
                            www.fynoo.com
                        </p>
                    </body>
                </html>
                """

            # Turn these into plain/html MIMEText objects
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            message.attach(part1)
            message.attach(part2)

            # Create secure connection with server and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(
                    sender_email, receiver_email, message.as_string()
                )

            data_json = {
                'id': 1,
                'msg': 'email sent successfully',
            }

            return JsonResponse(data_json)

        else:
            pass

            data_json = {
                'id': 0,
                'msg': 'email not exists',
            }

            return JsonResponse(data_json)

    else:
        pass

        return render(request, 'forgot_password.html')


def reset_password(request):
    if request.method == 'POST':
        form = request.POST
        print(form)
        password = request.POST.get('password')
        reset_pin = request.POST.get('reset_pin')

        user = CustomUser.objects.get(forgot_password_pin=reset_pin)
        print(user)
        user.set_password(password)
        user.save()
        #update_session_auth_hash(request, user)

        data_json = {
            'id': 1,
            'msg': 'Password Changed successfully',
        }

        return JsonResponse(data_json)

    else:
        user_pin = request.GET.get('pin')
        print(user_pin)
        user_pin = user_pin.split('/')
        user_pin = user_pin[0]
        print(user_pin)

        return render(request, 'reset_pass.html', {'user_pin': user_pin})
