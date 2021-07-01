ENV_FILE = hadoop.env
HADOOP_NETWORK = hadoop_default

build:
	docker build -t hadoop-base ./base
	docker build -t hadoop-namenode ./namenode
	docker build -t hadoop-datanode ./datanode
	docker build -t hadoop-resourcemanager ./resourcemanager
	docker build -t hadoop-nodemanager ./nodemanager
	docker build -t hadoop-timelineserver ./timelineserver

hadoop-test:
	docker build -t hadoop-test ./test
	docker run --network ${HADOOP_NETWORK} --env-file ${ENV_FILE} hadoop-test