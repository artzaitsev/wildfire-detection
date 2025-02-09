FROM node:18 AS frontend-builder

ARG VITE_GOOGLE_MAPS_API_KEY

WORKDIR /app/web
COPY web/package.json web/package-lock.json ./

RUN npm ci

COPY web ./

RUN echo "::add-mask::$VITE_GOOGLE_MAPS_API_KEY"
RUN echo "VITE_GOOGLE_MAPS_API_KEY=$VITE_GOOGLE_MAPS_API_KEY" >> /app/.env

RUN npm run build

FROM python:3.9

WORKDIR /app

COPY --from=frontend-builder /app/web/dist /app/web/dist
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app

#CMD ["fastapi", "run", "cmd/service.py", "--port", "8000", "--proxy-headers"]
