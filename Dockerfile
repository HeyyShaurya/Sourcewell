FROM node:22-alpine
WORKDIR /app
COPY package.json server.mjs index.html app.js styles.css ./
COPY assets ./assets
ENV PORT=8080
EXPOSE 8080
CMD ["node", "server.mjs"]
