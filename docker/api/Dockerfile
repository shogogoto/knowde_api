FROM python:3.9

WORKDIR /api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

COPY ./docker/api/requirements.txt .

RUN set -eux
# RUN apk add --no-cache build-base
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install --no-cache-dir --trusted-host pypi.python.org -r /api/requirements.txt
# RUN stty erase ^H # backspace効かないの修正 https://www.itmedia.co.jp/help/tips/linux/l0133.html
WORKDIR /api/app
EXPOSE 8000

# --host以降はdockerの場合は必要っぽい
#CMD ["python3", "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
# python3 -m uvicorn app.main:app --reload
# docker run -d --name knowde_api -p 8000:8000 -v ../:/api/app knowde_api

