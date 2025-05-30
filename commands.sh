git pull origin main 
docker-compose down --volumes --remove-orphans
docker rmi socialmedia-audio-extractor_audio-extractor
docker system prune -f
docker image prune -a -f
docker-compose build --no-cache
docker-compose up -d
python3 test_api.py