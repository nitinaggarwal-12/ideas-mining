FROM python:3.12-slim
WORKDIR /app
COPY public ./public
COPY src ./src
COPY data ./data
COPY scripts ./scripts
COPY assets ./assets
COPY generated-repos ./generated-repos
COPY server.py ./server.py
ENV HOST=0.0.0.0
ENV PORT=8080
EXPOSE 8080
CMD ["python3", "server.py"]
