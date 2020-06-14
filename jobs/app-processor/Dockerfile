FROM python:3

WORKDIR /app
ADD . .
RUN pip install -q -r requirements.txt
CMD python main.py --input "$INPUT" --output "$OUTPUT"
