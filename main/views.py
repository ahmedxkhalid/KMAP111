from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import Student

def index(request):
    if 'user' in request.session:
        return render(request, 'admin_panel.html')
    else:
        return render(request, 'admin-login.html')

def admin_login(request):
    if 'user' in request.session:
        return render(request, 'admin_panel.html')
    else:
        return render(request, 'admin-login.html')

def admin_panel(request):
    if 'user' in request.session:
        students = Student.objects.all()
        params = {'students': students}
        return render(request, 'admin_panel.html', params)
    else:
        if request.method == 'POST':
            user_name = request.POST['uname']
            pass_word = request.POST['pwd']
            if user_name == 'admin' and pass_word == 'admin123':
                request.session['user'] = user_name
                students = Student.objects.all()
                params = {'students': students}
                return render(request, 'admin_panel.html', params)
            else:
                return render(request, 'admin-login.html')
        else:
            return render(request, 'admin-login.html')

def delete_student(request, id):
    get_stu = Student.objects.get(id=id)
    get_stu.delete()
    return redirect('/admin_panel')

def edit_confirm(request, id):

    if request.method == 'POST':
        get_stu = Student.objects.get(id=id)
        get_stu.name = request.POST.get('sname', get_stu.name)
        get_stu.roll_no = request.POST.get('roll_no', get_stu.roll_no)
        get_stu.accounting = int(request.POST.get('accounting', get_stu.accounting))
        get_stu.decision_support = int(request.POST.get('decision_support', get_stu.decision_support))
        get_stu.information_security = int(request.POST.get('information_security', get_stu.information_security))
        get_stu.english_accounting = int(request.POST.get('english_accounting', get_stu.english_accounting))
        get_stu.personnel_management = int(request.POST.get('personnel_management', get_stu.personnel_management))

        total = get_stu.accounting + get_stu.decision_support + get_stu.information_security + get_stu.english_accounting + get_stu.personnel_management
        get_stu.total = total
        get_stu.percent = total / 500 * 100  # Assuming maximum score is 100 for each subject
        get_stu.save()

        return redirect('/admin_panel')

    else:

        return redirect('/admin_login')

def admin_logout(request):
    del request.session['user']
    return redirect('/')

def add_student(request):
    return render(request, 'add_student.html')
    
def edit_student(request, id):

    get_stu = Student.objects.get(id=id)

    params = {'student': get_stu}

    return render(request, 'edit.html', params)
def add_confirm(request):
    if request.method == 'POST':
        sname = request.POST['sname']
        roll_no = request.POST['roll-no']
        accounting = int(request.POST['accounting'])
        decision_support = int(request.POST['decision_support'])
        information_security = int(request.POST['information_security'])
        english_accounting = int(request.POST['english_accounting'])
        personnel_management = int(request.POST['personnel_management'])

        total = accounting + decision_support + information_security + english_accounting + personnel_management
        percent = total / 500 * 100  # Assuming maximum score is 100 for each subject
        add_student = Student.objects.create(name=sname, roll_no=roll_no, accounting=accounting, decision_support=decision_support, information_security=information_security, english_accounting=english_accounting, personnel_management=personnel_management, total=total, percent=percent)
        add_student.save()
        return redirect('/admin_panel')
    else:
        return redirect('/admin_panel')

def result(request):
    if request.method == 'POST':
        roll_no = int(request.POST['roll_no'])
        student = Student.objects.get(roll_no=roll_no)
        accounting = student.accounting
        decision_support = student.decision_support
        information_security = student.information_security
        english_accounting = student.english_accounting
        personnel_management = student.personnel_management

        total = accounting + decision_support + information_security + english_accounting + personnel_management
        percent = total / 500 * 100  # Assuming maximum score is 100 for each subject
        status = 'Fail' if percent < 33 else 'Pass'

        params = {
            'roll_no': roll_no,
            'name': student.name,
            'accounting': accounting,
            'decision_support': decision_support,
            'information_security': information_security,
            'english_accounting': english_accounting,
            'personnel_management': personnel_management,
            'total': total,
            'percent': percent,
            'status': status
        }

        return render(request, 'result.html', params)
    else:
        return render(request, 'index.html')
