# How to use the benchmark?

Tested with **python 3.8** and **python 3.9**

1. `python -m pip install virtualenv`
2. `python -m virtualenv env`
3. Activate virtual enviorment by: `source env/bin/activate` or `env/Scripts/activate` on windows.
4. Install dependencies: `python -m pip install -r srcrequirements.txt`
5. Edit _config.yml_. There are some further instructions on what each fields represents. 
6. Run benchmark: `python src/benchmarker.py`


### Config.yml
---

[Yaml anchors](https://docs.ansible.com/ansible/latest/user_guide/playbooks_advanced_syntax.html): To not repeat yourself.

For each system we can define a set of databases where our data is hosted. 
Each source must contain:
- **image**: Docker image. In further iterations this should be optional. We can already have preconfigured databases which we can connect using the jdbc url.
- **url**: JDBC url. 
- **user**: Database username
- **password**: Databse password
- **tables**: A list of tables which we know are hosted on the actual database. For this iteration we are creating the defined tables and filling them with the required data.
- **ports**: Database port mapping. local:external/docker.
- **volumes**: Predifined docker volumes where we save database configurations, so that data is not lost after we restart containers.

In addition to sources queries, metrics and scale_factors need to be defined.
- **queries**: must be a list. E.g.: [q1] or [q1,q2,"q5:q10"] but it **cannot be only q1**. The last option is problematic. 
- **metrics**: This corresponds to the benchmark outputs. Processing time is the default. 
- **scale_factors**: Because we based this benchmark on TPC-H generated data we give the option for choosing on what workload should the benchmark run. 


### How to extend the framework for further systems?
---
At src/systems there is a abstract class called System from which every new system should inherit. 
As such every system should implement the following methods:
- **setup**: Everything that is required to startup a system. That could be crating a docker image which we use locally or in cloud. In cases the system is already configured this method can be left unimplemented. That means: pass
- **run_query**: (requried) This method has two imputs: 
    - Sql: string ->  Rendered sql query
    - Show: boolean -> True in order to display the query output
- **post_startup**: After starting up a system there still can be some configuration required. This method is however not required for every system. 