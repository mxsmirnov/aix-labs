# Flochart diagram
* markdown работает

## Диаграмма 1. Simple Left-Right Graph
* ориентация рисунка слева направо (по умолчанию свержу вниз)
* формы (начертания контуров) элементов можно задать скобками
* типы стрелок
* метки стрелок
* комментарии
```mermaid
%% Два знака процента - это комментарии
flowchart LR     
%% Nodes
    1([Start])
    2[Look for <br>lost item]
    3{{Did I find it?}}
    4([Stop])
%% Node links
    1 --> 2 --> 3 -->|Yes| 4
    3 -.->|No| 2
```
## Диаграмма 2. Subgraph (version 1)
Подграфы и связи между объектами из них
_Расположение элементов предсказать непросто_
```mermaid
flowchart 
    c1-->a2
    subgraph one
        a1-->a2
    end
    subgraph two
        b1-->b2
    end
    subgraph three
        c1-->c2
    end
```
## Диаграмма 2. Subgraph (version 2)
Поменяли местами подграфы two и three
```mermaid
flowchart 
    c1-->a2
    subgraph one
        a1-->a2
    end
    subgraph three
        c1-->c2
    end
    subgraph two
        b1-->b2
    end
```

## Диаграмма 2. Subgraph (version 3)
* Но лучше управлять расположением элементов, задавая направление стрелок
* Заодно переопредлили стиль подграфов B1, B2
```mermaid
flowchart LR
  subgraph TOP
    direction TB
    subgraph B1
        direction RL
        i1 -->f1
    end
    subgraph B2
        direction BT
        i2 -->f2
    end
  end
  A --> TOP --> B
  B1:::someclass --> B2:::someclass
  classDef someclass fill:#E2F0D9, stroke:#385723
```


## Диаграмма 2. Subgraph (version 4)
Направление (direction) для элементов за границами подграфов
```mermaid
flowchart LR
    subgraph subgraph1
        direction TB
        top1[top] --> bottom1[bottom]
    end
    subgraph subgraph2
        direction TB
        top2[top] --> bottom2[bottom]
    end
    %% ^ These subgraphs are identical, except for the links to them:

    %% Link *to* subgraph1: subgraph1 direction is maintained
    outside --> subgraph1
    %% Link *within* subgraph2:
    %% subgraph2 inherits the direction of the top-level graph (LR)
    outside ---> top2
```
## Диаграмма 3. Анимированные стрелки
Разной толщины и скорости анимации
```mermaid
flowchart LR
  A e1@==> B
  e1@{ animate: true }
  C e2@--> D
  e2@{ animation: slow}
```

## Node shapes
```mermaid
flowchart LR
    id1(This is the **text** in the box)
    id2([This is the *text* in the box])
    id3[[This is the text in the box]]
    id4[(Database)]
    id5((This is the text in the circle))
    id6>This is the text in the box]
    id7{This is the text in the box}
    id8{{This is the text in the box}}
    id9[/This is the text in the box/]
    id10[\This is the text in the box\]
    id11[/Christmas\]
    id12[\Go shopping/]
    id13(((This is the text in the circle)))
    id14@{ shape: manual-file, label: "File Handling"}
    id15@{ shape: manual-input, label: "User Input"}
    id16@{ shape: docs, label: "Multiple Documents"}
    id17@{ shape: procs, label: "Process Automation"}
    1d18@{ shape: paper-tape, label: "Paper Records"}
    id19@{ shape: notch-rect, label: "Card" }
    id20@{ img: "https://mermaid.js.org/favicon.svg", label: "My example image label", pos: "t", h: 60, constraint: "on" }
```