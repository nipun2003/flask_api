from flask import Blueprint, request, jsonify
from src.video.aws import getPresignedUrl
import videoController
from src.authentication.authHandler import AuthHandler as handler

video = Blueprint("video", __name__, url_prefix="/api/v1/video")

@video.get('/sample')
def getVideo():
    key = 'Nagpuri/Kahani/sohrai.mp4'
    resp = getPresignedUrl(key=key)
    return jsonify(resp)

@video.get('/get_video_courses')
def getVideoCourses():
    return videoController.getVideoCourse()

@video.get('/get_all_videos')
def getAllVideos():
    courseId = request.args.get('course_id')
    return videoController.getAllVideos(courseId)

@video.get('/create_source')
def getVideoSouce():
    res = checkHeader()
    if(res['error']):
        return res
    user_id = res['user_id']
    id = request.args.get('video_id')
    quality= request.args.get('quality')
    return videoController.createVideoSource(user_id=user_id,id=id)

def checkHeader():
    header = request.headers.get('Authorization')
    response = {'error':False}
    if header is None:
        response['error'] = True
        response['error_code'] = 1
        response['message'] = "Session token is misssing"
    else:
        split = header.split('.')
        print(split)
        if(len(split) == 3):
            timestamp = split[0]
            api_key = split[1]
            print(api_key)
            expiry = split[2]
            if(not handler.isValidApiKey(api_key)):
                response['error'] = True
                response['error_code'] = 2
                response['message'] = "Access Denied. Invalid session token"
            else :
                user_id=None
                user = handler.getUserByApiKey(api_key=api_key)
                if(user is not None):
                    user_id = user.id
                response['user_id'] = user_id
        else:
            response['error'] = True
            response['error_code'] = 2
            response['message'] = "Access Denied. Invalid session token Split length not 3"
    return response

    

