FROM ccnmtl/django.base
ADD wheelhouse /wheelhouse
RUN apt-get update && apt-get install -y libxml2-dev libxslt-dev
RUN /ve/bin/pip install --no-index -f /wheelhouse -r /wheelhouse/requirements.txt \
  && rm -rf /wheelhouse
WORKDIR /app
COPY . /app/
RUN /ve/bin/flake8 /app/spokehub/ --max-complexity=5 \
  && /ve/bin/python manage.py test \
  && npm install
EXPOSE 8000
ADD docker-run.sh /run.sh
ENV APP spokehub
ENTRYPOINT ["/run.sh"]
CMD ["run"]
