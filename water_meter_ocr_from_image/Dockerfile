ARG BUILD_FROM
FROM $BUILD_FROM

# Add env
ENV LANG C.UTF-8

RUN apk add --no-cache python3
RUN apk add cmd:pip3

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install .py script dependency
RUN pip3 install boto3 requests paho-mqtt pysmb pillow

# Copy data for add-on
COPY ocr_aws.py /
COPY run.sh /

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]