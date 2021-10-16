# -*- coding: utf-8 -*-
"""
## Install PyMySQL 
ซึ่งเป็น package สำหรับเชื่อมต่อ MySQL database
"""

! pip install pymysql

"""## Config DB credential
วิธีด้านล่างนี้เป็นวิธีที่ไม่ปลอดภัย ที่เราใช้ใน workshop นี้เพราะจะได้เห็นวิธีการ connect กับ database
"""

class Config:
  MYSQL_HOST = '34.136.184.58'
  MYSQL_PORT = 3306  # default port ของ MySQL คือ 3306
  MYSQL_USER = 'r2de'
  MYSQL_PASSWORD = 'DataScience-chillchill'
  MYSQL_DB = 'r2de_ws1'
  MYSQL_CHARSET = 'utf8mb4'

"""## Connect to DB
หลังจากที่มี Credential ของ database 
"""

import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host=Config.MYSQL_HOST,
                             port=Config.MYSQL_PORT,
                             user=Config.MYSQL_USER,
                             password=Config.MYSQL_PASSWORD,
                             db=Config.MYSQL_DB,
                             charset=Config.MYSQL_CHARSET,
                             cursorclass=pymysql.cursors.DictCursor)

connection

"""ตัวแปร connection นี้ เราได้ connect ต่อเข้ากับ database เอาไว้แล้ว
## List Tables
ตรวจสอบว่ามี Tables อะไรบ้าง
"""

# list all tables
cursor = connection.cursor()
cursor.execute("show tables;")
tables = cursor.fetchall()
cursor.close()
print(tables)

"""จากโค้ดตัวอย่างด้านบนจะเห็นได้ว่า การคิวรี่ database ทุกครั้ง เราจะต้องสร้าง `cursor` ขึ้นมาเพื่อ query SQL นั้น แล้วก็ปิด cursor ทุกครั้งหลังจบ 
ดังนั้น จึงนิยมใช้คำสั่ง `with` ในการจัดการสร้าง cursor ขึ้นมา เมื่อจบคำสั่ง cursor จะถูก close ไปเองโดยอัตโนมัติเมื่อออกนอก scope ของ `with`
## Query Table
"""

# ใข้ with statement แทน cursor.close()
# Query ข้อมูลจาก table online_retail 

with connection.cursor() as cursor:
  # Read a single record
  sql = "SELECT * FROM online_retail;"
  cursor.execute(sql)
  result = cursor.fetchall()

print("number of rows: ", len(result), "⁀⊙﹏☉⁀")

type(result)

"""Row มีเยอะเกินไปจึงต้องใช้ Pandas เข้ามาช่วย
## Convert to Pandas
"""

import pandas as pd

retail = pd.DataFrame(result)

type(retail)


"""Data ที่ได้
"""
retail

"""---


# Get data from REST API

หลังจากต่อกับ Database แล้ว ก็มายิง REST API

Package `requests` ใช้สำหรับการยิง REST API

(โดยปกติต้อง install package นี้เพิ่มเติม แต่ colab pre-install ไว้อยู่แล้ว)

วิธีการ install: `pip install requests`
"""

import requests

"""ลองคลิกดูผลลัพธ์ผ่าน web browser ได้ [Currency conversion API](https://de-training-2020-7au6fmnprq-de.a.run.app/currency_gbp/all) 

ผลลัพธ์ที่ return กลับมาจะเป็นประเภท JSON
จึงต้องใช้ package `json` (built-in) เพื่อโหลดข้อมูลเป็น dictionary

การที่เราสามารถยิง request และ output ออกมาได้เลยโดยที่ไม่ต้องสร้าง payload เพิ่ม ดังตัวอย่างนี้ เรียกว่า HTTP GET (ในกรณีอื่น ๆ สามารถเพิ่ม arguement หรือ query string เข้าไปใน URL ได้)


"""

url = "https://de-training-2020-7au6fmnprq-de.a.run.app/currency_gbp/all"
# เขียนโค้ดเพื่อ call URL นี้

response = requests.get(url)
response.text

response.json()

"""ดูประเภทข้อมูล"""

type(response.text)

"""## JSON loading
แต่ JSON ที่เราเห็นมันเป็นเพียงแค่ string

เราจะแปลง string ให้กลายเป็น dictionary!

เราเลยต้อง import `json` (built-in package)
"""

import json


? json

result = response.json()
result

# ลองอ่าน string JSON ที่ได้รับ ให้กลายเป็น dictionary
result_conversion_rate = json.loads(response.text)
result_conversion_rate

"""เช็คประเภทข้อมูล"""

print(type(result_conversion_rate))
assert isinstance(result_conversion_rate, dict)

""" ## Convert to Pandas
"""

conversion_rate = pd.DataFrame.from_dict(result_conversion_rate)

conversion_rate[:3]

conversion_rate = conversion_rate.reset_index().rename(columns={"index":"date"})
conversion_rate[:3]

conversion_rate[:3]

"""ที่ต้องใช้ `.from_dict()` เพราะว่า ข้อมูลมี key ที่แตกต่างกันออกไป คือ index ที่เป็นเวลา เพราะฉะนั้น `.from_dict()` จึงเข้ามาช่วนการโหลดข้อมูลลักษณะแบบนี้

# Join the data

ในตอนนี้เราจะนำข้อมูลการซื้อขายและข้อมูล Rate การแปลงค่าเงิน เราจะรวมข้อมูลจากทั้งสอง Dataframe มารวมกัน

เราจะนำข้อมูลจากทั้งสองมารวมกันผ่าน column InvoiceDate ใน retail และ date ใน conversion_rate 

แต่ถ้าสังเกตดีๆ แล้วจะพบว่า InvoiceDate ใน retail จะเก็บข้อมูลในรูปแบบ datetime ส่วน date ใน conversion_rate จะเก็บข้อมูลในรูปแบบ timestamp ที่ส่วนเวลาเป็นเวลา 00:00:00 ทั้งหมด
"""

retail

# ก็อปปี้ column InvoiceDate เก็บเอาไว้ เผื่อได้ใช้ในอนาคต ไม่งั้นข้อมูล timestamp ของเราจะหายไป
retail['InvoiceTimestamp'] = retail['InvoiceDate']
retail

# แปลงให้ InvoiceDate ใน retail กับ date ใน conversion_rate มีเฉพาะส่วน date ก่อน
retail['InvoiceDate'] = pd.to_datetime(retail['InvoiceDate']).dt.date
conversion_rate['date'] = pd.to_datetime(conversion_rate['date']).dt.date

retail.head()

# รวม 2 dataframe เข้าด้วยกันด้วยคำสั่ง merge
final_df = retail.merge(conversion_rate, how="left", left_on="InvoiceDate", right_on="date")
final_df

"""พอ join ข้อมูลได้แล้ว เราก็ มา คูณ currency conversion กัน (UnitPrice * Rate)"""

# เพิ่ม column 'THBPrice' ที่เกิดจาก column UnitPrice * Rate
final_df["THBPrice"] = final_df["UnitPrice"] * final_df["Rate"]
final_df

def convert_rate(price, rate):
  return price * rate

final_df["THBPrice"] = final_df.apply(lambda x: x["UnitPrice"]* x["Rate"], axis=1)

final_df["THBPrice"] = final_df.apply(lambda x: convert_rate(x["UnitPrice"], x["Rate"]), axis=1)
final_df

"""## Save to CSV"""
final_df.to_csv("output.csv", index=False)

