# pull official base image
FROM node:17.3.0-alpine

# set working directory
WORKDIR /frontend

# add `/app/node_modules/.bin` to $PATH
ENV PATH /frontend/node_modules/.bin:$PATH

# install frontend dependencies
COPY package.json ./
COPY package-lock.json ./
RUN npm install
RUN npm install react-scripts@5.0.0 -g

# add app
COPY . ./

# start app
CMD ["npm", "start"]
