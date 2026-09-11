# Разбор истории чужого репозитория (средняя №10)

**Репозиторий:** [2dust/v2rayN](https://github.com/2dust/v2rayN) — GUI-клиент для Xray и sing-box
(C#, лицензия GPL-3.0, основной автор — `2dust`).

```bash
git clone https://github.com/2dust/v2rayN.git
```

- Дата клонирования: **2026-09-11**.
- Состояние на момент разбора: `master` = `4f5a6be12da72ebce3babe2dacf7549aff5daddf`
  (`git describe --tags` → `7.25.1-2-g4f5a6be1`).
- Клон размещён **вне** репозитория лабораторной работы, чтобы чужая история не смешалась
  с историей `mtp-lab-1`; в этот репозиторий попадают только результаты разбора.

Все выводы ниже получены на указанном коммите — при повторном клонировании новые коммиты
изменят числа, но команды остаются теми же.

---

## 1. Общие сведения

| Показатель | Команда | Значение |
|---|---|---|
| Коммитов в `master` | `git rev-list --count HEAD` | 2979 |
| Из них merge-коммитов | `git rev-list --merges --count HEAD` | 139 |
| Коммитов во всех ссылках | `git rev-list --count --all` | 3053 |
| Тегов | `git tag \| wc -l` | 340 |
| Авторов в `master` | `git shortlog -sn HEAD \| wc -l` | 156 |
| Удалённые ветки | `git branch -r` | `master`, `7.24.4`, `v7.23` |
| Сабмодули | `cat .gitmodules` | `v2rayN/GlobalHotKeys` → `2dust/GlobalHotKeys` |

Первые коммиты `master` (`git log --reverse --format='%h %ad %an | %s' --date=short | head -3`):

```
8bbb50ce 2019-10-11 2dust | mge
0091a587 2019-10-12 2dust | Update OptionSettingForm.resx
fe0bd593 2019-10-12 2dust | Update OptionSettingForm.cs
```

Последние 10 коммитов (`git log --oneline -10`):

```
4f5a6be1 Update build-windows-x86.yml
7674d7e4 Delete redundant fields (#10144)
77c462ec up 7.25.1
526cd683 Show language names in theme settings
7be23d7e Add Azerbaijani (az) UI localization (#10141)
d952c180 Update ResUI.zh-Hant.resx (#10139)
80fa6575 Bug fix
f05e44d7 优化策略组选择 (#10136)
b10c16a9 Add custom HTTP headers for subscription updates (#10118)
143ada13 Remove vnext (#10132)
```

---

## 2. Авторы

`git shortlog -sn --no-merges HEAD | head -10`:

```
  2019	2dust
   242	DHR60
   130	YFdyh000
    57	JieXu
    30	dependabot[bot]
    25	Miheichev Aleksandr Sergeevich
    15	ShiinaRinne
    12	Lemonawa
    11	crazypeace
    11	小仙女
```

- `2dust` написал около 71 % коммитов (2019 из 2840 без учёта слияний) — проект фактически
  ведёт один мейнтейнер, остальные 155 авторов присылают точечные правки.
- Среди авторов есть бот `dependabot[bot]` (30 коммитов, `git log --author=dependabot`) —
  он автоматически обновляет зависимости через pull request.
- Файла `.mailmap` в репозитории нет, поэтому `shortlog` группирует авторов «как записано»
  в коммитах, без склейки разных написаний одного человека.

---

## 3. Ветвление и слияния: смена способа приёма pull request

Фрагмент графа вокруг слияния PR №5026 (`git log --graph --oneline -n 14 855fd4f0`):

```
*   855fd4f0 Merge pull request #5026 from GibMeMyPacket/feat/singbox/exp_cachefile
|\  
| * 80783992 Add `Enable cache file for sing-box`
* | 870955fe Bug fix
|/  
* e0cea929 Up 6.43
* 315f4c35 Code clean
* d961ea22 Built-in routing rule set upgraded to V2
* 5c0c07c7 Migrate geosite & geoip to rule sets (sing-box)
* bba93a0f Added tls fragment support (Xray-core)
* 5683df2f Added outbound HTTP support (support group prefix proxy)
* b5cb9ce6 Set autoHideStartup default value is false
* 06a32dc8 Adjust sing-box dns  default example
* dff12a8a fix
* dc3f07ee Bug fix
* 1aef49ee Custom configuration file to use Xray prefix in non-Tun mode
```

Здесь видно классическое слияние: ветка контрибьютора (`80783992`) и параллельный коммит
мейнтейнера в `master` (`870955fe`) сведены merge-коммитом с двумя родителями.

Распределение коммитов по годам (по дате коммита; «squash PR» — обычный коммит, сообщение
которого заканчивается номером PR вида `(#10144)`):

```bash
git log --format='%cd|%p|%s' --date=format:%Y | awk -F'|' '
  { y = $1; c[y]++
    if (split($2, a, " ") > 1) m[y]++          # два родителя — merge-коммит
    else if ($3 ~ /\(#[0-9]+\)$/) s[y]++ }     # номер PR в конце — squash
  END { for (y in c) printf "%s %d %d %d\n", y, c[y], m[y] + 0, s[y] + 0 }' | sort
```

| Год | Коммитов | Merge-коммитов | Squash PR |
|---|---|---|---|
| 2019 | 56 | 2 | 0 |
| 2020 | 248 | 28 | 0 |
| 2021 | 70 | 8 | 0 |
| 2022 | 284 | 22 | 0 |
| 2023 | 470 | 62 | 0 |
| 2024 | 658 | 17 | 46 |
| 2025 | 719 | 0 | 176 |
| 2026 | 474 | 0 | 297 |
| **Итого** | **2979** | **139** | **519** |

Последние merge-коммиты и первые squash-коммиты:

```
$ git log --merges -3 --format='%h %ad %s' --date=short
4fc71fb7 2024-10-21 Merge branch 'master' of https://github.com/2dust/v2rayN
e223b80b 2024-05-06 Merge pull request #5066 from sincereliu/master
855fd4f0 2024-04-27 Merge pull request #5026 from GibMeMyPacket/feat/singbox/exp_cachefile

$ git log --no-merges --reverse --format='%h %ad %s' --date=short | grep -E '\(#[0-9]+\)$' | head -2
83b4f1e6 2024-05-18 Fix incorrect filenames (#5122)
63d5a2a1 2024-06-10 Fix bug (#5213)
```

**Вывод:** до мая 2024 года PR вливались кнопкой *Create a merge commit* (история ветвистая),
а с мая 2024 года — *Squash and merge*: весь PR превращается в один коммит в `master`, и после
октября 2024 года в истории нет ни одного merge-коммита. Граф `master` за 2025–2026 годы —
прямая линия.

---

## 4. Устройство отдельного коммита

`git show --stat 7674d7e4`:

```
commit 7674d7e4728b3591aff3fcdb726686a793f816ed
Author: DHR60
Date:   2026-09-10 05:52:28 +0000

    Delete redundant fields (#10144)

 v2rayN/ServiceLib/Sample/SampleOutbound | 8 +-------
 1 file changed, 1 insertion(+), 7 deletions(-)
```

Это squash-коммит PR №10144 от второго по активности автора: один файл, одна логическая правка.

---

## 5. Переименования файлов и `git log --follow`

Файл `v2rayN/ServiceLib/Models/Configs/Config.cs` (класс настроек приложения) переносился
четыре раза. Без `--follow` Git видит только историю по текущему пути:

```
$ git log --oneline -- v2rayN/ServiceLib/Models/Configs/Config.cs | wc -l
4
$ git log --follow --oneline -- v2rayN/ServiceLib/Models/Configs/Config.cs | wc -l
115
```

Цепочка переименований (`git log --follow --name-status`, строки `R`):

```
8090799c 2026-05-11 Refactor models into sub-namespaces
R097	v2rayN/ServiceLib/Models/Config.cs	v2rayN/ServiceLib/Models/Configs/Config.cs
61bea05f 2024-08-19 Refactoring Project
R097	v2rayN/v2rayN/Models/Config.cs	v2rayN/ServiceLib/Models/Config.cs
2004df83 2024-03-31 Rename Model to Models
R098	v2rayN/v2rayN/Model/Config.cs	v2rayN/v2rayN/Models/Config.cs
fc0c8f6b 2024-02-19 spell check and update
R097	v2rayN/v2rayN/Mode/Config.cs	v2rayN/v2rayN/Model/Config.cs
```

`R097` — переименование с 97 % совпадения содержимого: Git не хранит факт переноса,
а вычисляет его по похожести файлов. Самый ранний коммит файла — `8bbb50ce 2019-10-11 mge`,
то есть он существует с начала истории `master`.

`git blame` тоже прослеживает строки через переименования
(`git blame -L 1,12 --date=short v2rayN/ServiceLib/Models/Configs/Config.cs`):

```
8090799cc v2rayN/ServiceLib/Models/Configs/Config.cs (2dust 2026-05-11  1) namespace ServiceLib.Models.Configs;
4d3db5606 v2rayN/ServiceLib/Models/Config.cs         (2dust 2025-04-02  2) 
4d3db5606 v2rayN/ServiceLib/Models/Config.cs         (2dust 2025-04-02  3) [Serializable]
4d3db5606 v2rayN/ServiceLib/Models/Config.cs         (2dust 2025-04-02  4) public class Config
^8bbb50ce v2rayN/v2rayN/Mode/Config.cs               (2dust 2019-10-11  5) {
4d3db5606 v2rayN/ServiceLib/Models/Config.cs         (2dust 2025-04-02  6)     #region property
17bfe74ec v2rayN/v2rayN/Mode/Config.cs               (2dust 2023-02-11  7) 
4d3db5606 v2rayN/ServiceLib/Models/Config.cs         (2dust 2025-04-02  8)     public string IndexId { get; set; }
4d3db5606 v2rayN/ServiceLib/Models/Config.cs         (2dust 2025-04-02  9)     public string SubIndexId { get; set; }
9fd20d1dc v2rayN/v2rayN/Mode/Config.cs               (2dust 2022-10-14 10) 
4d3db5606 v2rayN/ServiceLib/Models/Config.cs         (2dust 2025-04-02 11)     #endregion property
4d3db5606 v2rayN/ServiceLib/Models/Config.cs         (2dust 2025-04-02 12) 
```

Открывающая скобка класса (строка 5) не менялась с первого коммита `^8bbb50ce` — символ `^`
означает граничный коммит, у которого нет родителя в `master`. Для каждой строки показан
путь, по которому файл лежал в момент её последнего изменения.

---

## 6. Теги и релизы

- Все 340 тегов — **лёгкие** (`git for-each-ref refs/tags --format='%(objecttype)'` → `340 commit`):
  они указывают прямо на коммит, без отдельного объекта с автором, датой и сообщением.
- Релиз фиксируется коммитом вида `up 7.25.1`, на который ставится тег.
- Между двумя последними релизами (`7.25.0` от 2026-09-05 и `7.25.1` от 2026-09-10) —
  15 коммитов (`git log --oneline 7.25.0..7.25.1 | wc -l`).
- Удалённые ветки `7.24.4` и `v7.23` — ветки старых релизов; обе полностью входят в `master`
  (`git rev-list --count master..origin/7.24.4` → `0`, для `v7.23` тоже `0`).

---

## 7. Два корня истории

```
$ git rev-list --max-parents=0 --all --format='%h %ad %an | %s' --date=short
8bbb50ce 2019-10-11 2dust | mge
7894dd93 2019-07-30 2dust | Initial commit
```

В репозитории **два корневых коммита**. `master` начинается с `8bbb50ce` (2019-10-11), а более
ранняя история — от `7894dd93 Initial commit` (2019-07-30) — с `master` не связана:
`git merge-base --is-ancestor 2.30 HEAD` возвращает «не предок». Эта старая история
(3053 − 2979 = 74 коммита) доступна только через 14 тегов с `2.30` по `2.43`, поэтому
`git log` по `master` её не показывает, а `git rev-list --all` — показывает.
Судя по датам, в октябре 2019 года автор начал `master` заново, сохранив старые релизы
только тегами.

---

## 8. Стиль сообщений коммитов

| Вид сообщения (без merge-коммитов, всего 2840) | Количество |
|---|---|
| Начинается с `Bug fix` / `Bugfix` (`grep -ciE '^bug ?fix'`) | 183 |
| `up X.Y.Z` — подъём версии (`grep -cE '^up [0-9]'`) | 200 |
| В стиле Conventional Commits (`feat:`, `fix:`, …) | 37 |

Подсчёт: `git log --no-merges --format=%s | grep ...` с указанным шаблоном.

Сообщения короткие и часто неинформативные (`Bug fix`, `fix`, `Code clean`): по `git log`
понять суть такой правки нельзя, приходится смотреть diff. У PR от внешних авторов
сообщения содержательнее, потому что squash берёт заголовок pull request.

---

## Выводы

1. История крупного проекта с одним основным мейнтейнером: 71 % коммитов — от `2dust`,
   ещё 155 авторов вносят точечные правки через PR.
2. Способ приёма PR сменился в 2024 году с merge-коммитов на squash — это видно и по графу,
   и по статистике по годам; после октября 2024 года история `master` линейная.
3. `git log --follow` и `git blame` необходимы при анализе: файл настроек менял путь четыре
   раза, и без `--follow` видно лишь 4 из 115 его изменений.
4. В репозитории два несвязанных корня; часть истории доступна только по тегам, что показывает
   разницу между `git log` (от `HEAD`) и `git rev-list --all` (от всех ссылок).
5. Сообщения коммитов в основном не информативны; в собственной лабораторной работе
   я придерживаюсь Conventional Commits, чтобы история читалась без diff.
