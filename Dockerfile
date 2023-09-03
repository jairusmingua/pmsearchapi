FROM python:3.9.17-slim-bullseye
# upgrade pip
RUN pip install --upgrade pip
RUN apt-get update && apt-get install gcc make -y
RUN groupadd --gid 1000 pmsearchapi \
  && useradd --uid 1000 --gid pmsearchapi --shell /bin/bash --create-home pmsearchapi

USER pmsearchapi

WORKDIR /home/app

COPY --chown=pmsearchapi:pmsearchapi . .
RUN chmod +x ./start.sh
# setup python environment
ENV VIRTUAL_ENV=/home/app/venv 

# python setup
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install -r requirements.txt

# define the port number the container should expose
EXPOSE 8000

CMD ["/bin/bash", "./start.sh"]