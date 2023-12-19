from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, col

def main():
    # Definir o caminho de entrada e saída
    input_path = "<>/input/public/lambda_hours/"
    output_path = "<>/output/spark/TimeAggregateperEmployeeInEachCustomer"

    # Cria uma sessão Spark
    spark = SparkSession.builder.appName('Time and EmpresaName').getOrCreate()

    # Carrega os dados CSV
    all_data = spark.read.option("header", "true").parquet(input_path)

    # Imprime o esquema do DataFrame
    print('Esquema do DataFrame all_data:')
    all_data.printSchema()

    # Certifique-se de que a coluna 'Time' é numérica
    all_data = all_data.withColumn("Time", col("Time").cast("float"))

    # Agrupa por 'UserName' e 'EmpresaName' e calcula a soma do tempo
    grouped_data = all_data.groupBy("UserName", "EmpresaName").agg(sum("Time").alias("TotalTime"))

    # Salva o resultado em um parquet
    grouped_data.write.parquet(output_path, mode='append')


    # Mostra algumas estatísticas
    print('Número total de registros nos dados de origem:', all_data.count())
    print('Número total de horas que cada UserName gastou em cada EmpresaName:', grouped_data.count())

    print('Adicionado com sucesso em:', output_path)

if __name__ == "__main__":
    main()
