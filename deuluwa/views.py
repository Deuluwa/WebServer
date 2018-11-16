from deuluwa.models import User, Userinformation, Courseinformation, Attendancerecord, Notice, Lectureroom, Coursestudent, Course
from django.http import HttpResponse
from deuluwa.funcs import getEndTime, getTime, tardyCheck, makeDateTime
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, date, timedelta

#사용자 로그인
def getUserInfo(request):
    try :
        inputId = request.GET.get('id')
        inputPw = request.GET.get('password')

        command = "SELECT * FROM deuluwa.public.user WHERE id = '{id}' AND password = MD5('{password}');".format(id=inputId,password=inputPw)
        list = User.objects.raw(command)
        if len(list) > 0:
            if(list[0].admin == True):
                message = 'success admin'
            else:
                message = 'success'
        else:
            message = 'failed'

    except Exception as e:
        print("실패 원인 : " + str(e))
        message = 'failed'

    return HttpResponse(message)

#사용자 상세정보 조회
def getUserAddInfo(request):
    try :
        inputId = request.GET.get('id')

        userInfo = Userinformation.objects.filter(id__userinformation=inputId).first()

        address = userInfo.address
        phone = userInfo.phonenumber
        name = userInfo.name

        jsonData = {"address":address, "phonenumber":phone, "name":name}
        message = json.dumps(jsonData,ensure_ascii=False)

    except Exception as e:
        print("실패 원인 : " + str(e))
        message = 'failed'

    return HttpResponse(message)

#수강생 수강목록 조회
def getUserCourseList(request):
    try :
        inputId = request.GET.get('id')
        command = "SELECT * FROM courseinformation, coursestudent WHERE courseinformation.courseindex = coursestudent.couseid AND userid = '{id}';".format(id=inputId)

        userClasses = Courseinformation.objects.raw(command)
        userClassesList = []

        for userClass in userClasses:
            learningTime = getEndTime(userClass.starttime, userClass.coursetime)
            userClassesList.append(
                {'index':userClass.courseindex.index,
                 'coursename' : userClass.coursename,
                 'classday' : userClass.classday,
                 'startdate' : userClass.startdate.strftime("%Y-%m-%d"),
                 'enddate' : userClass.enddate.strftime("%Y-%m-%d"),
                 'starttime' : learningTime[0].strftime("%H:%M"),
                 'endtime' : learningTime[1].strftime("%H:%M")
                 }
            )
        message = json.dumps(userClassesList,ensure_ascii=False)

    except Exception as e:
        print("실패 원인 : " + str(e))
        message = 'failed'

    return HttpResponse(message)

#출석정보 조회
def getAttendanceCheckList(request):
    try:
        inputCourseId = request.GET.get('courseid')
        inputId = request.GET.get('id')

        objects = Attendancerecord.objects.filter(userid=inputId).filter(courseid=inputCourseId).order_by('-checkdate')[:5]

        courseTime = getEndTime(Courseinformation.objects.filter(courseindex=inputCourseId)[0].starttime,
                                   Courseinformation.objects.filter(courseindex=inputCourseId)[0].coursetime)

        attendanceList = []

        for result in objects:

            checkTime = getTime(result.checktime.strip())
            attendanceList.append({
                'checkdate' : str(result.checkdate),
                'checktime' : str(result.checktime),
                'attendance' : str(tardyCheck(courseTime[0], courseTime[1], checkTime))
            })

        message = json.dumps(attendanceList, ensure_ascii=False)
    except Exception as e:
        message = 'failed : ' + str(e)

    return HttpResponse(message)

#수업 상세정보 출력
def getCourseTotalInformation(request):
    try:
        inputCourseId = request.GET.get('courseid')
        inputCourseName = request.GET.get('coursename')
        cursor = connection.cursor()

        if inputCourseId == None and inputCourseName == None:
            command = "SELECT * FROM courseinfoview;"

        elif inputCourseId != None:
            command = "SELECT * FROM courseinfoview WHERE index='{index}';".format(index=inputCourseId)

        else:
            command = "SELECT * FROM courseinfoview WHERE coursename LIKE'%{coursename}%';".format(coursename=inputCourseName)

        cursor.execute(command)
        result = cursor.fetchall()
        list = []

        for obj in result:
            checkTime = getEndTime(obj[3], obj[4])
            list.append(
                {
                    'index': str(obj[0]),
                    'coursename': str(obj[1]),
                    'teacher': str(obj[2]),
                    'starttime': str(checkTime[0].strftime("%H:%M")),
                    'endtime': str(checkTime[1].strftime("%H:%M")),
                    'roomname': str(obj[5]),
                    'classday': str(obj[6]),
                    'startdate': str(Courseinformation.objects.filter(courseindex=obj[0]).first().startdate),
                    'enddate': str(Courseinformation.objects.filter(courseindex=obj[0]).first().enddate),
                    'roomindex': str(obj[7]),
                    'teacherindex': str(obj[8])
                }
            )
            if (inputCourseId != None):
                break

        message = json.dumps(list, ensure_ascii=False)

    except Exception as e:
        message = 'failed : ' + str(e)

    return HttpResponse(message)

#수업 수강생 조회
def getcoursestudentlist(request):
    try:
        inputCourseId = request.GET.get('courseid')

        objects = Coursestudent.objects.filter(couseid=inputCourseId)

        list = []

        for obj in objects:
            list.append({
                'id' : str(obj.userid.id),
                'name' : str(Userinformation.objects.filter(id=obj.userid).first().name)
            })

        if(len(list) > 0):
            message = json.dumps(list, ensure_ascii=False)
        else:
            message = 'NO RESULT'

    except Exception as e:
        message = 'failed : ' + str(e)

    return HttpResponse(message)

#사용자 목록 출력
def getUserList(request):
    try:
        inputUserName = request.GET.get('username')

        if (inputUserName == None):
            objects = Userinformation.objects.order_by('id').all()
        else:
            objects = Userinformation.objects.filter(name=inputUserName).order_by('id')

        list = []

        message='test'
        for obj in objects:
            list.append({
                'id' : str(obj.id.id),
                'name' : str(obj.name),
                'address' : str(obj.address),
                'phonenumber' : str(obj.phonenumber),
                'admin' : str(obj.id.admin)
            })
        if (len(list) > 0):
            message = json.dumps(list, ensure_ascii=False)
        else:
            message = 'NO RESULT'

    except Exception as e:
        message = 'failed : ' + str(e)
        print(message)

    return HttpResponse(message)

#공지사항 출력
def getNoticeMessages(request):
    noticeMessages = Notice.objects.order_by('-index')

    noticeList = []

    for result in noticeMessages:
        noticeList.append({
            'index' : result.index,
            'message' : result.message,
            'user' : Userinformation.objects.filter(id__userinformation=result.user.id).first().name,
            'time' : makeDateTime(str(result.date).strip(), str(result.time).strip())
        })

    message = json.dumps(noticeList, ensure_ascii=False)

    return HttpResponse(message)

#공지사항 입력
@csrf_exempt
def writeNoticeMessage(request):
    try:
        inputId = request.POST['id']
        inputMessage = request.POST['message']

        message = inputMessage

        time = datetime.now()

        query = Notice.objects.create(
            user=User.objects.filter(id=inputId).first(),
            message=inputMessage,
            date=time.strftime('%Y-%m-%d'),
            time=time.strftime('%H:%M:%S')
        )
        query.save()

        noticeMessages = Notice.objects.order_by('-index')

        noticeList = []

        for result in noticeMessages:
            noticeList.append({
                'index': result.index,
                'message': result.message,
                'user': Userinformation.objects.filter(id__userinformation=result.user.id).first().name,
                'time': makeDateTime(str(result.date).strip(), str(result.time).strip())
            })

        message = json.dumps(noticeList, ensure_ascii=False)

    except Exception as e:
        message = 'failed : ' + str(e)

    return HttpResponse(message)

#사용자 정보 업데이트
@csrf_exempt
def updateUserInformation(request):
    try:
        inputId = request.POST['id']
        inputName = request.POST['name']
        inputPhonenumber = request.POST['phonenumber']
        inputAddress = request.POST['address']

        userinfo = Userinformation.objects.get(id=inputId)
        print(userinfo)
        userinfo.name=inputName
        userinfo.phonenumber=inputPhonenumber
        userinfo.address=inputAddress
        userinfo.save()

        objects = Userinformation.objects.order_by('id').all()

        list = []

        message = 'test'
        for obj in objects:
            list.append({
                'id': str(obj.id.id),
                'name': str(obj.name),
                'address': str(obj.address),
                'phonenumber': str(obj.phonenumber),
                'admin': str(obj.id.admin)
            })

        message = json.dumps(list, ensure_ascii=False)
        
    except Exception as e:
        message = 'failed : ' + str(e)

    return HttpResponse(message)

#사용자 등록
@csrf_exempt
def addUser(request):
    try:
        inputId = request.POST['id']
        inputName = request.POST['name']
        inputPhonenumber = request.POST['phonenumber']
        inputAddress = request.POST['address']
        inputAdmin = request.POST['admin']

        admin = inputAdmin == 'True' if True else False

        cursor = connection.cursor()
        #command = "SELECT * FROM courseinfoview WHERE index='{index}';".format(index=inputCourseId)
        command = "SELECT MD5('{md5pass}');".format(md5pass = inputPhonenumber)
        cursor.execute(command)
        makePassword = cursor.fetchall()[0][0]

        User.objects.create(id=inputId, password=makePassword, admin=admin)

        Userinformation.objects.create(
            id=User.objects.filter(id=inputId).get(),
            name=inputName,
            phonenumber=inputPhonenumber,
            address=inputAddress,
        )

        objects = Userinformation.objects.order_by('id').all()

        list = []

        for obj in objects:
            list.append({
                'id': str(obj.id.id),
                'name': str(obj.name),
                'address': str(obj.address),
                'phonenumber': str(obj.phonenumber),
                'admin': str(obj.id.admin)
            })

        message = json.dumps(list, ensure_ascii=False)

    except Exception as e:
        message = 'failed : ' + str(e)

    return HttpResponse(message)

#비밀번호 초기화
@csrf_exempt
def passwordReset(request):
    try:
        inputId = request.GET.get('id')

        user = User.objects.filter(id=inputId).first()

        cursor = connection.cursor()
        # command = "SELECT * FROM courseinfoview WHERE index='{index}';".format(index=inputCourseId)
        command = "SELECT MD5('{md5pass}');".format(md5pass=Userinformation.objects.filter(id=user).first().phonenumber)
        cursor.execute(command)
        makePassword = cursor.fetchall()[0][0]

        user.password=makePassword
        user.save()

        message='success'


    except Exception as e:
        message = 'failed : ' + str(e)

    return HttpResponse(message)

#강의실 목록 조회
def getRoomList(request):
    try:
        inputRoomName = request.GET.get('roomname')

        if(inputRoomName == None):
            resultList = Lectureroom.objects.all()
        else:
            resultList = Lectureroom.objects.filter(name=inputRoomName)

        list = []

        for result in resultList:
            list.append({
                'index': str(result.index),
                'name': str(result.name)
            })


        if (len(list) > 0):
            message = json.dumps(list, ensure_ascii=False)
        else:
            message = "NO RESULT"

    except Exception as e:
        message = 'failed : ' + str(e)

    return HttpResponse(message)

#코스에 학생 관리
@csrf_exempt
def manageStudentToCourse(request):
    try:
        inputCourseId = request.POST['courseid']
        inputUserId = request.POST['userid']
        inputMode = request.POST['mode']

        if inputMode == 'add':
            query = Coursestudent.objects.create(
                couseid = Course.objects.filter(index=inputCourseId).first(),
                userid = User.objects.filter(id=inputUserId).first()
            )
            query.save()

        elif inputMode == 'delete':
            query = Coursestudent.objects.filter(
                couseid = Course.objects.filter(index=inputCourseId).first(),
                userid = User.objects.filter(id=inputUserId).first()
            ).delete()

        message = 'success'

    except Exception as e:
        message = 'failed : ' + str(e)
    return HttpResponse(message)

#수업 관리
@csrf_exempt
def manageCourse(request):
    try:
        inputMode = request.POST['mode']
        #수업 추가시
        if inputMode == 'add':
            #필요한 항목들을 받아온다
            inputTeacherId      = request.POST['teacher']
            inputRoomIndex      = request.POST['room']
            inputStartDate      = request.POST['startdate']
            inputEndDate        = request.POST['enddate']
            inputStartTime      = request.POST['starttime']
            inputRunningTime    = request.POST['runningtime']
            inputClassDay       = request.POST['classday']
            inputCourseName     = request.POST['coursename']

            try:
                courseQuery = Course.objects.create(
                    lectureindex        = User.objects.filter(id=inputTeacherId).first(),
                    lectureroomindex    = Lectureroom.objects.filter(index=inputRoomIndex).first()
                )

                courseQuery.save()
            except Exception as e:
                message = 'Course Insert Failed : ' + str(e)


            try:
                informationQuery = Courseinformation.objects.create(
                    courseindex     = Course.objects.all().last(),
                    startdate       = datetime.strptime(inputStartDate,'%Y-%m-%d').date(),
                    enddate         = datetime.strptime(inputEndDate,'%Y-%m-%d').date(),
                       starttime       = inputStartTime.strip(),
                    coursetime      = int(inputRunningTime),
                    classday        = inputClassDay.strip(),
                    coursename      = inputCourseName.strip()
                )

                informationQuery.save()
            except Exception as e:
                message = 'CourseInformation Insert Failed : ' + str(e)

            message = 'success : ' + str(Course.objects.all().last().index)

        #수업 삭제시
        elif inputMode == 'delete':
            inputCourseId = request.POST['courseid']
            #수강생 -> 수업상세정보 -> 수업정보를 지운다
            Coursestudent.objects.filter(couseid=inputCourseId).delete()
            Courseinformation.objects.filter(courseindex=inputCourseId).delete()
            Course.objects.filter(index=inputCourseId).delete()
            message = 'success'

        #수업 수정시
        elif inputMode == 'modify':
            inputCourseId       = request.POST['courseid']
            inputTeacherId      = request.POST['teacher']
            inputRoomIndex      = request.POST['room']
            inputStartDate      = request.POST['startdate']
            inputEndDate        = request.POST['enddate']
            inputStartTime      = request.POST['starttime']
            inputRunningTime    = request.POST['runningtime']
            inputClassDay       = request.POST['classday']
            inputCourseName     = request.POST['coursename']

            #두 항목을 업데이트 한다
            Course.objects.filter(index=inputCourseId).update(
                lectureindex=User.objects.filter(id=inputTeacherId).first(),
                lectureroomindex=Lectureroom.objects.filter(index=inputRoomIndex).first()
            )

            Courseinformation.objects.filter(courseindex=inputCourseId).update(
                startdate=datetime.strptime(inputStartDate, '%Y-%m-%d').date(),
                enddate=datetime.strptime(inputEndDate, '%Y-%m-%d').date(),
                starttime=inputStartTime.strip(),
                coursetime=int(inputRunningTime),
                classday=inputClassDay.strip(),
                coursename=inputCourseName.strip()
            )

            message = 'success'
    except Exception as e:
        message = 'failed : ' + str(e)

    return HttpResponse(message)

#출석 날짜 목록 출력
def getCheckDayList(request):
    try:
        inputCourseId = request.GET.get('courseid')
        #시작일부터 오늘까지 출력
        #0~6 -> 월~목

        courseObject = Courseinformation.objects.filter(courseindex=inputCourseId).first()
        courseStartDate = datetime.combine(courseObject.startdate, datetime.min.time())
        today = datetime.today()
        courseDay = courseObject.classday

        dateList = []

        while courseStartDate <= today:

            if courseDay[courseStartDate.weekday()] == 'T':
                dateList.append({
                    'date' : str(courseStartDate.date())
                })

            courseStartDate += timedelta(days=1)

        message = json.dumps(dateList, ensure_ascii=False)

    except Exception as e:
        message = 'failed : ' + str(e)

    return HttpResponse(message)

#해당 날짜 출석 목록 출력
@csrf_exempt
def getCheckList(request):
    try:
        inputCourseId = request.GET.get('courseid')
        inputDate = request.GET.get('date')

        courseTime = getEndTime(Courseinformation.objects.filter(courseindex=inputCourseId)[0].starttime,
                                   Courseinformation.objects.filter(courseindex=inputCourseId)[0].coursetime)
        starttime = courseTime[0].strftime("%H:%M")
        endtime = courseTime[1].strftime("%H:%M")

        checkList = []
        students = Coursestudent.objects.filter(couseid=inputCourseId).all()
        for student in students:
            if len(Attendancerecord.objects.filter(userid=student.userid, checkdate=inputDate)) == 0:
                #결석인 경우 이때 새로 만듬
                checkQuery = Attendancerecord.objects.create(
                    userid=student.userid,
                    courseid=Course.objects.filter(index=inputCourseId).first(),
                    checkdate=inputDate,
                    checktime=str(courseTime[1].strftime("%H%M"))
                )
                checkQuery.save()

            #리스트에 담음
            checkList.append({
                'userid' : str(student.userid.id),
                'name' : str(Userinformation.objects.filter(id=student.userid).first().name),
                'checked' : str(tardyCheck(starttime,endtime,Attendancerecord.objects.filter
                (userid=student.userid, courseid=inputCourseId, checkdate=inputDate).first().checktime)),
                'checktime' :  str(Attendancerecord.objects.filter
                (userid=student.userid, courseid=inputCourseId, checkdate=inputDate).first().checktime)
            })

        message = json.dumps(checkList,ensure_ascii=False)

    except Exception as e:
        message = 'failed : ' + str(e)
    return HttpResponse(message)