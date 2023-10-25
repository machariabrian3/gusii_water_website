import logging
import os
from datetime import datetime

from flask import session
from sqlalchemy import create_engine, text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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


def load_all_tenders():
  with engine.connect() as conn:
    result = conn.execute(text('select * from tenders order by id desc'))
    tenders = []
    for row in result.all():
      tenders.append(row)
    return tenders


def authenticate_user(email, password):
  with engine.connect() as conn:
    result = conn.execute(
        text(
            'SELECT * FROM accounts WHERE email = :email AND password = :password and status = "ACTIVE"'
        ), {
            'email': email,
            'password': password
        })
    user = result.fetchone()
    return user


def insert_tender(data, filename):
  user_id = session.get('id')

  if user_id is None:
    logger.error("User not authenticated")
    return "User not authenticated"

  logger.info(f"Data received here : {str(data)}")

  with engine.connect() as conn:
    query = text("""
        INSERT INTO tenders
        (created_by, title, description, publish_date, closing_date, doc_url, tender_status, created_date, updated_date)
        VALUES
        (:created_by, :title, :description, :publish_date, :closing_date, :doc_url, 'ACTIVE', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """)

    parameters = {
        "created_by": user_id,
        "title": data["title"],
        "description": data["description"],
        "publish_date": datetime.strptime(data["publishDate"], "%Y-%m-%d"),
        "closing_date": datetime.strptime(data["closingDate"], "%Y-%m-%d"),
        "doc_url": filename
    }

    try:
      conn.execute(query, parameters)
      logger.info(f"Tender inserted successfully. : {str(parameters)}")
    except Exception as e:
      logger.error(f"Error inserting tender(db): {str(e)}")


def close_tender(data):
  user_id = session.get('id')

  if user_id is None:
    logger.error("User not authenticated")
    return "User not authenticated"

  logger.info(f"Data received here : {str(data)}")

  with engine.connect() as conn:
    query = text("""
        UPDATE tenders
        SET tender_status = 'CLOSED',
            updated_date = CURRENT_TIMESTAMP,
            updated_by = :updated_by
        WHERE id = :tender_id
    """)
    parameters = {
        "updated_by": user_id,  # Updated_by field
        "tender_id": data["tender_id"],  # The tender ID you want to update
    }
    try:
      conn.execute(query, parameters)
      logger.info(f"Tender updated successfully. : {str(parameters)}")
    except Exception as e:
      logger.error(f"Error updated tender(db): {str(e)}")


def load_all_careers():
  with engine.connect() as conn:
    result = conn.execute(text('select * from careers order by id desc'))
    careers = []
    for row in result.all():
      careers.append(row)
    return careers


def insert_career(data, filename):
  user_id = session.get('id')

  if user_id is None:
    logger.error("User not authenticated")
    return "User not authenticated"

  logger.info(f"Data received here : {str(data)}")

  with engine.connect() as conn:
    query = text("""
        INSERT INTO careers
        (created_by, title, requirements, responsibilities, doc_url, job_status, created_date, updated_date)
        VALUES
        (:created_by, :title, :requirements, :responsibilities, :doc_url, 'ACTIVE', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """)

    parameters = {
        "created_by": user_id,
        "title": data["title"],
        "requirements": data["requirements"],
        "responsibilities": data["responsibilities"],
        "doc_url": filename
    }

    try:
      conn.execute(query, parameters)
      logger.info(f"Career inserted successfully. : {str(parameters)}")
    except Exception as e:
      logger.error(f"Error inserting career(db): {str(e)}")


def close_careers(data):
  user_id = session.get('id')

  if user_id is None:
    logger.error("User not authenticated")
    return "User not authenticated"

  logger.info(f"Data received here : {str(data)}")

  with engine.connect() as conn:
    query = text("""
        UPDATE careers
        SET job_status = 'CLOSED',
            updated_date = CURRENT_TIMESTAMP,
            updated_by = :updated_by
        WHERE id = :career_id
    """)
    parameters = {
        "updated_by": user_id,  # Updated_by field
        "career_id": data["career_id"],  # The tender ID you want to update
    }
    try:
      conn.execute(query, parameters)
      logger.info(f"Career updated successfully. : {str(parameters)}")
    except Exception as e:
      logger.error(f"Error updated career(db): {str(e)}")
