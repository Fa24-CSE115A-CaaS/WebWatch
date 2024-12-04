#!/bin/bash

# Take down services
docker-compose down

# Clone repo
cd /home/webwatch/app/WebWatch/
git fetch --all
git reset --hard origin/main
git status

# Change permission for scripts
chmod +x /home/webwatch/app/WebWatch/backend/.devcontainer/post-create-commands.sh /home/webwatch/app/WebWatch//backend/scraper-linux64/downloadchrome.sh 

# Build frontend
cd /home/webwatch/app/WebWatch/frontend
npm install
npm run build

# Copy build to nginx
rm -Rf /home/webwatch/nginx/html/*
cp -r /home/webwatch/app/WebWatch/frontend/dist/* /home/webwatch/nginx/html/

# Bring up services
docker-compose up -d
