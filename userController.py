from src.constants.const import *
from datetime import datetime
from src.authentication.authHandler import AuthHandler as handler

def checkPhone(phone):
    if handler.checkPhone(phone):
        result = {
            "error": False,
            "navigation_code": 1,
            "navigation_type": "login",
            "message": "Phone number alrady exist, Proceed to login."
        }
    else:
        res = handler.createNewSecret(phone=phone, a=1)
        if(res):
            result = {
                'error': False,
                'navigation_code': 2,
                'navigation_type': 'register',
                'message': "An OTP has been sent to your mobile, Proceed to register."
            }
        else:
            result = {
                'error': True,
                'message': "Oops! An error occurred while sending OTP"
            }
    return result

def registerUser(otp,name,phone,password,email):
    otpRes = verifyOtp(otp=otp,phone=phone)
    if(otpRes['error']):
        return otpRes
    res = handler.createUser(name=name,phone=phone,password=password,email=email)
    if(res == USER_CREATED_SUCCESSFULLY):
        result = {
            'error' : False,
            'message' : "You are successfully registered" 
        }
        user = handler.getUserByPhone(phone=phone)
        if(user is not None) : 
            timestamp = int(datetime.now().timestamp())
            expiry = timestamp+2592000
            token = f"{timestamp}.{user.api_key}.{expiry}"
            res = handler.insertSessionToken(user_id=user.id,token=token,timestamp = timestamp,expiry = expiry)
            if(res) :
                return {
                        "error" : False,
                        "userid" : user.id,
                        "name" : user.name,
                        "phone" : user.phone,
                        "email" : user.email,
                        "username" : user.username,
                        "image" : user.image,
                        "apiKey" : token,
                        "createdAt" : user.created_at
                    }
            return {
                'error' : True,
                'message' : 'An error occurred. Please try again'
            }
        else :
            return {
                'error' : True,
                'message' : 'An error occurred. Please try again'
            }
    else :
        result = {
            'error' : True,
            'message' : "Error creating user" 
        }
    return result

def verifyOtp(otp, phone):
    try:
        res = handler.verifyOtp(phone=phone, otp=int(otp))
        if(res == 0):
            result = {
                'error': False,
                'message': 'Otp verified successfull'
            }
        elif (res == 1):
            result = {
                'error': True,
                'message': "Otp is expired",
                'server_diff': res
            }
        elif(res == 2):
            result = {
                'error': True,
                'message': 'Invalid otp'
            }
    except:
        result = {
            'error': True,
            'message': 'Otp format is bad'
        }
    return result

def login(phone,password):
    if handler.checkLogin(phone=phone,password=password):
        user = handler.getUserByPhone(phone=phone)
        if(user is not None):
            session = handler.getSessionToken(user_id=user.id)
            if session is not None:
                handler.deletePreviousToken(session)
            timestamp = int(datetime.now().timestamp())
            expiry = timestamp+2592000
            token = f"{timestamp}.{user.api_key}.{expiry}"
            handler.insertSessionToken(user_id=user.id,token=token,timestamp = timestamp,expiry = expiry)
            return {
                    "error" : False,
                    "userid" : user.id,
                    "name" : user.name,
                    "phone" : user.phone,
                    "email" : user.email,
                    "username" : user.username,
                    "image" : user.image,
                    "apiKey" : token,
                    "createdAt" : user.created_at
                }
        else :
            return {
            'error' : True,
            'message' : "An error occurred. Please try again"
        }
    else : 
        return {
            'error' : True,
            'message' : 'Login failed. Incorrect credentials'
        }


def generateOtp(phone):
    res = handler.createNewSecret(phone=phone,a = 2)
    if(res):
        return {
            "error":False,
            "message" : "An OTP has been sent to your mobile."
        }
    return {
        "error":True,
        "message" : "Oops! An error occurred while sending OTP"
    }

def resetPassword(otp,phone,password):
    otpRes = verifyOtp(otp=otp,phone=phone)
    if(otpRes['error']):
        return otpRes
    res = handler.updatePassword(phone=phone,password=password)
    if(res):
        return {
            "error":False,
            "message":"Password updated successfully"
        }
    return {
            "error":True,
            "message":"Password updation failed."
        }
    


