from api.db.models import DataBaseRecord
from api.db.database import engine
import pandas as pd
import json

def show_records(db):
    records = db.query(DataBaseRecord).all()
    return records

def show_record(emis_id,db):
    records = db.query(DataBaseRecord).get([emis_id])
    return records

def create_record(request,db):
    db_record = DataBaseRecord(
            emis = request.emis,
            centre_no = request.centre_no,
            name = request.name,

            wrote_2014 = request.wrote_2014,
            passed_2014 = request.passed_2014,
            wrote_2015 = request.wrote_2015,
            passed_2015 = request.passed_2015,
            wrote_2016 = request.wrote_2016,
            passed_2016 = request.passed_2016,

            province = request.province,

            pass_rate_2014 = round(request.passed_2014/request.wrote_2014*100,2),
            pass_rate_2015 = round(request.passed_2015/request.wrote_2015*100,2),
            pass_rate_2016 = round(request.passed_2016/request.wrote_2016*100,2)
        )
    db.add(db_record)
    db.commit()
    return request

del_key = lambda d: d.pop('_sa_instance_state')
row2dict = lambda r: r.__dict__

def deliver_charts(db):
    records = db.query(DataBaseRecord).all()
    df = pd.read_sql_table("Records", engine)
    charts = {
            "schools_in_province":
            {"labels":df.groupby('province').name.count().index.tolist() ,
            "series":[df.groupby('province').name.count().values.tolist()]},
            "wrote_2014_province":
            {"labels":df.groupby('province').wrote_2014.sum().index.tolist(),
            "series":[df.groupby('province').wrote_2014.sum().values.tolist(),
                    df.groupby('province').wrote_2015.sum().values.tolist(),
                    df.groupby('province').wrote_2016.sum().values.tolist()]},
            "passrate_2014_province":
            {"labels":(df.groupby('province').passed_2014.sum()/df.groupby('province').wrote_2014.sum()).index.tolist(),
            "series":[(df.groupby('province').passed_2014.sum()/df.groupby('province').wrote_2014.sum()).values.tolist(),
                    (df.groupby('province').passed_2015.sum()/df.groupby('province').wrote_2015.sum()).values.tolist(),
                    (df.groupby('province').passed_2016.sum()/df.groupby('province').wrote_2016.sum()).values.tolist()]},
        
            }
    return json.dumps(charts)
    # records = list(map(row2dict,records))
    # print(records)
    # records = list(map(del_key,records))
    # print(records)
    # df =  pd.read_sql(records, db)
    # print(df)