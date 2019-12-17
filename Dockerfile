FROM python:3.7

RUN pip install dash==1.6.1 dash-daq==0.3.1 pandas gevent
RUN pip install dash_bootstrap_components Image cvxpy

ADD data /data
ADD assets /assets
ADD *.py /

# we pass -u to ensure that print output is shown in docker
CMD ["python", "-u", "flask_server.py"]
