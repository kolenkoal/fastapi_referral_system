FROM python:3.9

RUN mkdir /referral_system

WORKDIR /referral_system

COPY requirements/base.txt /tmp/base.txt

RUN python -m venv /py && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/base.txt && \
   rm -rf /tmp && \
   adduser \
       --disabled-password \
       --no-create-home \
       fastapiuser

RUN pip install alembic
RUN pip install pydantic-settings


COPY . .

RUN chmod a+x /referral_system/docker/*.sh

CMD ["sh", "-c", "alembic upgrade head && gunicorn src.app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000"]

USER fastapiuser