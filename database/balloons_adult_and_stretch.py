from sqlalchemy import Column, ForeignKey, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine, func
import pandas as pd

from classifiers import naive_bayes

DB_DIALECT = "postgresql"
DB_UNAME = "mecker"
DB_PASSWORD = "redhot12"
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "balloon_adult_and_scretch"


Base = declarative_base()


class Data(Base):
    __tablename__ = "data"
    id = Column(Integer, Sequence("data_id_seq"), primary_key=True)
    color = Column(String, nullable=False)
    size = Column(String, nullable=False)
    act = Column(String, nullable=False)
    age = Column(String, nullable=False)
    class_name = Column(String, nullable=False)

    @staticmethod
    def add(data):
        new_data = Data(class_name=data[4], \
            color=data[0], size=data[1], \
            act=data[2], age=data[3])

        session.add(new_data)
        session.commit()

    @staticmethod
    def calc_sum_class():
        result = {}
        query = session.query(Data.class_name, func.count(Data.class_name)).group_by(Data.class_name).all()
        for class_name, class_count in query:
            result[class_name] = class_count

        return result

    @staticmethod
    def calc_sum_data():
        query = session.query(Data).all()
        return len(query)

    @staticmethod
    def calc_sum_attributes(c_data, class_name):
        result = []
        names = [Data.color, Data.size, Data.act, Data.age, Data.class_name]
        for i in range(0,4):
            query = session.query(Data).filter((names[i] == c_data[i]) & \
                (Data.class_name == class_name)).all()
            result.append(len(query))

        return result


# initalize database
engine = create_engine("{}://{}:{}@{}:{}/{}".format(
    DB_DIALECT, DB_UNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME))
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# functions
def add_trainings_data_csv(file_path):
    names = ["color", "size", "act", "age", "class_name"]
    dataset = pd.read_csv(file_path, names=names)
    for data in dataset.values:
        Data.add(data)


def benchmark():
    right = 0
    wrong = 0

    query = session.query(Data).all()
    for c_data in query:
        vect = [c_data.color, c_data.size, c_data.act, c_data.age, c_data.class_name]
        res_class = naive_bayes.classify(Data, vect)
        if res_class == c_data.class_name:
            right += 1
        else:
            wrong += 1

    return (right * 100) / (right + wrong)
