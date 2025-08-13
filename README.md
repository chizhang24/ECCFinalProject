# Scalability Benchmark: Multi-Node Sorting on Hadoop and Spark

This repository documents our final project for the Engineering Cloud Computing course. It explores the setup, benchmarking, and comparative analysis of distributed data processing frameworks — **Hadoop MapReduce** and **Apache Spark** — deployed in both **Docker-based environments** and on the **Jetstream2 cloud platform**.

---

## 📌 Objective

To evaluate and compare the performance, scalability, and efficiency of Hadoop MapReduce and Spark using the TeraSort benchmark in two deployment environments:
- **Docker (local container-based setup)**
- **Jetstream2 (cloud-based HPC environment)**

---

## 🧱 Project Components

Although not all files are tracked in this repo, the project includes the following core components:

- **Docker-based Hadoop MapReduce Setup**
  - Single-node and multi-node cluster setup
  - TeraGen and TeraSort execution
- **Docker-based Spark Setup**
  - Spark master-worker configuration using Bitnami images
  - Spark TeraSort benchmark using `spark-submit`
- **Jetstream2 Cloud Benchmarking**
  - Hadoop and Spark benchmarks replicated on Jetstream2 VMs
  - Cluster scaling (1–6 workers) and metric collection
- **Performance Metrics Analysis**
  - Wall time, I/O throughput, shuffle throughput
  - Memory & CPU usage, task reliability
  - Visualizations and plots generated using Python (optional)

---

## ⚙️ Setup Instructions

### Hadoop MapReduce on Docker

1. Clone Hadoop base repo:
   ```bash
   git clone https://github.com/big-data-europe/docker-hadoop.git
   cd docker-hadoop
   docker compose up -d
   ```

2. Run TeraGen and TeraSort:
   ```bash
   docker exec -it namenode bash
   hadoop jar /opt/hadoop-3.2.1/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.2.1.jar teragen 10000000 /input
   hadoop jar /opt/hadoop-3.2.1/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.2.1.jar terasort /input /output
   ```

---

### Spark on Docker

1. Add Spark services to `docker-compose.yml`:
   (Refer to the Bitnami Spark setup with master and worker roles.)

2. Execute Spark job:
   ```bash
   docker compose up -d spark-master spark-worker
   spark-submit --master spark://spark-master:7077 /opt/spark_terasort.py
   ```

---

### Hadoop MapReduce on Jetstream

1. Create Jetstream instances of m3.large flavor with 60GB RAM and 60GB Root Disk
   Start HDFS and YARN on the cluster
   ```bash
   $ $HADOOP_HOME/sbin/start-dfs.sh
   $ $HADOOP_HOME/sbin/start-yarn.sh
   ```
   
2. Generate data using Teragen:
   ```bash
   $ hadoop jar /opt/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar teragen 10000000 /input
   ```
   
3. Run Terasort:
 ```bash
   hadoop jar $HADOOP_HOME/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar \
   terasort /user/exouser/terasort-input /user/exouser/terasort-output
 ```

---

### Spark on Jetstream

1. Install Spark and start the services
   ```bash
    $SPARK_HOME/sbin/start-all.sh


3. Submit Spark job:
   ```bash
   $ spark-submit --master yarn --deploy-mode client --num-executors 6 --executor-cores 2 --executor-memory 1G /home/exouser/spark_terasort.py

   ```

---

## 📊 Performance Highlights

| Environment  | Framework        | Wall Time ↓ | Throughput ↑ | Notes |
|--------------|------------------|-------------|---------------|-------|
| Docker       | Hadoop MapReduce | Slower      | Moderate      | Easy to set up, limited scale |
| Docker       | Spark            | Faster      | Higher        | More efficient for sorting |
| Jetstream2   | Hadoop MapReduce | Variable    | High at scale | More stable under load |
| Jetstream2   | Spark            | Fastest     | Best          | Ideal for large jobs |

---

## 📌 Conclusion

 - We benchmarked 4 cloud platforms in shuffle heavy task (TeraSort) extensively
 - Analyzed the best scenarios where the platforms most suitably apply
 - For our task, Spark Docker has the best performance
---

## 👥 Contributors

- Chi Zhang - czh4@iu.edu
- Krishna Priya - fkrishna@iu.edu

---

## 📄 License

This project is for academic use under the Engineering Cloud Computing course - Indiana University Bloomington.

---
