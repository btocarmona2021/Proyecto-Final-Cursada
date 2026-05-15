find . -name "views.py" -type f -exec sh -c 'echo "\n\n========== {} ==========\n" && cat {}' \; > todos_los_views.txt

find . -name "models.py" -type f -exec sh -c 'echo "\n\n========== {} ==========\n" && cat {}' \; > todos_los_models.txt                                                          

find . -name "urls.py" -type f -exec sh -c 'echo "\n\n========== {} ==========\n" && cat {}' \; > todos_los_urls.txt

find ./interface -name "*.ts" -type f -exec sh -c 'echo "\n\n========== {} ==========\n" && cat {}' \; > interfaces.txt

python manage.py runserver 8000

python manage.py makemigrations

python manage.py migrate

docker compose --env-file .env --env-file .env.user down

docker compose --env-file .env --env-file .env.user up -d

find ./src/interfaces -name "*.ts" -type f -exec sh -c 'echo "\n\n========== {} ==========\n" && cat {}' \; > interfaces.txt

find ./src/services -name "*.ts" -type f -exec sh -c 'echo "\n\n========== {} ==========\n" && cat {}' \; > services.txt

find ./frontend/src/stores -name "*.ts" -type f -exec sh -c 'echo "\n\n========== {} ==========\n" && cat {}' \; > stores.txt

find . \
  -type f \( -name "*.vue" -o -name "*.js" -o -name "*.ts" \) \
  -exec sh -c 'echo "\n\n========== {} ==========\n" && cat "{}"' \; \
  > proyecto.txt






