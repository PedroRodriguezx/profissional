
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum

# Definir o caminho de entrada e saída no S3
input_path = "<>/input/public/lambda_hours/"
output_path = "<>/output/spark/TimePerEmployee"

def main():
    spark = SparkSession.builder.appName('Time and UserName').getOrCreate()
    # Replace CSV read with Parquet read
    all_data = spark.read.parquet(input_path)


    # Convert 'Time' column to numeric type (assuming it contains time values)
    all_data = all_data.withColumn("Time", col("Time").cast("float"))

    # Group by 'UserName' and sum the 'Time' column
    grouped_data = all_data.groupBy("UserName").agg(sum("Time").alias("TotalTime"))
    grouped_data.show(200)

    print('Total number of records in the source data: %s' % all_data.count())
    print('Total number of hours that each UserName worked: %s' % grouped_data.count())

    # Save the grouped data to S3 in Parquet format
    grouped_data.write.parquet(output_path, mode='append')


    print('Successfully saved to S3: %s' % output_path)

if __name__ == '__main__':
    main()
