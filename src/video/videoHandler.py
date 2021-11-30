from sqlalchemy.sql.expression import *
from src.database.dbConnector import DbConnector

conn = DbConnector()

videoCourse = conn.meta_data.tables['video_courses']
videos = conn.meta_data.tables['videos']
class VideoHandler:
    def getVideoCourse():
        query = text("SELECT *, id as course_id,"+
        "(SELECT count(*) from videos where video_course_id = course_id) as videos_count,"+
        "(SELECT sum(duration_sec) from videos where video_course_id = course_id) "+
        "as total_videos_duration from video_courses ")
        return conn.engine.execute(query).fetchall()
        
    def getAllVideos(courseId):
        stm = select([videos]).where(and_(videos.c.video_course_id==courseId))
        return conn.engine.execute(stm).fetchall()

    def fetchAllSubjectIn(subject_arr):
        subject_arr = ",".join(str(int) for int in subject_arr)
        query = f"""SELECT * from subjects where id in ({subject_arr})"""
        return conn.engine.execute(query).fetchall()
    def fetchVideoSource(videoId):
        stmt = select([videos]).where(and_(videos.c.id == videoId))
        try:
            return conn.engine.execute(stmt).one()
        except Exception as e:
            print(e)
            return None

