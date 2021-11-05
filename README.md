# Project Data Engineer
เป็น Project ที่แสดงถึงขั้นตอนการทำงานของ Data Engineer ในตัว Project นี้จะใช้ Google Cloud ในการทำงานเป็นหลัก

## สารบัญ
* Data Collection with Python & Pandas
* Data Cleansing with Spark
* Upload files to Data Lake
* Automated Data Pipeline whit Airflow
* Big Data Warehouse whit Google BigQuery
* Report & Dashboard whit Google Data Studio

## Data Collection with Python & Pandas
ทำ Data Collection ด้วย python โดยการเก็บข้อมูลจาก Database และ REST API ด้วย Python

### Input:
- อ่านข้อมูลจาก MySQL
- อ่านข้อมูลจาก REST API ด้วย Package Requests

### Output:
- Dataset ข้อมูลที่รวมแล้ว(CSV)



## Data Cleansing with Spark
เป็นการทำข้อมูลให้มีความสะอาดใช้งานง่าย ใน workshop นี้จะใช้ PySpark, Spark และ Pandas เพื่อให้ข้อมูลของเรามีคุณภาพ

### Input:
- ข้อมูลที่เราดึงมาแล้ว(CSV)
- Notebook ที่รองรับ PySpark, Spark และ Pandas ในที่นี้ใช้ Google Colab

### Output:
- ข้อมูลที่ทำความสะอาดเรียบร้อยแล้ว(CSV)



## Upload files to Data Lake
การอัพโหลดไฟล์เข้า Data Lake ในที่นี้จะใช้ Google Cloud Platform อัพโหลดเข้า Google Cloud Storage 



# Automated Data Pipeline whit Airflow
สร้าง Data Pipeline ใน Airflow เพื่อดึงข้อมูลแบบอัตโนมัติ ในที่นี้จะใช้ Google Cloud Composer ในการทำ



# Big Data Warehouse whit Google BigQuery
ใช้ Apache Airflow เพื่อโหลดข้อมูลเข้า BigQuery โดยอัตโนมัติ



## Report & Dashboard whit Google Data Studio
ทำ Dashboard ดึงข้อมูลจาก BigQuery เพื่อนำมารายงานผล
[Sarah Gift World Dashboard](https://datastudio.google.com/embed/u/0/reporting/6805ef50-0d56-4531-9cc3-7ec34a8843ea/page/O2KNC)


## Summary
สร้าง Pipeline ในการดึงข้อมูลจาก Database กับ API มาลงที่ Data Lake และเมีการก็บไว้ใน Data Warehouse แล้วทำให้เป็น Automated หลังจากนั้นทำการดึงข้อมูลมาใช้ โดยการทำเป็น Visualisation
