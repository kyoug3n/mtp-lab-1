#!/bin/sh
# Формирует текстовый отчёт о коммитах с помощью git shortlog.
# Запуск из корня репозитория:
#     sh scripts/shortlog_report.sh [ревизия] > reports/shortlog.txt
# По умолчанию анализируется ветка main.
set -e

REV=${1:-main}

section() {
    printf '\n== %s\n$ %s\n' "$1" "$2"
}

echo "Отчёт о коммитах (git shortlog)"
echo "Ревизия:     $REV = $(git rev-parse --short "$REV") ($(git log -1 --format=%cd --date=iso "$REV"))"
echo "Сформирован: $(date '+%Y-%m-%d %H:%M:%S %z')"
echo "Команда:     sh scripts/shortlog_report.sh $REV > reports/shortlog.txt"
echo "Коммиты, сделанные после указанной ревизии, в отчёт не входят."

section "1. Авторы и количество коммитов" "git shortlog -sne $REV"
git shortlog -sne "$REV"

section "2. То же без merge-коммитов" "git shortlog -sne --no-merges $REV"
git shortlog -sne --no-merges "$REV"

section "3. Количество коммитов по дням" "git shortlog -s --group=format:%cs $REV"
git shortlog -s --group=format:%cs "$REV"

section "4. Количество коммитов по типам Conventional Commits" \
    "git log --format=%s $REV | sed -E 's/^(fixup! )?([a-z]+)(\\(.*\\))?:.*/\\2/' | sort | uniq -c | sort -rn"
git log --format=%s "$REV" | sed -E 's/^(fixup! )?([a-z]+)(\(.*\))?:.*/\2/' | sort | uniq -c | sort -rn

section "5. Сравнение: коммиты во всех ветках" "git shortlog -sn --all"
git shortlog -sn --all

section "6. Коммиты, сгруппированные по авторам" "git shortlog $REV"
git shortlog "$REV"
