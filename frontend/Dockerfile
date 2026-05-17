FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM node:20-alpine AS builder
WORKDIR /app
ARG API_BASE_URL
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN sed -i "s|http://YOUR-IP:YOUR-PORT/api|${API_BASE_URL}|g" \
    src/app/core/interceptors/api.config.ts
RUN npm run build -- --configuration production

FROM node:20-alpine AS dev
WORKDIR /app
ENV NODE_ENV=development
COPY --from=deps /app/node_modules ./node_modules
COPY . .
VOLUME ["/app/node_modules"]
EXPOSE 4200
CMD ["npm", "run", "start", "--", "--host", "0.0.0.0", "--poll", "500"]

FROM nginx:alpine AS runtime
ENV NGINX_ENTRYPOINT_QUIET_LOGS=1
COPY --from=builder /app/dist/angular-conduit /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]