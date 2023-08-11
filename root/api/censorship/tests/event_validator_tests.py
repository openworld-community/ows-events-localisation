from root.api.censorship.main import EventsValidator

validator = EventsValidator

bads: list[str] = [
    'пидор',
    'пидорас',
    'пидорок',
    'пидр',
    'негр',
    'пизда',
    'хуе',
    'блять',
    'ебал',
    'ебло',
    'ебля',
    'ебу',
    'еби',
    'ебёт',
    'ебнутый',
    'хуею',
    'сука',
    'сцуко',
    'норм слово',
    'норм слово, но с хуй']

for word in bads:
    print(
        f'Результат проверки слова или фразы "{word}" -- {"забраковано" if not validator.validate_string(line=word) else "одобрено"}')
