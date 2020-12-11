FROM python:3.8.5-alpine

ARG package

ENV FLASK_APP slothtamer
ENV SLOTHTAMER_API_KEY insecure

COPY dist/${package} ./
RUN pip install ${package}

EXPOSE 8080
ENTRYPOINT exec /bin/sh -c "waitress-serve --call 'slothtamer:create_app'"
