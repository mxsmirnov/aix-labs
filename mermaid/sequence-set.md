# Набор диаграмм последовательности (mermaid)

Несколько простых примеров mermaid диаграммами для учебного курса **"Проектируем ИТ-решения с использованием Cursor AI"**

## Предварительные замечания
* Markdown внутри Mermaid не поддерживаются. HTLML-вставки поддерживаются с оговорками

## Диаграмма 1 (версия 1)
```mermaid
sequenceDiagram
    participant U as User
    participant A as Agent
    participant T as Tool
    participant L as LLM

    U->>A: 1. Какая погода в Москве?
    A->>L: 2. Системный промпт + запрос + описание tool
    L-->>A: 3. Вызови функциию  get_weather('Москва')
    A->>T: 4. Вызов инструмента (API погоды)
    T-->>A: 5. Результат: "{'temp': '5°C', 'condition': 'ясно'}"
    A->>L: 6. Отправляем результата инструмента обратно в LLM
    L-->>A: 7. Финальный ответ: "В Москве сейчас +5°C и ясно."
    A->>U: 8. Отвечаем пользователю
```
## Диаграмма 1 (версия 2)
Делаем несколько улучшений:
* добавляем группировку: _Агент_ и _Инструмент_ реализованы в виде монолитного _Приложения_ 
* под первой стрелкой размещаем примечание (с переносом строк)
* осваиваем добавление комментариев
* подсвечиваем запрос-ответ прямоугольником

```mermaid
sequenceDiagram
    participant U as 😎 User
     %% Комментарий должен быть вначале строки
    box Приложение
        participant A as ⚙️ Agent
        participant T as 🛠️ Tool
    end
    participant L as 🎲 LLM
    
    U->>A: 1. Какая погода в Москве?
    Note over U,A: LLM не знает текущую погоду в Москве<br/>Надо где-то спросить 
    
    A->>L: 2. Системный промпт + запрос + описание tool
    L-->>A: 3. Вызови функциию  get_weather('Москва')
    A->>T: 4. Вызов инструмента (API погоды)
    T-->>A: 5. Результат: "{'temp': '5°C', 'condition': 'ясно'}"
    rect rgb(232, 232, 232)
    A->>L: 6. Отправляем результата инструмента обратно в LLM
    L-->>A: 7. Финальный ответ: "В Москве сейчас +5°C и ясно."
    end
    A->>U: 8. Отвечаем пользователю

```

## Диаграмма 2
Стереотипы на диаграмме последовательности

```mermaid
sequenceDiagram
    participant Alice@{ "type" : "actor" }
    actor Bob
    Alice->>Bob: Hi!
```
## Диаграмма 2 (версия 2)
Стереотипы на диаграмме последовательности

```mermaid
sequenceDiagram
    participant Actor@{ "type" : "actor" }
    participant Interface@{ "type" : "boundary" }
    participant Process@{ "type" : "control" }
    participant Store@{ "type" : "database" }
    participant Many@{ "type" : "collections" }
    participant ESB@{ "type" : "queue" }
```
## Диаграмма 3 Ветвления и циклы

```mermaid
sequenceDiagram
    Alice->>Bob: Hello Bob, how are you?
    alt is sick
        Bob->>Alice: Not so good :(
    else is well
        Bob->>Alice: Feeling fresh like a daisy
    end
    opt Extra response
        Bob->>Alice: Thanks for asking
    end
```

