from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, col, to_date, year, month, dayofmonth

def main():
    # Definir o caminho de entrada e saída
    input_path = "<>/input/public/lambda_hours/"
    output_path = "<>/output/spark/TimeAggregateperEmployeeInDate"

    # Cria uma sessão Spark
    spark = SparkSession.builder.appName('Time and UserName').getOrCreate()

    # Carrega os dados Parquet
    all_data = spark.read.option("header", "true").parquet(input_path)

    # Imprime o esquema do DataFrame
    print('Esquema do DataFrame all_data:')
    all_data.printSchema()

    # Certifique-se de que a coluna 'Time' é numérica
    all_data = all_data.withColumn("Time", col("Time").cast("float"))

    # Adiciona colunas de data usando a coluna 'LoggedAt'
    all_data = all_data.withColumn("Year", year(to_date(col("LoggedAt"))))
    all_data = all_data.withColumn("Month", month(to_date(col("LoggedAt"))))
    all_data = all_data.withColumn("Day", dayofmonth(to_date(col("LoggedAt"))))

    # Agrupa por 'Year', 'Month', 'Day', 'UserName' e 'EmpresaName' e calcula a soma do tempo
    grouped_data = all_data.groupBy("Year", "Month", "Day", "UserName").agg(sum("Time").alias("TotalTime"))

    grouped_data.show(200)

    # Salva o resultado particionado por data em Parquet
    grouped_data.write.parquet(output_path, mode='append')

    # Mostra algumas estatísticas
    print('Número total de registros nos dados de origem:', all_data.count())
    print('Número total de quantas horas foram gastas no dia:', grouped_data.count())

    print('Adicionado com sucesso em:', output_path)

if __name__ == "__main__":
    main()
