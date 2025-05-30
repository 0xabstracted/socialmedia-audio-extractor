git pull origin main 
docker-compose down --volumes --remove-orphans
docker rmi socialmedia-audio-extractor_audio-extractor
docker system prune -f
docker image prune -a -f
docker-compose -f docker-compose.simple.yml down
docker-compose -f docker-compose.simple.yml up -d --build
python3 test_api.py
