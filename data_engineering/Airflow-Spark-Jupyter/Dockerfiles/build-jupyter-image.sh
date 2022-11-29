# -- Software Stack Version

SPARK_VERSION="3.0.0"
HADOOP_VERSION="2.7"
JUPYTERLAB_VERSION="2.1.5"

docker build \
  -f 'cluster-base.Dockerfile' \
  -t cluster-base .

docker build \
  --build-arg spark_version="${SPARK_VERSION}" \
  --build-arg jupyterlab_version="${JUPYTERLAB_VERSION}" \
  -f 'jupyterlab.Dockerfile' \
  -t jupyterlab .