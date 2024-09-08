import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import datetime


args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

current_date = datetime.datetime.now().strftime("%Y-%m-%d")
# Script generated for node Amazon S3
weather_dyf = glueContext.create_dynamic_frame.from_options(
    format_options={"quoteChar": "\"", "withHeader": True, "separator": ","}, 
    connection_type="s3", 
    format="csv", 
    connection_options={
        "paths": [f"s3://weather-data-landing-zone-zn/date={current_date}/weather_api_data.csv"], 
        "recurse": True
        },
        transformation_ctx="weather_dyf"
        )

# Script generated for node Change Schema
ChangeSchema_weather_dyf = ApplyMapping.apply(
    frame=weather_dyf, 
    mappings=[
        ("dt", "string", "dt", "string"), 
        ("weather", "string", "weather", "string"),
        ("visibility", "string", "visibility", "string"), 
        ("`main.temp`", "string", "temp", "string"), 
        ("`main.feels_like`", "string", "feels_like", "string"),
        ("`main.temp_min`", "string", "temp_min", "string"), 
        ("`main.temp_max`", "string", "temp_max", "string"), 
        ("`main.pressure`", "string", "pressure", "string"), 
        ("`main.sea_level`", "string", "sea_level", "string"), 
        ("`main.grnd_level`", "string", "ground_level", "string"), 
        ("`main.humidity`", "string", "humidity", "string"),  
        ("`wind.speed`", "string", "wind", "string"),
        ],
        transformation_ctx="ChangeSchema_weather_dyf")


redshift_output = glueContext.write_dynamic_frame.from_options(
    frame = ChangeSchema_weather_dyf,
    connection_type = "redshift",
    connection_options={
        "redshiftTmpDir":"s3://aws-glue-assets-861276114026-us-east-1/temporary/",
        "useConnectionProperties":"true",
         "dbtable":"public.weather_data",
        "aws_iam_role":"arn:aws:iam::861276114026:role/service-role/AmazonRedshift-CommandsAccessRole-20240908T203537",
        "connectionName": "Redshift-connection-General",
        "preactions":"DROP TABLE IF EXISTS public.weather_data; CREATE TABLE IF NOT EXISTS public.weather_data (dt VARCHAR, weather VARCHAR, visibility VARCHAR, temp VARCHAR, feels_like VARCHAR, min_temp VARCHAR, max_temp VARCHAR, pressure VARCHAR, sea_level VARCHAR, ground_level VARCHAR, humidity VARCHAR, wind VARCHAR);"
    },
    transformation_ctx="redshift_output",
)

job.commit()