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
DB_NAME = "balance"


Base = declarative_base()


class Data(Base):
    __tablename__ = "data"
    id = Column(Integer, Sequence("data_id_seq"), primary_key=True)
    left_weight = Column(Integer, nullable=False)
    left_distance = Column(Integer, nullable=False)
    right_weight = Column(Integer, nullable=False)
    right_distance = Column(Integer, nullable=False)
    class_name = Column(String, nullable=False)

    @staticmethod
    def add(data):
        new_data = Data(class_name=data[0], \
            left_weight=data[1], left_distance=data[2], \
            right_weight=data[3], right_distance=data[4])

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
        names = [Data.class_name, Data.left_weight, Data.left_distance, Data.right_weight, Data.right_distance]
        for i in range(1,5):
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
    names = ["class", "left_weight", "left_distance", "right_weight", "right_distance"]
    dataset = pd.read_csv(file_path, names=names)
    for data in dataset.values:
        Data.add(data)


def benchmark():
    right = 0
    wrong = 0

    query = session.query(Data).all()
    for c_data in query:
        vect = [c_data.class_name, c_data.left_weight, c_data.left_distance, c_data.right_weight, c_data.right_distance]
        res_class = naive_bayes.classify(Data, vect)
        if res_class == c_data.class_name:
            right += 1
        else:
            wrong += 1

    return (right * 100) / (right + wrong)
