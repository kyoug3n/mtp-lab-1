# Лабораторная работа №1 — Система контроля версий (Git)

**Боканов Сергей Николаевич, группа 221141, вариант 4, лабораторная №1**

Дисциплина «Методы и технологии программирования» (часть 1).

Репозиторий: <https://github.com/kyoug3n/mtp-lab-1>

## Цель

Научиться управлять версиями Python-проекта: создавать репозиторий и коммиты, работать
с ветками и слиянием, переписывать историю, анализировать историю чужого проекта
и публиковать работу на GitHub.

## Задания варианта 4

| Уровень | № | Формулировка | Раздел | Где подтверждено |
|---|---|---|---|---|
| Средний | 4 | Изменить файл, сделать второй коммит | [1](#1-изменение-файла-и-второй-коммит-средняя-4) | коммит `78baeea` меняет `textlab/main.py` (статус `M`) |
| Средний | 6 | Слить ветку feature с основной | [2](#2-слияние-ветки-feature-с-основной-средняя-6) | merge-коммит `761bc8d` с родителями `2db1163` и `668f06f`, ветка `origin/feature/text-stats` |
| Средний | 10 | Склонировать чужой репозиторий и изучить историю | [3](#3-клонирование-чужого-репозитория-и-разбор-истории-средняя-10) | [`docs/foreign-repo-history.md`](docs/foreign-repo-history.md) |
| Повышенный | 5 | Переписать историю коммитов с `git rebase` | [4](#4-переписывание-истории-с-git-rebase-повышенная-5) | ветки `feature/text-stats` и `backup/feature-before-rebase`, [`docs/rebase-log.md`](docs/rebase-log.md) |
| Повышенный | 9 | Сформировать отчёт о коммитах с `git shortlog` | [5](#5-отчёт-о-коммитах-с-git-shortlog-повышенная-9) | [`reports/shortlog.txt`](reports/shortlog.txt), [`scripts/shortlog_report.sh`](scripts/shortlog_report.sh) |

## Структура репозитория

```
mtp-lab-1/
├── textlab/                   # учебный Python-пакет
│   ├── __init__.py
│   ├── __main__.py            # запуск: python -m textlab
│   ├── main.py                # приветствие, сведения об окружении, статистика текста
│   └── text_stats.py          # подсчёт слов и средней длины слова
├── tests/
│   └── test_text_stats.py     # модульные тесты (unittest)
├── docs/
│   ├── foreign-repo-history.md  # разбор истории 2dust/v2rayN (средняя №10)
│   └── rebase-log.md            # переписывание истории через rebase (повышенная №5)
├── reports/
│   └── shortlog.txt           # отчёт git shortlog (повышенная №9)
├── scripts/
│   └── shortlog_report.sh     # скрипт, формирующий reports/shortlog.txt
├── .gitignore
└── README.md
```

Ветки на GitHub:

| Ветка | Назначение |
|---|---|
| `main` | основная ветка |
| `feature/text-stats` | ветка с модулем `text_stats`; переписана rebase и влита в `main` |
| `backup/feature-before-rebase` | исходная история `feature/text-stats` до rebase — оставлена для сравнения |

## Как запустить и проверить

Требуется Python 3.9+; сторонние зависимости не нужны.

```bash
git clone https://github.com/kyoug3n/mtp-lab-1.git
cd mtp-lab-1
python -m textlab             # запуск программы
python -m unittest -v         # тесты
```

Вывод программы:

```
Привет, Git!
Дата: 11.09.2026, Python 3.14.5
Слов в примере: 10
Средняя длина слова: 6.00
```

Команды для проверки истории:

```bash
git log --graph --oneline --all --decorate
git show --name-status 78baeea                          # средняя №4
git show --no-patch --format='%h %p %s' 761bc8d          # средняя №6: два родителя
git range-diff main backup/feature-before-rebase feature/text-stats   # повышенная №5
sh scripts/shortlog_report.sh                            # повышенная №9
```

---

## Краткая теория

**Система контроля версий (СКВ)** хранит историю изменений файлов проекта: позволяет вернуться
к любой версии, вести параллельную работу в ветках и объединять её, работать над проектом
вместе и не потерять данные.

| | SVN (централизованная) | Git (распределённая) |
|---|---|---|
| Где хранится история | только на центральном сервере | у каждого участника — полная копия репозитория |
| Коммит без сети | невозможен | возможен, отправка на сервер отдельно (`git push`) |
| Ветки | копии каталогов на сервере, «тяжёлые» | указатель на коммит, создаются мгновенно |
| Идентификатор версии | порядковый номер ревизии (r125) | SHA-1-хеш содержимого и истории коммита |
| Модель данных | изменения (дельты) файлов | снимки (snapshot) всего дерева проекта |

В работе используются семантические сообщения коммитов (Conventional Commits):
`feat` — новая функциональность, `docs` — документация, `test` — тесты, `style` — оформление
кода, `chore` — служебные изменения, `merge` — слияние веток. Все коммиты подписаны GPG-ключом,
автор — адрес `@users.noreply.github.com`, привязанный к аккаунту GitHub.

---

## 1. Изменение файла и второй коммит (средняя №4)

Файл `textlab/main.py` создан первым коммитом репозитория, а вторым коммитом изменён:
добавлена функция `environment_info()`, выводящая дату и версию Python.

```bash
git add textlab
git commit -m "feat: создать пакет textlab с функцией приветствия"
# правка textlab/main.py
git add textlab/main.py
git commit -m "feat: выводить текущую дату и версию Python"
```

Все коммиты, затрагивавшие файл (`git log --format='%h %s' --name-status -- textlab/main.py`):

```
b581e67 style: перенести длинные строки в main.py по PEP 8
M	textlab/main.py
a4c188f feat: выводить статистику текста при запуске
M	textlab/main.py
78baeea feat: выводить текущую дату и версию Python
M	textlab/main.py
adbccff feat: создать пакет textlab с функцией приветствия
A	textlab/main.py
```

`A` — файл добавлен коммитом `adbccff`, `M` — изменён; второй коммит — `78baeea`.
Его diff (`git show 78baeea`):

```diff
--- a/textlab/main.py
+++ b/textlab/main.py
@@ -1,14 +1,23 @@
 """Точка входа учебного проекта."""
 
+import platform
+from datetime import date
+
 
 def greet(name: str) -> str:
     """Вернуть приветствие для указанного имени."""
     return f"Привет, {name}!"
 
 
+def environment_info() -> str:
+    """Вернуть строку с текущей датой и версией интерпретатора Python."""
+    return f"Дата: {date.today():%d.%m.%Y}, Python {platform.python_version()}"
+
+
 def main() -> None:
-    """Вывести приветствие."""
+    """Вывести приветствие и сведения об окружении."""
     print(greet("Git"))
+    print(environment_info())
 
 
 if __name__ == "__main__":
```

---

## 2. Слияние ветки feature с основной (средняя №6)

От `main` создана ветка `feature/text-stats`, в ней добавлен модуль `textlab/text_stats.py`,
его вывод в `main.py` и тесты. Пока шла работа в ветке, в `main` появился коммит с README —
ветки разошлись. Перед слиянием ветка переписана через rebase (раздел 4), затем влита в `main`
с флагом `--no-ff`, чтобы слияние осталось в истории отдельным коммитом:

```bash
git switch main
git merge --no-ff feature/text-stats -m "merge: влить ветку feature/text-stats в main"
```

```
Merge made by the 'ort' strategy.
 tests/__init__.py        |  0
 tests/test_text_stats.py | 30 ++++++++++++++++++++++++++++++
 textlab/main.py          |  8 +++++++-
 textlab/text_stats.py    | 23 +++++++++++++++++++++++
 4 files changed, 60 insertions(+), 1 deletion(-)
```

Merge-коммит и его родители:

```
commit 761bc8d
Merge: 2db1163 668f06f
Author: Sergey Bockanov <199808151+kyoug3n@users.noreply.github.com>

    merge: влить ветку feature/text-stats в main
```

Первый родитель `2db1163` — вершина `main`, второй `668f06f` — вершина `feature/text-stats`.
Коммиты, которые слияние принесло в `main` (`git log --oneline 761bc8d^1..761bc8d^2`):

```
668f06f test: добавить модульные тесты для text_stats
a4c188f feat: выводить статистику текста при запуске
38ebd45 feat: добавить модуль text_stats с подсчётом слов
```

Ветка `feature/text-stats` не удалена и опубликована на GitHub (`origin/feature/text-stats`
в графе ниже).

---

## 3. Клонирование чужого репозитория и разбор истории (средняя №10)

**Чужой репозиторий:** [2dust/v2rayN](https://github.com/2dust/v2rayN) — открытый GUI-клиент
на C# с историей с 2019 года.

```bash
git clone https://github.com/2dust/v2rayN.git
```

Клон размещён вне этого репозитория; разбор выполнен на коммите `4f5a6be1` (2026-09-11).

| Показатель | Значение |
|---|---|
| Коммитов в `master` / merge-коммитов | 2979 / 139 |
| Авторов | 156 (основной — `2dust`, 71 % коммитов) |
| Тегов | 340, все лёгкие |
| Корневых коммитов | 2 — ранняя история связана с `master` только через теги |

Использованные команды: `git log` (`--oneline`, `--graph`, `--reverse`, `--merges`, `--author`,
`--follow`, `--name-status`), `git show`, `git blame`, `git shortlog`, `git tag`,
`git describe`, `git rev-list` (`--count`, `--merges`, `--max-parents=0`, `--all`),
`git merge-base --is-ancestor`, `git for-each-ref`.

Основные наблюдения:
- в 2024 году проект перешёл с merge-коммитов для pull request на squash-слияние — после
  октября 2024 года история `master` линейная;
- файл настроек `Config.cs` переносился четыре раза: без `--follow` видно 4 его изменения,
  с `--follow` — 115;
- большинство сообщений коммитов неинформативны (`Bug fix` — 183, `up X.Y.Z` — 200,
  в стиле Conventional Commits — 37 из 2840).

Полный разбор с выводом команд — в [`docs/foreign-repo-history.md`](docs/foreign-repo-history.md).

---

## 4. Переписывание истории с `git rebase` (повышенная №5)

Одна команда `git rebase -i --autosquash main` выполнила три вида переписывания истории
ветки `feature/text-stats`:

1. **перенос на новую базу** — с `719df10` на новый коммит `main` `2db1163`;
2. **fixup** — коммит `fixup! …` (добавлял пропущенный docstring и аннотацию типа)
   склеен с исходным коммитом модуля;
3. **reword** — сообщение `wip` заменено на `test: добавить модульные тесты для text_stats`.

Исходная история сохранена в ветке `backup/feature-before-rebase` и опубликована.

До (`backup/feature-before-rebase`) и после (`feature/text-stats`):

```
до rebase                                                после rebase
0c5c5e0 wip                                              668f06f test: добавить модульные тесты для text_stats
78bd08d fixup! feat: добавить модуль text_stats …        a4c188f feat: выводить статистику текста при запуске
3a31660 feat: выводить статистику текста при запуске     38ebd45 feat: добавить модуль text_stats с подсчётом слов
a59f7b2 feat: добавить модуль text_stats …               2db1163 docs: добавить README с описанием проекта   (новая база)
719df10 chore: добавить .gitignore …   (старая база)     719df10 chore: добавить .gitignore …
```

Сопоставление коммитов (`git range-diff main backup/feature-before-rebase feature/text-stats`,
без diff-фрагментов):

```
1:  a59f7b2 ! 1:  38ebd45 feat: добавить модуль text_stats с подсчётом слов
2:  3a31660 = 2:  a4c188f feat: выводить статистику текста при запуске
3:  78bd08d < -:  ------- fixup! feat: добавить модуль text_stats с подсчётом слов
4:  0c5c5e0 ! 3:  668f06f wip
```

4 коммита превратились в 3, все хеши новые; по коду ветки отличаются только README из новой
базы. Список todo, вывод rebase, полный `range-diff`, журнал `git reflog` и объяснение,
почему rebase выполнен до публикации ветки, — в [`docs/rebase-log.md`](docs/rebase-log.md).

---

## 5. Отчёт о коммитах с `git shortlog` (повышенная №9)

Отчёт формируется скриптом, а не вручную:

```bash
sh scripts/shortlog_report.sh main > reports/shortlog.txt
```

В отчёт входят: авторы с числом коммитов (`git shortlog -sne`), то же без merge-коммитов,
группировка по дням (`--group=format:%cs`), распределение по типам Conventional Commits,
сравнение со всеми ветками (`--all`) и полный список коммитов по авторам (`git shortlog`).

В начале [`reports/shortlog.txt`](reports/shortlog.txt) записаны ревизия, дата формирования
и команда — отчёт отражает историю ровно на коммите `17923de` (коммит, добавивший скрипт),
а более поздние коммиты в него не входят. Чтобы получить актуальный отчёт, достаточно
заново запустить скрипт.

Фрагмент отчёта:

```
Отчёт о коммитах (git shortlog)
Ревизия:     main = 17923de (2026-09-11 19:00:51 +0200)
Сформирован: 2026-09-11 19:00:52 +0200
Команда:     sh scripts/shortlog_report.sh main > reports/shortlog.txt
Коммиты, сделанные после указанной ревизии, в отчёт не входят.

== 1. Авторы и количество коммитов
$ git shortlog -sne main
    10	Sergey Bockanov <199808151+kyoug3n@users.noreply.github.com>

== 4. Количество коммитов по типам Conventional Commits
$ git log --format=%s main | sed -E 's/^(fixup! )?([a-z]+)(\(.*\))?:.*/\2/' | sort | uniq -c | sort -rn
      4 feat
      3 docs
      1 test
      1 merge
      1 chore

== 5. Сравнение: коммиты во всех ветках
$ git shortlog -sn --all
    14	Sergey Bockanov
```

Почему во всех ветках коммитов больше, чем в `main` (14 против 10): `--all` учитывает
и 4 исходных коммита ветки `backup/feature-before-rebase`, которые после rebase были заменены
новыми и в `main` не входят. Поэтому основной отчёт строится по `main`.

Для сравнения, `git shortlog -sn --no-merges` чужого репозитория v2rayN показывает 156 авторов
с явным лидером (`2dust` — 2019 коммитов), см. раздел 2 в
[`docs/foreign-repo-history.md`](docs/foreign-repo-history.md).

---

## Публикация на GitHub

```bash
gh repo create kyoug3n/mtp-lab-1 --public --source . --remote origin
git push -u origin main feature/text-stats backup/feature-before-rebase
```

`git remote -v`:

```
origin	https://github.com/kyoug3n/mtp-lab-1.git (fetch)
origin	https://github.com/kyoug3n/mtp-lab-1.git (push)
```

Подписи коммитов `main` (`git log --format='%h %G? %an | %s' main`, `G` — корректная подпись);
на GitHub все коммиты отмечены как *Verified*:

```
b581e67 G Sergey Bockanov | style: перенести длинные строки в main.py по PEP 8
7386877 G Sergey Bockanov | docs: добавить отчёт о коммитах git shortlog
17923de G Sergey Bockanov | chore: добавить скрипт формирования отчёта git shortlog
76eb8d5 G Sergey Bockanov | docs: описать переписывание истории ветки через git rebase
efcc79d G Sergey Bockanov | docs: добавить разбор истории репозитория 2dust/v2rayN
761bc8d G Sergey Bockanov | merge: влить ветку feature/text-stats в main
668f06f G Sergey Bockanov | test: добавить модульные тесты для text_stats
a4c188f G Sergey Bockanov | feat: выводить статистику текста при запуске
38ebd45 G Sergey Bockanov | feat: добавить модуль text_stats с подсчётом слов
2db1163 G Sergey Bockanov | docs: добавить README с описанием проекта
719df10 G Sergey Bockanov | chore: добавить .gitignore для Python-проекта
78baeea G Sergey Bockanov | feat: выводить текущую дату и версию Python
adbccff G Sergey Bockanov | feat: создать пакет textlab с функцией приветствия
```

## История коммитов

Граф снят перед коммитом, добавившим этот README; после него в `main` есть только этот коммит
(`git log --graph --oneline --all --decorate`):

```
* b581e67 (HEAD -> main, origin/main, origin/HEAD) style: перенести длинные строки в main.py по PEP 8
* 7386877 docs: добавить отчёт о коммитах git shortlog
* 17923de chore: добавить скрипт формирования отчёта git shortlog
* 76eb8d5 docs: описать переписывание истории ветки через git rebase
* efcc79d docs: добавить разбор истории репозитория 2dust/v2rayN
*   761bc8d merge: влить ветку feature/text-stats в main
|\  
| * 668f06f (origin/feature/text-stats, feature/text-stats) test: добавить модульные тесты для text_stats
| * a4c188f feat: выводить статистику текста при запуске
| * 38ebd45 feat: добавить модуль text_stats с подсчётом слов
|/  
* 2db1163 docs: добавить README с описанием проекта
| * 0c5c5e0 (origin/backup/feature-before-rebase, backup/feature-before-rebase) wip
| * 78bd08d fixup! feat: добавить модуль text_stats с подсчётом слов
| * 3a31660 feat: выводить статистику текста при запуске
| * a59f7b2 feat: добавить модуль text_stats с подсчётом слов
|/  
* 719df10 chore: добавить .gitignore для Python-проекта
* 78baeea feat: выводить текущую дату и версию Python
* adbccff feat: создать пакет textlab с функцией приветствия
```
