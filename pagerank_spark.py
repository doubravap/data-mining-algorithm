#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 17 20:53:16 2018

@author: junewang
"""
from pyspark.sql import SparkSession
from pyspark.sql import Row


spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

df = spark.read.csv('/Users/junewang/Desktop/sparkcode/sales.csv', header=True, inferSchema=True)    
df.show()
df.printSchema()

##create an rdd for dataframe
dfrdd=df.rdd
dfrdd.take(3)
###Q1:Find all distinct countries.
df_country=df.select("Country").distinct()
df_country.show()   

###Q2:Find the Name and Price of sales records in Brazil.
df_Brazil=df.filter("Country='Brazil'")\
        .select("Name","Price")\
        .show()
df_Brazil=df.filter("Country='Brazil'").select("Name","Price").show() 
    
##Q3:For each country, find the total Price.
df_price=df.groupBy("Country").sum("Price").show()

##Q4:List countries by their total Price in descending order.
##groupby一定要有sum()和show()才能展示出来
df_order=df.select('*')\
                .groupBy("Country")\
                .sum("Price")\
                .withColumnRenamed('sum(Price)','totalprice')\
                .orderBy('totalprice',ascending=False)\
                .select('Country')
df_order.show()      

##Q5:Redo Question 3, but replace the country names by their IDs.
df2 = spark.read.csv('/Users/junewang/Desktop/sparkcode/countries.csv', header=True, inferSchema=True)
df2.show()

df_price=df.groupBy("Country").sum("Price")
df_price_id=df_price.join(df2,"Country")\
            .select("ID","sum(Price)")
df_price_id.show()

###page ranke
from pyspark.sql.functions import *
from pyspark.sql import functions
numOfIterations = 10
#lines = spark.read.text("/Users/junewang/Desktop/sparkcode/pagerank_data.txt")
# You can also test your program on the follow larger data set:
lines = spark.read.text("/Users/junewang/Desktop/sparkcode/dblp.in")
a = lines.select(split(lines[0],' '))
links = a.select(a[0][0].alias('src'), a[0][1].alias('dst'))
outdegrees = links.groupBy('src').count()
ranks = outdegrees.select('src', lit(1).alias('rank'))
links = links.withColumn("score", functions.lit(0)).join(outdegrees,"src").join(ranks,"src")

for iteration in range(numOfIterations):
    links = links.withColumn("score", links["rank"]/links["count"])
    links1=links.select("dst","score")
    ####dst可以理解为出度，和下一次的入度进行匹配
    ranks=links1.groupBy('dst').sum("score").withColumnRenamed("sum(score)","rank")
    ranks=ranks.withColumn("src",ranks["dst"]).drop('dst')
    ranks=ranks.withColumn("rank", 0.85*ranks["rank"]+0.15)
    links=links.drop("rank")
    links=links.join(ranks,'src')
ranks.show()
ranks.orderBy(desc('rank')).show()









    
    
    
    
    