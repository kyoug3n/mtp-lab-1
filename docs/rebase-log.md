# Переписывание истории коммитов с `git rebase` (повышенная №5)

## Сценарий

История ветки `feature/text-stats` подготовлена так, чтобы на ней можно было показать три вида
переписывания истории одной командой `git rebase -i`:

1. **Перенос ветки на новую базу.** Пока в ветке шла работа, в `main` появился коммит
   `2db1163 docs: добавить README с описанием проекта`, и ветка отстала от `main`.
2. **Склейка исправления с исходным коммитом (fixup).** В коммите `a59f7b2`, добавившем модуль
   `text_stats`, у функции `words()` не хватало docstring и аннотации возвращаемого типа.
   Недочёт исправлен отдельным коммитом `78bd08d`, созданным командой
   `git commit --fixup=a59f7b2` — такой коммит получает сообщение `fixup! <исходное сообщение>`
   и при `--autosquash` сам встаёт в список сразу после исходного коммита.
3. **Переименование коммита (reword).** Тесты закоммичены с неинформативным сообщением `wip`.

Исправление в fixup-коммите намеренно безобидное (документация и аннотация типа, поведение
кода не меняется): сценарий нужен для демонстрации rebase.

Чтобы исходную историю можно было сравнить с результатом, перед rebase от ветки создана
резервная ветка **`backup/feature-before-rebase`**; она отправлена на GitHub вместе с остальными.

Команды ниже приведены так, как выполнялись в локальном репозитории. В свежем клоне к именам
веток `feature/text-stats` и `backup/feature-before-rebase` нужно добавить префикс `origin/`.

## История до rebase

`git log --graph --format='%h %s' 719df10^..backup/feature-before-rebase`:

```
* 0c5c5e0 wip
* 78bd08d fixup! feat: добавить модуль text_stats с подсчётом слов
* 3a31660 feat: выводить статистику текста при запуске
* a59f7b2 feat: добавить модуль text_stats с подсчётом слов
* 719df10 chore: добавить .gitignore для Python-проекта
```

База ветки — `719df10` (`git merge-base main backup/feature-before-rebase`).

Содержимое fixup-коммита (`git show 78bd08d`):

```diff
--- a/textlab/text_stats.py
+++ b/textlab/text_stats.py
@@ -5,7 +5,8 @@ import re
 WORD_PATTERN = re.compile(r"[a-zа-яё0-9]+", re.IGNORECASE)
 
 
-def words(text: str):
+def words(text: str) -> list[str]:
+    """Разбить текст на слова в нижнем регистре."""
     return WORD_PATTERN.findall(text.lower())
```

## Выполненные команды

```bash
git branch backup/feature-before-rebase feature/text-stats   # сохранить исходную историю
git switch feature/text-stats
git rebase -i --autosquash main
```

Список действий (todo), который Git сформировал с учётом `--autosquash` — fixup-коммит уже
перенесён под свой исходный коммит и помечен `fixup`:

```
pick a59f7b2 # feat: добавить модуль text_stats с подсчётом слов
fixup 78bd08d # fixup! feat: добавить модуль text_stats с подсчётом слов
pick 3a31660 # feat: выводить статистику текста при запуске
pick 0c5c5e0 # wip
```

В списке изменена одна строка — `pick` → `reword` для коммита `wip`:

```
pick a59f7b2 # feat: добавить модуль text_stats с подсчётом слов
fixup 78bd08d # fixup! feat: добавить модуль text_stats с подсчётом слов
pick 3a31660 # feat: выводить статистику текста при запуске
reword 0c5c5e0 # wip
```

При остановке на `reword` сообщение `wip` заменено на
`test: добавить модульные тесты для text_stats`.

Редактирование списка и сообщения было выполнено неинтерактивно — через переменные
`GIT_SEQUENCE_EDITOR` (правит todo-файл, заменяя `pick` на `reword` у коммита `0c5c5e0`)
и `GIT_EDITOR` (записывает новое сообщение коммита):

`seq-editor.sh` (получает путь к todo-файлу в `$1`):

```sh
#!/bin/sh
cp "$1" todo-before.txt                                  # сохранить исходный список для отчёта
sed -i 's/^pick \(0c5c5e0[0-9a-f]*\)/reword \1/' "$1"   # pick -> reword для коммита wip
cp "$1" todo-after.txt
```

`msg-editor.sh` (получает путь к файлу сообщения коммита в `$1`):

```sh
#!/bin/sh
printf 'test: добавить модульные тесты для text_stats\n' > "$1"
```

```bash
GIT_SEQUENCE_EDITOR=./seq-editor.sh GIT_EDITOR=./msg-editor.sh git rebase -i --autosquash main
```

(Скрипты лежали во временной папке вне репозитория, пути к ней в листингах сокращены; оба списка todo выше — содержимое
`todo-before.txt` и `todo-after.txt` без строк-комментариев.)

Результат тот же, что при ручной правке списка и сообщения в текстовом редакторе.

Вывод rebase:

```
Rebasing (1/4)Rebasing (2/4)Rebasing (3/4)Rebasing (4/4)[detached HEAD 668f06f] test: добавить модульные тесты для text_stats
 Date: Fri Sep 11 18:51:47 2026 +0200
 2 files changed, 30 insertions(+)
 create mode 100644 tests/__init__.py
 create mode 100644 tests/test_text_stats.py
Successfully rebased and updated refs/heads/feature/text-stats.
```

## История после rebase

`git log --graph --format='%h %s' 719df10^..feature/text-stats`:

```
* 668f06f test: добавить модульные тесты для text_stats
* a4c188f feat: выводить статистику текста при запуске
* 38ebd45 feat: добавить модуль text_stats с подсчётом слов
* 2db1163 docs: добавить README с описанием проекта
* 719df10 chore: добавить .gitignore для Python-проекта
```

- База ветки сменилась с `719df10` на `2db1163` — ветка снова начинается от вершины `main`.
- Было 4 коммита, стало 3: `fixup!` растворился в коммите модуля.
- `wip` получил осмысленное сообщение в стиле Conventional Commits.
- **У всех трёх коммитов новые хеши**, даже у `feat: выводить статистику…`, содержимое которого
  не изменилось: хеш зависит от родителя, а родитель стал другим. Коммиты заново подписаны GPG.

## Сопоставление старых и новых коммитов

`git range-diff 719df10..backup/feature-before-rebase 2db1163..feature/text-stats`
(в свежем клоне — с префиксом `origin/` у имён веток):

```
1:  a59f7b2 ! 1:  38ebd45 feat: добавить модуль text_stats с подсчётом слов
    @@ textlab/text_stats.py (new)
     +WORD_PATTERN = re.compile(r"[a-zа-яё0-9]+", re.IGNORECASE)
     +
     +
    -+def words(text: str):
    ++def words(text: str) -> list[str]:
    ++    """Разбить текст на слова в нижнем регистре."""
     +    return WORD_PATTERN.findall(text.lower())
     +
     +
2:  3a31660 = 2:  a4c188f feat: выводить статистику текста при запуске
3:  78bd08d < -:  ------- fixup! feat: добавить модуль text_stats с подсчётом слов
4:  0c5c5e0 ! 3:  668f06f wip
    @@ Metadata
     Author: Sergey Bockanov <199808151+kyoug3n@users.noreply.github.com>
     
      ## Commit message ##
    -    wip
    +    test: добавить модульные тесты для text_stats
     
      ## tests/__init__.py (new) ##
     
```

Каждый диапазон отсчитывается от своей базы: старая версия ветки — от `719df10`, новая — от
`2db1163`. Сразу после rebase то же сравнение давала короткая форма
`git range-diff main backup/feature-before-rebase feature/text-stats`, но после слияния
новые коммиты уже входят в `main`, и короткая форма перестаёт работать — поэтому здесь
диапазоны указаны явно.

Как читать: `!` — коммит изменён (в первый вошла правка из fixup, у последнего новое сообщение),
`=` — содержимое совпадает, `<` — коммит есть только в старой версии (fixup склеен).

Итоговые файлы веток отличаются только README, пришедшим из новой базы
(`git diff --stat backup/feature-before-rebase feature/text-stats`):

```
 README.md | 9 +++++++++
 1 file changed, 9 insertions(+)
```

Код и тесты после переписывания истории остались теми же.

## Журнал `git reflog`

Записи операции rebase и последующего слияния (`git reflog`, снято сразу после слияния):

```
761bc8d HEAD@{0}: merge feature/text-stats: Merge made by the 'ort' strategy.
2db1163 HEAD@{1}: checkout: moving from feature/text-stats to main
668f06f HEAD@{2}: rebase (finish): returning to refs/heads/feature/text-stats
668f06f HEAD@{3}: rebase (reword): test: добавить модульные тесты для text_stats
72da66b HEAD@{4}: rebase (reword): wip
a4c188f HEAD@{5}: rebase (pick): feat: выводить статистику текста при запуске
38ebd45 HEAD@{6}: rebase (fixup): feat: добавить модуль text_stats с подсчётом слов
70c20e8 HEAD@{7}: rebase (pick): feat: добавить модуль text_stats с подсчётом слов
2db1163 HEAD@{8}: rebase (start): checkout main
0c5c5e0 HEAD@{9}: checkout: moving from main to feature/text-stats
```

Видно, как Git выполнял todo по шагам: скопировал коммит модуля (`70c20e8`), дописал в него
fixup (`38ebd45`), скопировал второй коммит (`a4c188f`), скопировал `wip` (`72da66b`)
и сменил его сообщение (`668f06f`). Промежуточные `70c20e8` и `72da66b` ни на одну ветку
не попали. Reflog хранится только локально, поэтому на GitHub исходная история доступна
через ветку `backup/feature-before-rebase`.

## Почему rebase выполнен до публикации ветки

Rebase создаёт новые коммиты вместо старых. Если бы `feature/text-stats` уже была на GitHub,
обновить её пришлось бы через `git push --force-with-lease`, а у других участников, успевших
забрать ветку, история разошлась бы с удалённой. Поэтому ветка переписана локально, до
первого `git push`, и уже потом влита в `main` (задание средней сложности №6).
