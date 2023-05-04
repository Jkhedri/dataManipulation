from pyspark.sql import SparkSession

# create a SparkSession
spark = SparkSession.builder.appName("CSV to Parquet").getOrCreate()

# read the CSV/JSON file into a Spark DataFrame
df = spark.read.csv("snartparquet.csv", header=True, inferSchema=True)

# write the DataFrame to a Parquet file
df.write.parquet("aaaaaaaaaaaaa.parquet")

# stop the SparkSession
spark.stop()
