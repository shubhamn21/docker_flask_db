docker build -t shubham:api-image-final ./api\ image/
docker build -t shubham:database-final-image ./database-image/database/
docker-compose -f docker-compose.yml up 
