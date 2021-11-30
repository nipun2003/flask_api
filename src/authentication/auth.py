from flask import Blueprint, request, jsonify
import userController 
import re

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/check_phone')
def checkPhone():
    phone = request.args.get('phone')
    res = validate_not_mobile(phone)
    if(res['error']):
        return res
    phone = res['value']
    return jsonify(userController.checkPhone(phone=phone))

@auth.post('/register')
def registerUser():
    json = request.get_json()
    name = json['name']
    otp = json['otp']
    phone = json['phone']
    password = json['password']
    email = json['email']
    res = validate_not_mobile(phone)
    if(res['error']):
        return res
    phone = res['value']
    return jsonify(userController.registerUser(otp=otp,name=name,phone=phone,password=password,email=email))

@auth.post('/login')
def login():
    phone = request.args.get('phone')
    password = request.args.get('password')
    res = validate_not_mobile(phone)
    if(res['error']):
        return res
    phone = res['value']
    return jsonify(userController.login(phone=phone,password=password))

@auth.post('/reset_password')
def resetPassword():
    phone = request.args.get('phone')
    password = request.args.get('password')
    otp = request.args.get('otp')
    res = validate_not_mobile(phone)
    if(res['error']):
        return res
    phone = res['value']
    return jsonify(userController.resetPassword(otp=otp,phone=phone,password=password))


@auth.post('/generate_otp')
def generateOtp():
    phone = request.args.get('phone')
    res = validate_not_mobile(phone)
    if(res['error']):
        return res
    phone = res['value']
    return userController.generateOtp(phone)

def validate_not_mobile(value):
    value = str(value)
    if len(value) == 11 and value[0] == '0':
       value = value[1:]
    elif (len(value) == 12 and value[0:2] == "91"):
        value = value[2:]
    elif (len(value) == 13 and value[1:3] == "91"):
        value = value[3:]
    if(len(value)) == 10:
        return searchRule(value)
    return {
        'error':True,
        'message':"Phone number is not valid"
    }

def searchRule(value):
    value = str(value)
    rule = re.compile(r'(^[+0-9]{1,3})*([0-9]{10,11}$)')
    if rule.search(value):
        return {
            'error':False,
            'value':value
        }
    return {
        'error':True,
        'message':"Phone number is not valid"
    }

