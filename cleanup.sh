#!/usr/bin/env bash
# 날짜가 적힌 메모 파일(.md/.txt)을 notes_archive 폴더로 옮긴다.
# 사용법: ./cleanup.sh            목록을 보여준 뒤 확인(y)하면 옮김
#         ./cleanup.sh --dry-run  목록만 보여주고 옮기지 않음

cd "$(dirname "$0")" || exit 1

ARCHIVE="notes_archive"
DATE_PATTERN='[0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{8}'

# 날짜가 들어간 .md/.txt 파일 찾기 (.git과 보관 폴더는 제외)
mapfile -t files < <(
    find . -path ./.git -prune -o -path "./$ARCHIVE" -prune -o \
        -type f \( -name "*.md" -o -name "*.txt" \) -print |
    grep -E "/[^/]*($DATE_PATTERN)[^/]*$" | sort
)

if [ ${#files[@]} -eq 0 ]; then
    echo "옮길 파일이 없습니다."
    exit 0
fi

echo "다음 ${#files[@]}개 파일이 $ARCHIVE/ 로 옮겨집니다:"
for f in "${files[@]}"; do
    echo "  ${f#./}"
done

if [ "$1" = "--dry-run" ]; then
    echo "(--dry-run: 실제로 옮기지 않았습니다)"
    exit 0
fi

read -r -p "계속할까요? [y/N] " answer
if [ "$answer" != "y" ] && [ "$answer" != "Y" ]; then
    echo "취소했습니다."
    exit 0
fi

mkdir -p "$ARCHIVE"
for f in "${files[@]}"; do
    name=$(basename "$f")
    if [ -e "$ARCHIVE/$name" ]; then
        echo "건너뜀 (같은 이름이 이미 있음): ${f#./}"
        continue
    fi
    mv "$f" "$ARCHIVE/" && echo "옮김: ${f#./}"
done
