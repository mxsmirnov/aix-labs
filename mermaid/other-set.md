# Другие полезные Mermaid диаграммы

## Мой выбор: блочная диаграмма
```mermaid
block
  columns 3
  a["A label"] b:2 c:2 d
```
## Диаграмма с вложенными блоками
* можно использовать стрелки (см. от **g** -> **o**)
* и раскрашивать блоки (см **h**)
* элемент **p** пропушен (space)
```mermaid
block
  columns 3
  a:3
  block:group1:2
    columns 2
    h i j k
  end
  g
  block:group2:3
    %% columns auto (default)
    l m n o space q r
  end
  g --> o
  style h fill:#696
```
## Простая диаграмма Ганта
```mermaid
gantt
title Writing my thesis
dateFormat  DD-MM
axisFormat  %m-%d
section Research
    Procrastinate   :a1, 01-01, 59d
    Do it           :after a1  , 10d
section Write-up
    Should I start? :01-03 , 20d
    Ugh ok      : 6d
```
## Treemap (beta)
Подробнее посмотрите [Описание на сайте: mermaid.js.org](https://mermaid.js.org/syntax/treemap.html)
```mermaid
treemap-beta
"Annual Budget"
  "Operations"
    "Salaries": 700000
    "Equipment": 200000
    "Supplies": 100000
  "Marketing"
    "Advertising": 400000
    "Events": 100000
  "R&D"
    "Research": 300000
    "Development": 250000
```
## Круговая диаграмма
```mermaid
pie title Pets adopted by volunteers
    "Dogs" : 386
    "Cats" : 85
    "Rats" : 15
```
## Матрица 2х2
```mermaid
quadrantChart
    title Reach and engagement of campaigns
    x-axis Low Reach --> High Reach
    y-axis Low Engagement --> High Engagement
    quadrant-1 We should expand
    quadrant-2 Need to promote
    quadrant-3 Re-evaluate
    quadrant-4 May be improved
    Campaign A: [0.3, 0.6]
    Campaign B: [0.45, 0.23]
    Campaign C: [0.57, 0.69]
    Campaign D: [0.78, 0.34]
    Campaign E: [0.40, 0.34]
    Campaign F: [0.35, 0.78]

```
