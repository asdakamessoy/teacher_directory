# Teacher's Directory

Application to view Teacher personal details or active courses they are assigned to.


# Setup Application 

pip install - r requirements.txt

python /manage.py runserver


# API Sample

Get Teachers list 

Can be searched on the basis of firstname lastname or email.
Pagination has been implemented as well; where max records per page is 20

```bash
GET : /v1/teacher/all/?page_number=1
GET : /v1/teacher/all/?page_number=1&email=a@a.com
GET : /v1/teacher/all/?page_number=1&email=a@a.com&first_name=ABC
GET : /v1/teacher/all/?page_number=1&email=a@a.com&first_name=ABC&last_name=ABC

RESPONSE:

{
   "teachers":[
      {
         "reference_number":"4a977763-cbe0-427e-94a7-facce1634751",
         "first_name":"Laticia",
         "last_name":"Landen",
         "email":"teacher1@school.com"
      },
      {
         "reference_number":"6ff9959a-6f17-44b0-8c0e-fb5c715aaf65",
         "first_name":"Tamela",
         "last_name":"Tomblin",
         "email":"teach1@school.com"
      },
      {
         "reference_number":"35582a0f-6180-4138-8e18-2e3de3faca8d",
         "first_name":"Cordelia",
         "last_name":"Carpio",
         "email":"teach5@school.com"
      },
      {
         "reference_number":"61617602-d8fb-4a40-baad-3e1a8c2a06fd",
         "first_name":"Arlinda",
         "last_name":"Arehart",
         "email":"teach8@school.com"
      }
   ],
   "teachers_count":4
}


```


Get Individual Teacher details
This API returns Teacher's personal details along with list of courses he/she is assigned to.

Record is fetchsed using "Teacher.reference_number" rather ID.


```bash
GET : /v1/teacher/read/?reference_number=ABC


RESPONSE:

{
   "first_name":"Laticia",
   "last_name":"Landen",
   "email":"teacher1@school.com",
   "profile_picture":"/images/21167.JPG",
   "phone_number":"+971-505-550-507",
   "room_number":"3a",
   "code":"",
   "active_courses":[
      {
         "course_name":"Computer science",
         "start_date":"2021-10-17",
         "end_date":null
      },
      {
         "course_name":"Physics",
         "start_date":"2021-10-17",
         "end_date":null
      }
   ]
}

```



To Import Teacher report CSV File

I have created a basic interface, where you may see a fileupload form.

```bash
GET: /v1/teacher/upload-csv/

```

It does handle creating new Teacher records, and assigning them to respective subjects as well, keeping in mind one teacher can not have more than 5 active courses at a time.


