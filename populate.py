from flask import *
from flask import session as login_session
from database import *
from werkzeug.utils import secure_filename
from passlib.hash import pbkdf2_sha256 as crypt
import os
vol=Volunteers(name="mahmoud" ,password =crypt.hash("123")    ,birthday ="2424"     ,email ="dasd"     ,gender ="male"     ,username = "mahmoud"    ,profile = "s"    ,interests ="Community" ,phonenumber="554",address="2str",school="sises of st.joseph",pastorganizations="odsa")
session.add(vol)

org=Organizations(name = "safa",password = crypt.hash("123"),creationdate = "ss",email = "masd",username = "mah" ,description = "asdas",shortdescription = "asd",profile = "ada",background ="asdda",fields = "asd")
session.add(org)
session.commit()
req=Requests(organization_id=1,volunteer_id=1,start_time = "4-4" ,accepted =2 ,worked = 2,length =2 , date="5-5-5")
session.add(req)

session.commit()
