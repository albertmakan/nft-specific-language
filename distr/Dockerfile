FROM node:18-alpine

WORKDIR /app

COPY . .

RUN npm i

# spm api
EXPOSE 3000

# ipfs swarm
EXPOSE 4002
EXPOSE 4003

# ipfs gateway
EXPOSE 8080
EXPOSE 8081

CMD [ "npm", "start" ]