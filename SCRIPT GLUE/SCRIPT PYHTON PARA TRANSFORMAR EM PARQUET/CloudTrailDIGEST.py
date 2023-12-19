import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="dev-db-parquet",
    table_name="sourcecloudtrail_digest",  
    transformation_ctx="datasource"
)
applymapping1 = ApplyMapping.apply(
    frame=datasource,
    mappings=[
        ("awsaccountid", "string", "awsaccountid", "string"),
        ("digeststarttime", "string", "digeststarttime", "string"),
        ("digestendtime", "string", "digestendtime", "string"),
        ("digests3bucket", "string", "digests3bucket", "string"),
        ("digests3object", "string", "digests3object", "string"),
        ("digestpublickeyfingerprint", "string", "digestpublickeyfingerprint", "string"),
        ("digestsignaturealgorithm", "string", "digestsignaturealgorithm", "string"),
        ("newesteventtime", "string", "newesteventtime", "string"),
        ("oldesteventtime", "string", "oldesteventtime", "string"),
        ("previousdigests3bucket", "string", "previousdigests3bucket", "string"),
        ("previousdigests3object", "string", "previousdigests3object", "string"),
        ("previousdigesthashvalue", "string", "previousdigesthashvalue", "string"),
        ("previousdigesthashalgorithm", "string", "previousdigesthashalgorithm", "string"),
        ("previousdigestsignature", "string", "previousdigestsignature", "string"),
        ("logfiles", "array", "logfiles", "array"),
        ("partition_0", "string", "region", "string"),
        ("partition_1", "string", "year", "string"),
        ("partition_2", "string", "month", "string"),
        ("partition_3", "string", "day", "string"),
    ],
    transformation_ctx="applymapping"
)
resolvechoice2 = ResolveChoice.apply(frame = applymapping1, choice = "make_struct", transformation_ctx = "resolvechoice2")
relationalized3 = resolvechoice2.relationalize("trail", args["TempDir"]).select("trail")
datasink4 = glueContext.write_dynamic_frame.from_options(frame=relationalized3, connection_type="s3", 
connection_options={"path": "s3://<>" + "/parquet", "partitionKeys": ["region", "year", "month", "day"]},
 format="parquet", transformation_ctx="datasink4")


job.commit()





#########################################

