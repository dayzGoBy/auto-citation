## Телеграм-бот, подбирающий цитату к фотографии человека на основе его настроения  ([ссылка на бота](https://t.me/AutoCitationBot))

*Проект выполнен в рамках трека «ИИ и культурное наследие» в университете ИТМО*

*Над проектом работали: Грушевский Георгий (М3237) и Беляев Олег (М3236)*

## Использованные ресурсы:
[qdrant](https://github.com/qdrant/qdrant-client) - база данных для семантического поиска

[yorickvp/llava-13b](https://replicate.com/yorickvp/llava-13b/versions) - модель для описания фотографий

[sentence-transfromers/paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2) - энкодер для текста

Вы можете поднять бота локально с помощью docker

```docker-compose up --build```

Для этого вам понадобится .env файл с api-токенами от TelegramAPI, qdrant-client и replicate