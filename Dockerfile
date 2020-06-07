FROM python:3

ENV AIRFLOW_HOME="/airflow"
WORKDIR $AIRFLOW_HOME

RUN pip install -q \
    docker==4.2.1 \
    psycopg2==2.8.5 \
    typing_extensions==3.7.4.2 \
    apache-airflow==1.10.10 

RUN airflow version

RUN printf 'airflow initdb \n' > init.sh && \
    printf 'airflow webserver -p 80 & \n' >> init.sh && \
    printf 'airflow scheduler & \n' >> init.sh && \
    printf 'tail -f /dev/null \n' >> init.sh

CMD /bin/bash $AIRFLOW_HOME/init.sh
