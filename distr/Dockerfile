FROM node:16.18.1

WORKDIR /app

COPY . .

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