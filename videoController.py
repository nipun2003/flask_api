from sqlalchemy.sql.expression import false
from werkzeug.wrappers import response
from src.video.videoHandler import VideoHandler as handler
from src.video.aws import getPresignedUrl

def getVideoCourse():
    response = {'error':False,'course':[]}
    arr = handler.getVideoCourse()
    for item in arr:
        courseItem = {
            'id':int(item.id),
            'pid':int(item.pid),
            'name':item.title_en,
            'nameHi':item.title_hi,
            'description':item.description_en,
            'descriptionHi':item.description_hi,
            'price':float(item.price),
            'image':item.image,
            'totalVideos':item.videos_count,
            'totalDurationMins':int((int(item.total_videos_duration)/60)),
            'updatedOn':item.updated_at
        }
        response['course'].append(courseItem)
    return response

def getAllVideos(courseId):
    courseId = int(courseId)
    response = {
        'error':False,
        'videos':[],
        'subjects':[]
    }

    arr = handler.getAllVideos(courseId=courseId)
    subjectArr = []
    for item in arr:
        subjectArr.append(item.subject_id)
        course = {
            'id':int(item.id),
            'subjectId':int(item.subject_id),
            'title':item.title_en,
            'titleHi':item.title_hi,
            'source':item.source,
            'imageUrl':item.image,
            'price':float(item.size_kbytes),
            'durationSec':item.duration_sec,
            'updatedOn':item.updated_at,
            'isAvailable':bool(item.is_available)
        }
        response['videos'].append(course)
    subjectArr = list(set(subjectArr))
    response['subject_ids'] = subjectArr
    res = handler.fetchAllSubjectIn(subjectArr)
    for item in res:
        course = {
            'id':int(item.id),
            'nameEn':item.name_en,
            'nameHi':item.name_hi
        }
        response['subjects'].append(course)
    return response

def createVideoSource(user_id,id):
    id = int(id)
    video = handler.fetchVideoSource(id)
    response = {'error':False} 
    if(video is not None):
        key = video.key
        response['source'] = getPresignedUrl(key=key)
    else :
        response['source'] = ''
    return response

    