## Телеграм-бот, подбирающий цитату к фотографии человека на основе его настроения  ([ссылка на бота](https://t.me/AutoCitationBot))

*Проект выполнен в рамках трека «ИИ и культурное наследие» в университете ИТМО*
*Над проектом работали: Грушевский Георгий (М3237) и Беляев Олег (М3236)*

## Использованные ресурсы:
[qdrant](https://github.com/qdrant/qdrant-client) - база данных для семантического поиска

[deepface](https://github.com/serengil/deepface) - модель для распознавания эмоций на фотографии

[seara/rubert-base-cased-ru-go-emotions](https://huggingface.co/seara/rubert-base-cased-ru-go-emotions) - модель для распознавания эмоций в тексте

Вы можете поднять бота локально с помощью docker

```docker-compose up --build```

Для этого вам понадобится .env файл с api-токенами от TelegramAPI, qdrant-client и huggingface