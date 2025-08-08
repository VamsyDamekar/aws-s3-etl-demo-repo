import sys
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col, count, when, round

# ✅ Get arguments from Glue job parameters
args = getResolvedOptions(sys.argv, ["SOURCE_BUCKET", "OUTPUT_BUCKET"])
bucket = args["SOURCE_BUCKET"]
output_bucket = args["OUTPUT_BUCKET"]

# ✅ Create Glue context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# 📁 Load CSV files from S3
base_path = f"s3://{bucket}/data/"

customer_df = spark.read.option("header", True).csv(base_path + "customer.csv")
account_df = spark.read.option("header", True).csv(base_path + "account.csv")
transaction_df = spark.read.option("header", True).csv(base_path + "transaction.csv")

# 🔁 Ensure join keys are strings
customer_df = customer_df.withColumn("customer_id", col("customer_id").cast("string"))
account_df = account_df.withColumn("customer_id", col("customer_id").cast("string")) \
                       .withColumn("account_id", col("account_id").cast("string"))
transaction_df = transaction_df.withColumn("account_id", col("account_id").cast("string"))

# 🔗 Join customer → account → transaction
cust_acc_df = customer_df.join(account_df, on="customer_id", how="inner")
final_df = cust_acc_df.join(transaction_df, on="account_id", how="inner")

# 🧪 1. Check for missing/null values
print("🔍 Null value count per column:")
null_counts = final_df.select([
    count(when(col(c).isNull(), c)).alias(c) for c in final_df.columns
])
null_counts.show(truncate=False)

# 🧾 2. Check for duplicate rows
print("🔍 Duplicate row count:")
duplicates = final_df.groupBy(final_df.columns).count().filter("count > 1")
duplicates.show(truncate=False)

# 🛠 3. Fill missing values (example: email)
final_df = final_df.fillna({"email": "unknown@example.com"})

# ➕ 4. Add derived column: amount in dollars
final_df = final_df.withColumn("amount_dollars", round(col("amount_cents") / 100, 2))

# 💾 5. Save to S3 as Parquet
output_path = f"s3://{output_bucket}/output/cleaned_data/"
final_df.write.mode("overwrite").parquet(output_path)

print(f"✅ ETL job completed. Data written to {output_path}")
