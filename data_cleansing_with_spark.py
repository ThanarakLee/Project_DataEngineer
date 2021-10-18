
# ลง Spark ใน Google Colab
!apt-get update
!apt-get install openjdk-8-jdk-headless -qq > /dev/null
!wget -q https://archive.apache.org/dist/spark/spark-2.4.5/spark-2.4.5-bin-hadoop2.7.tgz
!tar xzvf spark-2.4.5-bin-hadoop2.7.tgz
!pip install -q findspark==1.3.0

# Set enviroment variable ให้รู้จัก Spark
import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-2.4.5-bin-hadoop2.7"

# ลง pyspark ผ่านคำสั่ง pip
!pip install pyspark==2.4.5

"""#### ใช้งาน Spark

ใช้ `local[*]` เพื่อเปิดการใช้งานการประมวลผลแบบ multi-core. Spark จะใช้ CPU ทุก core ที่อนุญาตให้ใช้งานในเครื่อง.
"""

# Server ของ Google Colab มีกี่ Core
!cat /proc/cpuinfo

# สร้าง Spark Session
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").getOrCreate()

# Get Python version
import sys
sys.version_info

# Get Spark version
spark.version


# เชื่อมต่อ Google colab กับ Google Drive
from google.colab import drive
drive.mount('/content/drive')

"""## Load data

ใช้คำสั่ง `spark.read.csv` เพื่ออ่านข้อมูลจากไฟล์ CSV

Arguments:

Header = True << บอกให้ Spark รู้ว่าบรรทัดแรกในไฟล์ CSV เป็น Header


Inferschema = True << บอกให้ Spark พยายามเดาว่าแต่ละ column มี type เป็นอะไร ถ้าตั้งเป็น False, ทุก column จะถูกอ่านเป็น string
"""

dt = spark.read.csv('/content/drive/My Drive/Data Science Chill/Online 2020: Road to Data Engineer/Workshop Files/WS2/Data Files/Online Retail WS2.csv', header = True, inferSchema = True, )

"""### Data Profiling

Data Profiling is a process of analysing summary of the data.

Example: max, min, average, sum, how many missing values etc.

#### Data

> Columns
- InvoiceNo
- StockCode
- Description
- Quantity
- InvoiceDate
- UnitPrice
- CustomerID
- Country
"""

dt

dt.show()

dt.show(100)

# Show Schema
dt.dtypes

# Show Schema (อีกแบบ)
dt.printSchema()

# นับจำนวนแถวและ column
print((dt.count(), len(dt.columns)))

# สรุปข้อมูลสถิติ
dt.describe().show()

# สรุปข้อมูลสถิติ
dt.summary().show()

# สรุปข้อมูลสถิติเฉพาะ column ที่ระบุ
dt.select("Quantity", "UnitPrice").describe().show()

"""### Exercise: ลองเช็ค Median ของ ค่า Quantity"""

# Write Answer here
dt.select("Quantity").summary().collect()[5]['Quantity']

"""
## EDA - Exploratory Data Analysis

### Non-Graphical EDA
"""

# Select text-based information
dt.where(dt['Quantity'] < 0).show()


# Quantity 50 - 120
dt.where( (dt['Quantity'] > 50) & (dt['Quantity'] < 120) ).show()

# UnitPrice 0.1 - 0.5
dt.where( (dt['UnitPrice'] >= 0.1) & (dt['UnitPrice'] <= 0.5) ).show()

# Quantity 50 - 120 and UnitPrice 0.1 - 0.5
dt.where(dt['Quantity'].between(50,120) & dt['UnitPrice'].between(0.1,0.5)).show()

"""### Graphical EDA
Spark ไม่ได้ถูกพัฒนามาเพื่องาน plot ข้อมูล เพราะฉะนั้นเราจะใช้ package `seaborn` `matplotlib` และ `pandas` ในการ plot ข้อมูลแทน
"""

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# แปลง Spark Dataframe เป็น Pandas Dataframe
dt_pd = dt.toPandas()

dt_pd.head()

# เลือกข้อมูล 500 แถวแรกเพื่อความรวดเร็วและความเรียบง่ายในการ visualize ข้อมูล
dt_pd_subset = dt_pd[0:500]

# Boxplot
sns.boxplot(dt_pd_subset['UnitPrice'])

# Histogram
sns.distplot(dt_pd_subset['UnitPrice']) 
plt.show()

# Scatterplot
dt_pd_subset.plot.scatter('UnitPrice', 'Quantity')

"""#### interactive chart"""

# Plotly - interactive chart
import plotly.express as px
fig = px.scatter(dt_pd_subset, 'UnitPrice', 'Quantity')
fig.show()

"""### Type Conversion

แปลง `InvoiceDate` จาก string -> date
"""

# Show top 5 rows
dt.show(5)

# Show Schema
dt.printSchema()

"""Is the date DD/MM/YYYY or MM/DD/YYYY? Let's find out


"""

# Show unique Invoice Date
dt.select("InvoiceDate").distinct().show()

# แปลง string เป็น date
from pyspark.sql import functions as f

# dt_temp = dt.withColumn('InvoiceDateTime', functions.to_date(
#     functions.unix_timestamp('InvoiceDate', 'dd/MM/yyyy HH:mm').cast('timestamp')
# ))

dt_temp = dt.withColumn('InvoiceDateTime', 
    f.unix_timestamp('InvoiceDate', 'dd/MM/yyyy HH:mm').cast('timestamp')
)
dt_temp.show()

dt_temp.printSchema()

dt_final = dt_temp.drop('InvoiceDate')
dt_final.show()

dt_final.printSchema()

"""## Data Cleansing with Spark
"""

# Check country distinct values. Find something interesting?
# ดูชื่อประเทศ
dt_final.select("Country").distinct().show()

dt_final.where(dt_final['Country'] == 'EIREs').show()

# เปลี่ยน EIREs เป็น EIRE
from pyspark.sql.functions import when

dt_temp_eire = dt_final.withColumn("CountryUpdate", when(dt_final['Country'] == 'EIREs', 'EIRE').otherwise(dt_final['Country']))

# Check the result
dt_temp_eire.select("CountryUpdate").distinct().show()

# Create final Dataframe
dt_final_eire = dt_temp_eire.drop("Country").withColumnRenamed('CountryUpdate', 'Country')

dt_final_eire.show()

"""#### Semantic Anomalies

**Integrity constraints**: ค่าอยู่นอกเหนือขอบเขตของค่าที่รับได้ เช่น
- Stockcode: ค่าจะต้องเป็นตัวเลข 5 ตัว
"""

dt_final_eire.select("Stockcode").show(100)

dt_final_eire.count()

dt_final_eire.filter(dt_final_eire["Stockcode"].rlike("^[0-9]{5}$")).count()

# ลองดูข้อมูลที่ถูกต้อง
dt_final_eire.filter(dt_final_eire["Stockcode"].rlike("^[0-9]{5}$")).show(5)

# ลองดูข้อมูลที่ไม่ถูกต้อง
dt_correct_stockcode = dt_final_eire.filter(dt_final_eire["Stockcode"].rlike("^[0-9]{5}$"))
dt_incorrect_stockcode = dt_final_eire.subtract(dt_correct_stockcode)

dt_incorrect_stockcode.show(10)


# ลบตัวอักษรตัวสุดท้ายออกจาก stock code
from pyspark.sql.functions import regexp_replace

dt_temp_stockcode = dt_final_eire.withColumn("StockcodeUpdate", regexp_replace(dt_final_eire['Stockcode'], r'[A-Z]', ''))

# Check the result
dt_temp_stockcode.show()

# Create final Dataframe
dt_final_stockcode = dt_temp_stockcode.drop("Stockcode").withColumnRenamed('StockcodeUpdate', 'StockCode')

dt_final_stockcode.show(4)

"""#### Missing values

การเช็คและแก้ไข Missing Values (หากจำเป็น)
"""

# Check จำนวน missing values ในแต่ละ column
from pyspark.sql.functions import col,sum

dt_final_stockcode.select(*[sum(col(c).isNull().cast("int")).alias(c) for c in dt_final_stockcode.columns]).show()

# Check ว่ามีแถวไหนที่ description เป็น null บ้าง

dt_final_stockcode.where( dt_final_stockcode['Description'].isNull() ).show()

# Check ว่ามีแถวไหนที่ customerID เป็น null บ้าง

dt_final_stockcode.where( dt_final_stockcode['customerID'].isNull() ).show()

"""### Exercise:
ทางทีม Data Analyst แจ้งว่าอยากให้เราแทน Customer ID ที่เป็น NULL ด้วย -1
"""

# Write code here
dt_customer_notnull = dt_final_stockcode.withColumn("CustomerIDUpdate", when(dt_final_stockcode['customerID'].isNull(), -1).otherwise(dt_final_stockcode['customerID']))

dt_customer_notnull.show()

"""### Clean ข้อมูลด้วย Spark SQL

![alt text](https://cdn-std.droplr.net/files/acc_513973/881iHw)

เลือกเฉพาะข้อมูลที่ `unitPrice` กับ `Quantity` ถูกต้อง (มากกว่า 0)
"""

dt_final_stockcode.createOrReplaceTempView("sales")
dt_sql = spark.sql("SELECT * FROM sales")
dt_sql.show()

dt_sql_count = spark.sql("SELECT count(*) as cnt_row FROM sales")
dt_sql_count.show()

dt_sql_count = spark.sql("SELECT count(*) as cnt_row, country FROM sales GROUP BY Country ORDER BY cnt_row DESC")
dt_sql_count.show()

dt_sql_valid_price = spark.sql("SELECT count(*) as cnt_row FROM sales WHERE UnitPrice > 0 AND Quantity > 0")
dt_sql_valid_price.show()

dt_sql_valid_price = spark.sql("SELECT * FROM sales WHERE UnitPrice > 0 AND Quantity > 0")
dt_sql_valid_price.show()


# Country USA ที่มี InvoiceDateTime ตั้งแต่วันที่ 2010-12-01 เป็นต้นไป และ UnitPrice เกิน 3.5
dt_sql_usa = spark.sql("""
SELECT * FROM sales
  WHERE InvoiceDateTime >= '2010-12-01'
  AND UnitPrice > 3.5
  AND Country='USA'
""").show()

# Country France ที่มี InvoiceDateTime ตังแต่วันที่ 2010-12-05 เป็นต้นไป และ UnitPrice เกิน 5.5 และ Description มีคำว่า Box
dt_sql_france = spark.sql("""
SELECT * FROM sales
  WHERE UnitPrice > 5.5
  AND InvoiceDateTime >= '2010-12-05'
  AND Country = 'France'
  AND LOWER(Description) LIKE '%box%'
""")

"""## Save cleaned data เป็น CSV

โดยปกติแล้ว Spark จะทำการ Save ออกมาเป็นหลายไฟล์ เพราะใช้หลายเครื่องในการประมวลผล
"""

# Write as partitioned files (use multiple workers)
dt_sql_valid_price.write.csv('Cleaned_Data_Now_Final.csv')

"""เราสามารถบังคับให้ Spark ใช้เครื่องเดียวได้"""

# Write as 1 file (use single worker)
dt_sql_valid_price.coalesce(1).write.csv('Cleaned_Data_Now_Final_Single.csv')


# สำคัญ: แก้โค้ดด้านล่างนี้เป็นชื่อไฟล์ที่ Spark สร้างขึ้นมาใน Google Drive เพราะชื่อไฟล์จะสุ่มสร้างออกมา ถ้ารันโดยไม่แก้เลยจะ Error
# อ่าน CSV ไฟล์ที่ 1
part1 = spark.read.csv('/content/Cleaned_Data_Now_Final.csv/part-00000-5c261eef-4f45-41e6-a0ba-9d29af6f0a1f-c000.csv', header = True, inferSchema = True, )
part1.count()

# สำคัญ: แก้โค้ดด้านล่างนี้เป็นชื่อไฟล์ที่ Spark สร้างขึ้นมาใน Google Drive เพราะชื่อไฟล์จะสุ่มสร้างออกมา ถ้ารันโดยไม่แก้เลยจะ Error
# อ่าน CSV ไฟล์ที่ 2
part2 = spark.read.csv('/content/Cleaned_Data_Now_Final.csv/part-00001-b357b1dd-f38e-459c-83ff-6e73bd6ebb0d-c000.csv', header = True, inferSchema = True, )
part2.count()

# วิธีอ่าน CSV ทุกไฟล์ในโฟลเดอร์นี้
all_parts = spark.read.csv('/content/Cleaned_Data_Now_Final.csv/part-*.csv', header = True, inferSchema = True, )

all_parts.count()
