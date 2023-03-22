FROM node:16.18.1 AS base

WORKDIR /app

COPY . .

FROM node:16.18.1 AS build-docs

WORKDIR /app/spm-docs

COPY --from=base /app/spm-docs .

RUN npm i
RUN npm run build

FROM node:16.18.1 AS final

WORKDIR /app

COPY --from=build-docs /app/spm-docs/build ./spm-docs/build
COPY --from=base /app/src ./src
COPY --from=base /app/package.json .

RUN npm i

# spm api
EXPOSE 3000

# ipfs swarm
EXPOSE 4002
EXPOSE 4003

# ipfs gateway
EXPOSE 9090
EXPOSE 9091

CMD [ "npm", "start" ]