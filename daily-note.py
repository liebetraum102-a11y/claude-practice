import sys
from datetime import date
from pathlib import Path

# 스크립트가 있는 폴더 기준으로 notes 폴더 사용 (어디서 실행해도 같은 위치)
notes_dir = Path(__file__).resolve().parent / "notes"
try:
    notes_dir.mkdir(exist_ok=True)
except FileExistsError:
    # notes라는 이름의 "파일"이 있으면 폴더를 만들 수 없다
    print(f"'{notes_dir}'라는 이름의 파일이 있어서 notes 폴더를 만들 수 없습니다. 그 파일의 이름을 바꾼 뒤 다시 실행해 주세요.")
    sys.exit(1)
except OSError as e:
    print(f"notes 폴더를 만들 수 없습니다. 폴더 권한을 확인해 주세요. ({e})")
    sys.exit(1)

# 실행할 때 오늘 날짜를 요일과 함께 보여주기
today = date.today()
weekdays = ["월", "화", "수", "목", "금", "토", "일"]
print(f"오늘은 {today.year}년 {today.month:02d}월 {today.day:02d}일 ({weekdays[today.weekday()]}요일)입니다.")

note_path = notes_dir / f"{today:%Y-%m-%d}.md"

if note_path.exists():
    print(f"이미 오늘 메모가 있습니다: {note_path}")
else:
    try:
        note_path.write_text("# 오늘의 메모\n\n- 할 일: \n", encoding="utf-8")
    except OSError as e:
        print(f"메모 파일을 만들 수 없습니다. notes 폴더의 권한을 확인해 주세요. ({e})")
        sys.exit(1)
    print(f"메모를 만들었습니다: {note_path}")
