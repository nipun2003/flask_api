from sqlalchemy.sql.expression import *
from src.database.dbConnector import DbConnector
import random
from datetime import datetime
import requests
from src.authentication.pass_hash import PassHash
from src.constants.const import *

conn = DbConnector()

Users = conn.meta_data.tables['users']
Secret = conn.meta_data.tables['secret']
Sessions = conn.meta_data.tables['sessions']

class AuthHandler:
    def getUserByPhone(phone):
        stmt = select([Users]).where(and_(Users.c.phone==phone))
        try:
            return conn.engine.execute(stmt).one()
        except :
            return None
    def checkPhone(phone):
        stmt = select([Users]).where(and_(Users.c.phone==phone))
        try:
            return conn.engine.execute(stmt).one() is not None
        except :
            return False
    def createNewSecret(phone,a):
        stmt = select([Secret]).where(and_(Secret.c.phone==phone))
        prevOtp = conn.engine.execute(stmt).fetchall()
        if(len(prevOtp)>0):
            prevOtp = prevOtp[0]
            stmt = Secret.delete().where(Secret.c.id==prevOtp.id)
            conn.engine.execute(stmt)
        otp = random.randint(100000, 999999)
        now = datetime.now()
        date = str(now.strftime("%Y-%m-%d %H:%M:%S"))

        stmt = Secret.insert().values(phone = phone,otp=otp,date = date,type = a)
        conn.engine.execute(stmt)
        return AuthHandler.sendOtp(phone=phone,otp=otp)

    def updatePassword(phone,password):
        hashMethod = PassHash()
        stmt = Users.update().where(
            Users.c.phone==phone
        ).values(password_hash = hashMethod.hash(password))
        try:
            conn.engine.execute(stmt)
            return True
        except Exception as e:
            print(e)
            return False

    def getSessionToken(user_id):
        stmt = select([Sessions]).where(and_(Sessions.c.user_id==user_id,Sessions.c.is_expired==2))
        try:
            return conn.engine.execute(stmt).one()
        except:
            return None

    def deletePreviousToken(session):
        stmt = Sessions.delete().where(Sessions.c.id == session.id)
        try:
            conn.engine.execute(stmt)
        except :
            pass

    def insertSessionToken(user_id,token,timestamp,expiry,type=2):
        stmt = Sessions.insert().values(
            user_id=user_id,
            login_token=token,
            created_at=timestamp,
            expires_at=expiry,
            is_expired=type
        )
        try:
            conn.engine.execute(stmt)
            return True
        except Exception as e:
            print(e)
            return False

    def createUser(name,phone,password,email):
        hashMethod = PassHash()
        if AuthHandler.isEmailExist(email):
            return USER_ALREADY_EXISTED
        passwordHash = hashMethod.hash(password)
        apiKey = hashMethod.generateApiKey()
        userName = AuthHandler.createUserName(name)
        stmt = Users.insert().values(
            name=name,
            phone=phone,
            password_hash=passwordHash,
            email = email,
            username=userName,
            api_key=apiKey,
            status=1
        )
        try:
            conn.engine.execute(stmt)
            return USER_CREATED_SUCCESSFULLY
        except Exception as e:
            print(e)
            return USER_CREATE_FAILED

    def verifyOtp(phone,otp):
        stmt = select([Secret]).where(and_(Secret.c.phone==phone))
        res = conn.engine.execute(stmt).fetchall()
        if(len(res)>0):
            res = res[0]
            if res.otp == otp:
                now = datetime.now().timestamp()
                sendTime = res.date
                sendTimeInFloat = datetime.strptime(
                    sendTime, "%Y-%m-%d %H:%M:%S").timestamp()
                validTime = 900.0
                if((now - sendTimeInFloat)) > validTime:
                    return 1
                else:
                    stmt = Secret.delete().where(Secret.c.id==res.id)
                    conn.engine.execute(stmt)
                    return 0
            else :
                return 2
        else:
            return 2
    
    def checkLogin(phone,password):
        res = AuthHandler.getUserByPhone(phone)
        hashMethod = PassHash()
        if res is not None:
            passwordHash = res.password_hash
            if(hashMethod.check_password(hash=passwordHash,password=password)):
                return True
            else : 
                return False
        return False



    def createUserName(name):
        stmt = text('SELECT COUNT(*) as count from users')
        count = conn.engine.execute(stmt).one().count
        name = name.split(" ")[0]
        return name+str(count)

    def isEmailExist(email):
        stmt = select([Users]).where(and_(Users.c.email==email))
        try:
            return conn.engine.execute(stmt).one() is not None
        except :
            return False

    def sendOtp(phone,otp):
        url = "http://mysms.sms7.biz/rest/services/sendSMS/sendGroupSms"
        params = {
            "AUTH_KEY": "4ae9995144e1811ffe5b63103151847a",
            "message": f"{otp} is the OTP for ExamHelper. Valid for 15 minutes.\nMsgId: lzrRoj3hcEz",
            "senderId": "EXMHLP",
            "routeId": '8',
            "mobileNos": phone,
            "smsContentType": 'english'
        }
        res = requests.get(url=url, params=params)
        result = res.json()
        # Status code == 3001 mean otp successfully send
        return result['responseCode'] == '3001'

    def isValidApiKey(api_key):
        stmt = select([Users]).where(and_(Users.c.api_key == api_key))
        try:
            return conn.engine.execute(stmt).fetchall() is not None
        except Exception as e:
            print(e)
            return False

    def getUserByApiKey(api_key):
        stmt = select([Users]).where(and_(Users.c.api_key == api_key))
        try:
            return conn.engine.execute(stmt).one()
        except Exception as e:
            print(e)
            return None
        
