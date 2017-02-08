#start the images by building and recreating them
docker-compose down &&
docker-compose build &&
docker-compose up --force-recreate;
