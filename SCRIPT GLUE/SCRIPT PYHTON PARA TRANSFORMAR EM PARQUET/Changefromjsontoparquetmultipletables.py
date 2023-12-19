import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

table_names = [
<>
]

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

for table_name in table_names:
    datasource = glueContext.create_dynamic_frame.from_catalog(
        database="cloud-trail-lake",
        table_name=table_name,
        transformation_ctx="datasource",
        additional_options = {"jobBookmarkKeys":["requestid"],"jobBookmarkKeysSortOrder":"asc"}
    )

    applymapping1 = ApplyMapping.apply(
        frame=datasource,
        mappings=[
            ("eventversion", "string", "eventversion", "string"),
            ("eventtime", "string", "eventtime", "string"),
            ("eventsource", "string", "eventsource", "string"),
            ("eventname", "string", "eventname", "string"),
            ("userName", "string", "userName", "string"),
            ("awsregion", "string", "awsregion", "string"),
            ("sourceipaddress", "string", "sourceipaddress", "string"),
            ("useragent", "string", "useragent", "string"),
            ("requestparameters", "struct", "requestparameters", "string"),
            ("responseelements", "struct", "responseelements", "string"),
            ("requestid", "string", "requestid", "string"),
            ("eventid", "string", "eventid", "string"),
            ("eventtype", "string", "eventtype", "string"),
            ("recipientaccountid", "string", "recipientaccountid", "string"),
            ("resources", "array", "resources", "array"),
            ("sharedeventid", "string", "sharedeventid", "string"),
            ("errorcode", "string", "errorcode", "string"),
            ("errormessage", "string", "errormessage", "string"),
            ("apiversion", "string", "apiversion", "string"),
            ("readonly", "boolean", "readonly", "boolean"),
            ("additionaleventdata", "struct", "additionaleventdata", "string"),
            ("vpcendpointid", "string", "vpcendpointid", "string"),
            ("managementevent", "boolean", "managementevent", "boolean"),
            ("eventcategory", "string", "eventcategory", "string"),
            ("partition_0", "string", "region", "string"),
            ("partition_1", "string", "year", "string"),
            ("partition_2", "string", "month", "string"),
            ("partition_3", "string", "day", "string"),
            ("useridentity.type", "string", "useridentity_type", "string"),
            ("useridentity.principalId", "string", "useridentity_principalId", "string"),
            ("useridentity.arn", "string", "useridentity_arn", "string"),
            ("useridentity.accountId", "string", "useridentity_accountId", "string"),
            ("useridentity.invokedBy", "string", "useridentity_invokedBy", "string"),
            ("useridentity.accessKeyId", "string", "useridentity_accessKeyId", "string"),
            ("useridentity.userName", "string", "useridentity_userName", "string"),
            ("useridentity.sessionContext.attributes.mfaAuthenticated", "string", "useridentity_mfaAuthenticated", "string"),
            ("useridentity.sessionContext.attributes.creationDate", "string", "useridentity_creationDate", "string"),
            ("useridentity.sessionContext.sessionIssuer.type", "string", "useridentity_sessionIssuer_type", "string"),
            ("useridentity.sessionContext.sessionIssuer.principalId", "string", "useridentity_sessionIssuer_principalId", "string"),
            ("useridentity.sessionContext.sessionIssuer.arn", "string", "useridentity_sessionIssuer_arn", "string"),
            ("useridentity.sessionContext.sessionIssuer.accountId", "string", "useridentity_sessionIssuer_accountId", "string"),
            ("useridentity.sessionContext.sessionIssuer.userName", "string", "useridentity_sessionIssuer_userName", "string"),
            ("useridentity.sessionContext.ec2RoleDelivery", "string", "useridentity_ec2RoleDelivery", "string"),
            ("useridentity.sessionContext.webIdFederationData.key", "string", "useridentity_webIdFederationData_key", "string"),
            ("useridentity.sessionContext.webIdFederationData.value", "string", "useridentity_webIdFederationData_value", "string")
        ],
        transformation_ctx="applymapping1"
    )

    resolvechoice2 = ResolveChoice.apply(frame=applymapping1, choice="make_struct", transformation_ctx="resolvechoice2")

    resolvechoice = ResolveChoice.apply(
        frame=applymapping1,
        choice="make_struct",
        transformation_ctx="resolvechoice"
    )

    relationalized = resolvechoice.relationalize(table_name, args["TempDir"]).select(table_name)


    datasink = glueContext.write_dynamic_frame.from_options(
        frame=relationalized,
        connection_type="s3",
        connection_options={
            "path": f"s3://<>",
            "partitionKeys": ["region", "year", "month", "day"]
        },
        format="parquet",
        transformation_ctx="datasink"
    )

job.commit()
