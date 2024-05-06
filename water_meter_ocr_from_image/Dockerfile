ARG BUILD_FROM=homeassistant/amd64-base:latest
FROM $BUILD_FROM

# Copy data for add-on
COPY run.sh /
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]