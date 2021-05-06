FROM python:3.8

RUN pip install pandas

COPY run.sh /run.sh
RUN chmod a+x /run.sh

COPY python_generator.py /python_generator.py

CMD ["/run.sh"]