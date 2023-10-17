import os

from sqlalchemy import create_engine, text

db_connection_string = os.environ['DB_CONNECTION_STR']

engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                           "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def load_jobs():
  with engine.connect() as conn:
    result = conn.execute(
        text('select * from careers where job_status = "ACTIVE"'))
    jobs = []
    for row in result.all():
      jobs.append(row)
    return jobs


def load_tenders():
  with engine.connect() as conn:
    result = conn.execute(
        text('select * from tenders where tender_status ="ACTIVE"'))
    tenders = []
    for row in result.all():
      tenders.append(row)
    return tenders
