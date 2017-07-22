from flask import *
from flask import session as login_session
from database import *
from werkzeug.utils import secure_filename
from passlib.hash import pbkdf2_sha256 as crypt
import os
import operator


app= Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
PROFILEVOL_FOLDER = 'static/profilevol'
PROFILEORG_FOLDER = 'static/profile'
BACKGROUND_FOLDER = 'static/background'
app.config['PROFILEORG_FOLDER'] = PROFILEORG_FOLDER
app.config['BACKGROUND_FOLDER'] = BACKGROUND_FOLDER
app.config['PROFILEVOL_FOLDER'] = PROFILEVOL_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/')
def home():
    return render_template('login.html')

#@app.route("/search",methods=['GET','POST'])
#def search():
#return render_template('home.html')

@app.route('/about_us')
def about_us():
    return render_template('aboutus.html')

@app.route('/logout')
def logout():
    login_session.clear()
    return render_template('login.html')

@app.route('/login' , methods=['GET','POST'])
def login():
    if(request.method=='GET'):
        return render_template('login.html')
    if (request.method=='POST'):
        email=request.form['email']
        password=request.form['password']
        login_session['username'] = username
        confirmpassorg=None
        confirmpassvol=None
        if(session.query(Volunteers).filter_by(email = email).first()!=None):
            confirmpassvol=session.query(Volunteers).filter_by(email = email).first().password#hashed password from volunteers
        if(session.query(Organizations).filter_by(email = email).first()!=None):
            confirmpassorg=session.query(Organizations).filter_by(email= email).first().password#hashed password from organizations
        if(confirmpassorg==None and confirmpassvol==None):
            flash("Email doesn't exist")
            return render_template('login.html')
        if(confirmpassorg!=None):
            if(confirmpassorg!=None and not crypt.verify(password,confirmpassorg)):
                flash('Wrong password')
                return render_template('login.html')
        if(confirmpassvol!=None and not crypt.verify(password,confirmpassvol)):
            flash('Wrong password')
            return render_template('login.html')
        if(confirmpassvol!=None):
            user=session.query(Volunteers).filter_by(email = email).first()
            login_session['id']=user.id
            login_session['type']="vol"
            organizations=sortbyinterest(user)
            return render_template("homevol.html",user=user,organizations=organizations)
        if(confirmpassorg!=None):
            user=session.query(Organizations).filter_by(email = email).first()
            login_session['id']=user.id
            login_session['type']="org"
            return redirect(url_for("homeorg",user=user))
def sortbyinterest(user):
    user_interests=user.interests.split(',')
    orgs=session.query(Organizations).all()
    orga={}
    for org in orgs:
        c=0 
        for interest in user_interests:
            if interest in org.fields:
                c+=1
        
        orga[org]=c
    lst=sorted(orga.items(),key=operator.itemgetter(1),reverse=True)
    result=[]
    for org,val in lst:
        result.append(org)
    
    return result
def sortbycity(user):
    user_city = user.city
    org = session.query(Organizations).all()
    okay_org = []
    for o in org:
        if user_city == o.city:
            okay_org.append(o)
    return okay_org
@app.route("/volunteer_profile/<int:user_id>")
def volunteer_profile(user_id):
    user = session.query(Volunteers).filter_by(id=user_id).first()
    
    return render_template('volunteer_profile.html', user=user, user_id = user.id)
@app.route('/editprofile/<int:user_id>',methods=['GET', 'POST'])
def editprofile(user_id):
   print('editing profile')
   #user_id = login_session['username']
   user=session.query(Volunteers).filter_by(id=user_id).first()
   print('obtained user')
   # image=request.files['profile']
   # if image is not None:
   #     if session.query(Volunteers).first() is None :
   #         x="0profile"
   #     else :
   #         x=str(session.query(Volunteers).order_by(Volunteers.id.desc()).first().id)+"profile"
   #     lst= image.filename.split(".")
   #     x += "."+lst[len(lst)-1]
   #     str1="\static\\images\\"+x ## we set the directory for the image so we can access it later
   #     image.save(os.path.join(app.config['UPLOAD_FOLDER'], x)) ## we save the image in UPLOAD_FOLDER
   #     user.profile=str1
   name=request.form['name']
   if name is not None:
       user.name=name

   print('After name')
   password=request.form['password']
   if password is not None:
       user.password=password
    #TODO confirm password
   print('After passwd')
  
   birthday=request.form['birthday']
   if birthday is not None:
       user.birthday=birthday
   print('After birth')
   interests=request.form['interests'] 
   if interests is not None:
       user.interests=interests
   print('After interests')
   school=request.form['school']
   if school is not None:
       user.school=school
   
   #TODO confirm that user actually worked at orgs listed in 'past organizations'
   
   address=request.form['address']
   if address is not None:
       user.address=address
   phonenumber=request.form['phonenumber']
   if phonenumber is not None:
       user.phonenumber=phonenumber

   print('about to commit')
   session.commit()
   # redirect(url_for(volunteer(user_id)))
   print('about to redirect')
   #redirect(url_for('volunteer/' + str(user_id)))
   #return  render_template("volunteer.html" )
   return volunteer_profile(user_id)  
 #user = session.query(Volunteers).filter_by(id=user_id).first()
    
 #  return render_template('volunteer.html', user=user, user_id = user.id)
@app.route('/homeorg', methods = ['GET','POST'])
def homeorg():
    all_requests = session.query(Requests).all()
    all_hour_requests = session.query(Request_Hour).all()
    all_feedback = session.query(Feedback).all()
    volunteers = session.query(Volunteers).all()
    org = session.query(Organizations).filter_by(id = login_session['organization_id']).first()
    return render_template('homeorg.html', org = org, all_requests = all_requests, volunteers = volunteers,all_hour_requests = all_hour_requests, all_feedback = all_feedback)

@app.route('/accept/<int:nominee_id>', methods = ['GET','POST'])
def accept(nominee_id):
    if request.method == 'POST':
        print("d")
        print(nominee_id)
        nominee = session.query(Requests).filter_by(id = nominee_id).first()
        print(nominee)

        
        nominee.accepted = 1
        session.commit()
        return redirect('homeorg')
@app.route('/reject/<int:nominee_id>', methods = ['GET', 'POST'])
def reject(nominee_id):
    if request.method == 'POST':
        nominee = session.query(Requests).filter_by(id = nominee_id).first()
        nominee.accepted = 2
        session.commit()
        return redirect('homeorg')
    
@app.route('/search', methods = ['GET','POST'])
def search():
    if request.method == 'POST':
        name_place = request.form['place']
        print(name_place)
        places = session.query(Organizations).filter(Organizations.name.contains(name_place.lower())).first()
        place_id = places.id
                #return render_template('diveplace.html',place_id = a)
        return redirect(url_for('place',place_id = places.id))

    return render_template('homevol.html')





@app.route('/homevol', methods = ['GET','POST'])
def homevol():
    total_hours = 0
    a = session.query(VolunteeringHours).filter_by(volunteer_id = login_session['id']).all()
    i = login_session['id']
    volunteer = session.query(Volunteers).filter_by(id = login_session['id']).first()
    goal = volunteer.goal_hour
    print(float(goal))

    for volunteer in a:
        if volunteer.volunteer_id == i:
            total_hours += volunteer.hours
       
    print(total_hours)
    f = total_hours * 100
    precent = f / goal
    print(float(precent))

    return render_template('homevol.html',precent = precent, volunteer = volunteer, a = a)
@app.route('/signup', methods = ['GET','POST'])
def signup():
    flag=0
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        birthday = request.form['birthday']
        city = request.form['city']
        about = request.form['about']
        interests = request.form['interests']
        interests=interests[:-1]
        profile = request.files['profile']
        gender = request.form['gender']
        phonenumber = request.form['phonenumber']
        school = request.form['school']

        pastorganizations = request.form['pastorganizations']
        goal_hour = request.form['goal']

        if name is None or email is None or password is None or birthday is None or username is None or interests is None or gender is None or phonenumber is None or address is None or school is None:
            flash("Your form is missing arguments")
            flag=1
        
        
        if (session.query(Volunteers).filter_by(email=email).first() is not None ) or (session.query(Organizations).filter_by(email=email).first() is not None) :
            flag=1
            flash("Email already exists")
        if profile.filename == '':
            flash('Profile: No selected file')
            flag = 1
        password=crypt.hash(password)
        
        if profile and allowed_file(profile.filename):
            if session.query(Volunteers).first() is None:
                x = "0profilevol"
            else:
                x = str(session.query(Volunteers).order_by(Volunteers.id.desc()).first().id)+"profilevol"
            lst = profile.filename.split(".")
            x += "."+lst[len(lst)-1]
            str1="static/profilevol/"+x
        else:
            flag=1
            flash("filetype is not allowed")
        if flag==1:
            return render_template('signup.html')
        profile.save(os.path.join(app.config['PROFILEVOL_FOLDER'],x))
        user = Volunteers(name = name, email=email, birthday = birthday, gender = gender, interests = interests,password= password,
       profile=str1,phonenumber=phonenumber,address=address,school=school,pastorganizations=pastorganizations,goal_hour = goal_hour, about = about, city = city)
        session.add(user)
        session.commit()
        return redirect(url_for('login'))
        
    else:
        return render_template('signup.html')
@app.route('/signupO',methods=['GET','POST'])
def signupO():
    flag=0
    if request.method == "POST":
        name = request.form['name']
        password = crypt.hash(request.form['password'])       
        creationdate = request.form['creationdate']
        email = request.form['email']
        city = request.form['city']
        description = request.form['description']
        shortdescription = request.form['shortdescription']
        fields = request.form['interests']
        fields =fields[:-1]
        profile = request.files['profile']
        background = request.files['background']
        if (len(shortdescription)>50):
            flash("short description is too long make sure it is less than 50 letters")
            flag=1
        if (session.query(Volunteers).filter_by(email=email).first() is not None ) or (session.query(Organizations).filter_by(email=email).first() is not None) :
            flag=1
            flash("Email already exists")
        if profile.filename == '':
            flash('Profile: No selected file')
            flag = 1
        if profile and allowed_file(profile.filename):
            if session.query(Organizations).first() is None:
                x = "0profile"
            else:
                x = str(session.query(Organizations).order_by(Organizations.id.desc()).first().id)+"profile"
            lst = profile.filename.split(".")
            x += "."+lst[len(lst)-1]
            str1="static/profile//"+x
        if background.filename != '' and not allowed_file(background.filename):
            flash("Background:Not allowed file")
            flag = 1
        if background.filename == '':
            flash('No selected file')
            flag = 1
        if background and allowed_file(background.filename):
            if session.query(Organizations).first() is None:
                x1 = "0background"
            else:
                x1 = str(session.query(Organizations).order_by(Organizations.id.desc()).first().id)+"background"
            lst1 = background.filename.split(".")
            x1 += "."+lst1[len(lst1)-1]
            str2="static//background//"+x 
        if background.filename != '' and not allowed_file(background.filename):
            flash("Not allowed file")
            flag = 1
        if flag==1:
            return render_template("signupO.html")
        background.save(os.path.join(app.config['BACKGROUND_FOLDER'],x1))
        profile.save(os.path.join(app.config['PROFILEORG_FOLDER'],x))
        new_organization = Organizations(name = name, password = password, creationdate = creationdate,email = email, 
             description = description, shortdescription = shortdescription, fields = fields,profile = str1 ,background=str2,city = city)
        session.add(new_organization)
        session.commit()
        return redirect(url_for('login'))

    else:
        return render_template('signupO.html')


#@app.route('/place')
#def place():
 #   return render_template('place.html')
@app.route('/homevol')
def myrequests():
    stillreqs=session.query(Requests).filter_by(volunteer_id=login_session['id'],accepted=0).all()
    acceptedreqs=session.query(Requests).filter_by(volunteer_id=login_session['id'],accepted=1).all()

    volnames=[]
    orgnames=[]
    acvolnames=[]
    acorgnames=[]
    for req in stillreqs:
        volnames.append(session.query(Volunteers).filter_by(id=req.volunteer_id).first().name)
        orgnames.append(session.query(Organizations).filter_by(id=req.organization_id).first().name)
    for req in acceptedreqs:
        acvolnames.append(session.query(Volunteers).filter_by(id=req.volunteer_id).first().name)
        acorgnames.append(session.query(Organizations).filter_by(id=req.organization_id).first().name)
    return render_template("homevol.html",stillreqs=stillreqs,acceptedreqs=acceptedreqs,acorgnames=acorgnames,acvolnames=acorgnames,type=login_session['type'],volnames=volnames,orgnames=orgnames)

@app.route('/delete/<int:id>')
def delete(id):
    req=session.query(Requests).filter_by(id=id).first()
    session.delete(req)
    session.commit()
    reqs=session.query(Requests).filter_by(volunteer_id=login_session['id']).all()
    return redirect(url_for('myrequests'))


@app.route('/place/<int:place_id>')
def place(place_id):
    login_session['organization_id']=place_id
    place = session.query(Organizations).filter_by(id = place_id).first()
    r = session.query(Requests).filter_by(volunteer_id = login_session['id']).first()
    return render_template('place.html',place_id = place.id, place = place,user_type=login_session['type'], r =r)
@app.route('/find')
def find():
    user=session.query(Volunteers).filter_by(id = login_session['id']).first()

    #places = session.query(Organizations).all()
    organizations=sortbyinterest(user)
    organizations1 = sortbycity(user)
    return render_template('find.html', organizations = organizations,user = user,organizations1 = organizations1)
@app.route('/volunteer',methods=['GET','POST'])
def volunteer():
    if request.method=='GET':
        return render_template('volunteer.html')
    start_time = request.form['start_time']
    length = request.form['length']
    date = request.form['date']
    request1=Requests(volunteer_id=login_session['id'],organization_id=login_session['organization_id'],
        start_time=start_time,accepted=0,worked=0,length=length, date = date)
    hours = VolunteeringHours(volunteer_id= login_session['id'], organization_id = login_session['organization_id'],
        hours = length)

    session.add(hours)

    session.add(request1)
    session.commit()
    return place(login_session['organization_id'])

@app.route('/ask_hours', methods = ['GET','POST'])
def ask_hours():
    if request.method == 'POST':
        new_request = Request_Hour(volunteer_id = login_session['id'], organization_id = login_session['organization_id'],worked = 0)
        session.add(new_request)
        session.commit()
        #return place(login_session['organization_id'])
        return place(login_session['organization_id'])

@app.route('/confirm_hours/<int:nominee_id>', methods = ['GET','POST'])
def confirm_hours(nominee_id):
    if request.method == 'POST':
        print("d")
        print(nominee_id)
        nominee = session.query(Request_Hour).filter_by(id = nominee_id).first()
        print(nominee)

        
        nominee.worked = 1
        session.commit()
        return redirect('homeorg')
@app.route('/ask_feedback',methods = ['GET','POST'])
def ask_feedback():
    if request.method == 'POST':
        new_feedback = Feedback(volunteer_id = login_session['id'], organization_id = login_session['organization_id'])
        session.add(new_feedback)
        session.commit()
        return render_template('homevol.html')
@app.route('/confirm_feedback/<int:nominee_id>', methods = ['GET','POST'])
def confirm_feedback(nominee_id):
    if request.method == 'POST':
        feedback = request.form['feedback']
        print("d")
        print(nominee_id)
        nominee = session.query(Feedback).filter_by(id = nominee_id).first()
        print(nominee)

        
        nominee.feedback = feedback
        session.commit()
        return redirect('homeorg')


@app.route('/my_volunteers')
def my_volunteers():
    my = session.query(Requests).filter_by(organization_id = login_session['organization_id']).all()
    print(my)
    v = session.query(Volunteers).all()
    return render_template('my_volunteers.html',my = my, v =v)

@app.route('/myprofile')
def myprofile():
    return render_template('myprofile.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/volunteer_calendar' )
def volunteer_calendar():
    volunteer = session.query(Volunteers).first()
    return render_template('volunteer_calendar.html')


#@app.route('/volunteeringhours')
#def volunteeringhours():
#if request.method




if __name__== '__main__' :
    app.run(debug=True)
    # profile=request.files['profile']
    # if profile.filename == '':
    #     flash('No selected file')
    #     flag=1
    # print("passed first")
    # if profile and allowed_file(profile.filename):     
    #     if session.query(Users).first() is None :
    #         x="0profile"
    #     else :
    #         x=str(session.query(Users).order_by(Users.id.desc()).first().id)+"profile"
    #     lst= profile.filename.split(".")
    #     x += "."+lst[len(lst)-1]
    #     str1="\static\\images\\"+x ## we set the directory for the image so we can access it later
    #     profile.save(os.path.join(app.config['UPLOAD_FOLDER'], x)) ## we save the image in UPLOAD_FOLDER
    # print("passed second")
    # if profile.filename!="" and not allowed_file(profile.filename) :
    #     flash("Please upload either a .jpg, .jpeg, .png, or .gif file.")
    #     flag=1
    # print("passed third")
