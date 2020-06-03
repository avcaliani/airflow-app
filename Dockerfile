FROM python:3

ENV AIRFLOW_HOME="/airflow"
WORKDIR $AIRFLOW_HOME

RUN pip install -q typing_extensions==3.7.4.2 apache-airflow==1.10.10

RUN airflow version
RUN sed -i -e "s/load_examples = True/load_examples = False/g" $AIRFLOW_HOME/airflow.cfg

RUN printf 'airflow initdb \n' > init.sh && \
    printf 'airflow webserver -p 80 & \n' >> init.sh && \
    printf 'airflow scheduler & \n' >> init.sh && \
    printf 'tail -f /dev/null \n' >> init.sh

CMD /bin/bash $AIRFLOW_HOME/init.sh
