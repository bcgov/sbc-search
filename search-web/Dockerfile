FROM node:14.15.1 as build-stage
WORKDIR /app
COPY ./package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:1.18.0 as production-stage

ARG BUILD_DATE
ARG VCS_REF

LABEL build_date=$BUILD_DATE
LABEL vcs_ref=$VCS_REF

RUN echo "hello1"
COPY nginx.conf /etc/nginx/nginx.conf
RUN mkdir /app
COPY --from=build-stage /app/dist /app
EXPOSE 8080:8080
CMD ["nginx", "-g", "daemon off;"]
