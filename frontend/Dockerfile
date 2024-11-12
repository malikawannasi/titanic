# Dockerfile pour le frontend
FROM node:16-alpine

WORKDIR /app

# Copier seulement package.json
COPY package.json ./

# Si yarn.lock existe, copiez-le. Sinon, ignorez cette ligne.
COPY yarn.lock ./

RUN yarn install  # ou `npm install` si vous utilisez npm

# Copier le reste des fichiers de l'application
COPY . .

# Construire l'application pour la production
RUN yarn build  # ou `npm run build` si vous utilisez npm

CMD ["yarn", "start"]  # ou `CMD ["npm", "start"]` pour npm
