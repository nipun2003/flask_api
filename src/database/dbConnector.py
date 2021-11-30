from src.constants.const import SQLALCHEMY_DATABASE_URI as dataUrl
import sqlalchemy as db

class DbConnector:
    def __init__(self) -> None:
        self.engine = db.create_engine(dataUrl)
        self.meta_data = db.MetaData(bind=self.engine)
        db.MetaData.reflect(self.meta_data)