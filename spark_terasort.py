import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import substring

spark = SparkSession.builder.appName("TeraSort").getOrCreate()
sc = spark.sparkContext
sc.setLogLevel("INFO")


NUM_WORKERS = 6  # Adjust manually based on setup
EXECUTOR_MEMORY_MB = 1024  # Verified from Spark UI
EST_BYTES_PER_ROW = 100    # TeraGen row is exactly 100 bytes

start_time = time.time()

# read teragen output data from hdfs
df = spark.read.text("hdfs://namenode:9000/input/")
input_count = df.count()
input_bytes = input_count * EST_BYTES_PER_ROW

# implement terasort
sorted_df = df.orderBy(substring("value", 1, 10))

#write the sorted data to HDFS
sorted_df.write.mode("overwrite").text("hdfs://namenode:9000/output/")
output_count = sorted_df.count()
output_bytes = output_count * EST_BYTES_PER_ROW

end_time = time.time()
wall_time = end_time - start_time

# metrics

shuffle_bytes = input_bytes + output_bytes
shuffle_throughput_MBps = shuffle_bytes / wall_time / (1024 ** 2)

agg_resource_util_ms = wall_time * 1000 * NUM_WORKERS
io_throughput_MBps_per_worker = (input_bytes + output_bytes) / (wall_time * NUM_WORKERS * 1024 ** 2)

cpu_efficiency = "N/A"
killed_tasks_per_worker = "N/A"



print("========== Spark TeraSort Benchmark ==========")
print(f"Number of Workers: {NUM_WORKERS}")
print(f"Wall Time: {wall_time:.2f} seconds")
print(f"Input Rows: {input_count}")
print(f"Output Rows: {output_count}")
print(f"Estimated Input Size: {input_bytes / 1024 ** 2:.2f} MB")
print(f"Estimated Output Size: {output_bytes / 1024 ** 2:.2f} MB")
print(f"Shuffle Throughput: {shuffle_throughput_MBps:.2f} MB/s")
print(f"Aggregate Resource Utilization: {agg_resource_util_ms:.2f} vcore-ms (approx)")
print(f"Memory Utilization per Worker: {EXECUTOR_MEMORY_MB:.2f} MB")
print(f"HDFS I/O Throughput per Worker: {io_throughput_MBps_per_worker:.2f} MB/s")
print(f"CPU Efficiency: {cpu_efficiency}")
print(f"Killed Tasks per Worker: {killed_tasks_per_worker}")
print("==============================================")

spark.stop()




