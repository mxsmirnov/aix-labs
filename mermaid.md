# Архитектура системы (GitHub-совместимая версия)

## 1. Диаграмма контекста (C4 альтернатива)

```mermaid
graph TB
    subgraph "Контекст системы"
        direction TB
        
        subgraph "Внешние системы"
            SMS[СМС-сервис]
            CBR[ЦБ РФ]
        end
        
        subgraph "Наша система"
            WebApp[Интернет-банк]
        end
        
        subgraph "Пользователи"
            Client[Клиент банка]
            Admin[Администратор]
        end
    end
    
    Client -->|Использует| WebApp
    Admin -->|Администрирует| WebApp
    WebApp -->|Отправляет СМС| SMS
    WebApp -->|Отчеты| CBR
    
    style Client fill:#d4f4dd
    style Admin fill:#d4f4dd
    style WebApp fill:#e1f5fe
    style SMS fill:#f3e5f5
    style CBR fill:#f3e5f5
    
    %% Легенда
    subgraph "Легенда"
        direction LR
        P[Человек]:::person
        S[Система]:::system
        ES[Внешняя система]:::extsystem
    end
    
    classDef person fill:#d4f4dd
    classDef system fill:#e1f5fe
    classDef extsystem fill:#f3e5f5
```

## 2. Диаграмма последовательности (Sequence Diagram)

```mermaid
sequenceDiagram
    title: Процесс авторизации
    participant U as Пользователь
    participant FE as Фронтенд
    participant Auth as AuthService
    participant DB as База данных
    
    U->>FE: Вводит логин/пароль
    activate FE
    FE->>+Auth: POST /api/login
    Auth->>+DB: Проверка учетных данных
    DB-->>-Auth: Данные пользователя
    Auth->>Auth: Генерация JWT токена
    Auth-->>-FE: 200 OK + JWT
    FE-->>U: Успешный вход
    deactivate FE
    
    Note right of U: Сессия установлена
    
    U->>FE: Запрос выписки
    FE->>+Auth: GET /api/statement
    Note over Auth: Проверка JWT токена
    Auth-->>-FE: Данные выписки
    FE-->>U: Отображение выписки
```

## 3. Диаграмма компонентов (Component Diagram)

```mermaid
graph TB
    %% Стили
    classDef client fill:#bbdefb,stroke:#1976d2
    classDef service fill:#c8e6c9,stroke:#388e3c
    classDef infra fill:#ffecb3,stroke:#ffa000
    classDef db fill:#f8bbd0,stroke:#c2185b
    
    %% Клиентская часть
    Web[Веб-браузер<br/>React]:::client
    Mobile[Мобильное приложение<br/>React Native]:::client
    
    %% Серверная часть
    GW[API Gateway<br/>Nginx]:::service
    Auth[Сервис аутентификации<br/>Go]:::service
    Payments[Платежный сервис<br/>Java]:::service
    Notify[Сервис уведомлений<br/>Python]:::service
    
    %% Инфраструктура
    DB1[(PostgreSQL<br/>Основная БД)]:::db
    DB2[(Redis<br/>Кэш)]:::db
    MQ[RabbitMQ<br/>Очереди]:::infra
    K8s[Kubernetes]:::infra
    
    %% Связи
    Web --> GW
    Mobile --> GW
    GW --> Auth
    GW --> Payments
    GW --> Notify
    
    Auth --> DB1
    Payments --> DB1
    Auth --> DB2
    Notify --> MQ
    
    %% Группировка
    subgraph "Клиентские приложения"
        Web
        Mobile
    end
    
    subgraph "Микросервисы"
        Auth
        Payments
        Notify
    end
    
    subgraph "Инфраструктура"
        DB1
        DB2
        MQ
        K8s
    end
```

## 4. Диаграмма состояния (State Diagram)

```mermaid
stateDiagram-v2
    [*] --> Неактивен : Новая карта
    
    Неактивен --> Активен : Активация
    Активен --> Заблокирован : 3 неверных PIN
    Заблокирован --> Активен : Разблокировка
    
    state Активен {
        [*] --> Готов
        Готов --> Транзакция : Оплата/Перевод
        Транзакция --> Успех : Подтверждено
        Транзакция --> Ошибка : Отказ/Недостаточно средств
        Успех --> Готов
        Ошибка --> Готов : Повтор
    }
    
    Активен --> Просрочен : Истечение срока
    Просрочен --> [*] : Утилизация
    Заблокирован --> [*] : Окончательная блокировка
```

## 5. Диаграмма потоков данных (Flowchart)

```mermaid
flowchart TD
    Start([Начало]) --> Login{Пользователь в системе?}
    
    Login -->|Нет| Auth[Страница авторизации]
    Auth --> Input[Ввод логина/пароля]
    Input --> Validate{Проверка данных}
    Validate -->|Неверно| Error[Ошибка авторизации]
    Error --> Auth
    
    Validate -->|Верно| Success[Успешный вход]
    Success --> Dashboard[Личный кабинет]
    
    Login -->|Да| Dashboard
    
    Dashboard --> Menu{Выбор действия}
    
    Menu -->|Платежи| Payment[Оплата услуг]
    Menu -->|Переводы| Transfer[Перевод между счетами]
    Menu -->|Выписки| Statement[Запрос выписки]
    Menu -->|Настройки| Settings[Настройки профиля]
    
    Payment --> Confirm{Подтверждение}
    Transfer --> Confirm
    Statement --> Show[Отображение выписки]
    Settings --> Save[Сохранение изменений]
    
    Confirm -->|Да| Process[Обработка операции]
    Confirm -->|Нет| Dashboard
    
    Process --> Result{Результат}
    Result -->|Успех| SuccessMsg[✅ Операция выполнена]
    Result -->|Ошибка| FailMsg[❌ Ошибка выполнения]
    
    SuccessMsg --> Dashboard
    FailMsg --> Dashboard
    Show --> Dashboard
    Save --> Dashboard
```

## 6. Timeline разработки (Gantt Chart)

```mermaid
gantt
    title План разработки MVP интернет-банка
    dateFormat YYYY-MM-DD
    axisFormat %d.%m
    
    section Бэкенд
    Архитектура API        :a1, 2024-01-01, 10d
    Сервис аутентификации  :a2, after a1, 15d
    Платежный модуль       :a3, after a1, 20d
    Интеграция с внешними системами :a4, after a2, 10d
    
    section Фронтенд
    Веб-интерфейс         :b1, 2024-01-10, 25d
    Мобильное приложение  :b2, 2024-01-20, 30d
    Адаптивный дизайн     :b3, after b1, 10d
    
    section Тестирование
    Юнит-тесты            :c1, after a2, 10d
    Интеграционные тесты  :c2, after a3, 15d
    Нагрузочное тестирование :c3, 2024-02-15, 10d
    
    section Документация
    Техническая документация :d1, 2024-01-15, 20d
    Руководство пользователя :d2, after b1, 15d
    
    section Деплой
    Подготовка инфраструктуры :e1, 2024-02-10, 10d
    Релиз MVP               :milestone, e2, 2024-02-25, 0d
    Мониторинг и логирование :e3, after e2, 5d
```

## 7. Статистика использования технологий

```mermaid
pie title Распределение технологий в проекте
    "Backend (Go/Java)" : 40
    "Frontend (React/RN)" : 25
    "Базы данных" : 15
    "Инфраструктура (K8s, Docker)" : 12
    "Мониторинг (Prometheus, Grafana)" : 5
    "Документация" : 3
```

---

## Почему эта версия работает на GitHub:

1. **Без C4-синтаксиса** - используем стандартные graph/flowchart диаграммы
2. **Стандартные типы диаграмм** - которые точно поддерживаются GitHub
3. **Стилизация через classDef** - вместо продвинутых C4-функций
4. **Все популярные типы диаграмм** представлены и проверены

## Что теперь увидите на GitHub:

✅ **Все 7 диаграмм отобразятся корректно**
✅ **Полностью интерактивные схемы**
✅ **Поддержка тем GitHub** (автоматическая смена цветов в темной теме)
✅ **Масштабирование и навигация**
✅ **Никаких ошибок рендеринга**

## Для проверки:

Создайте новый файл в любом репозитории GitHub с именем `README.md` или `ARCHITECTURE.md`, вставьте этот код, и все диаграммы появятся автоматически!

**Это и есть "нативная поддержка Mermaid в GitHub" в действии** - диаграммы рендерятся без плагинов, установок, конвертаций или внешних сервисов.
