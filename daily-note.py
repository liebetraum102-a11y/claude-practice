from datetime import date
from pathlib import Path

# 스크립트가 있는 폴더 기준으로 notes 폴더 사용 (어디서 실행해도 같은 위치)
notes_dir = Path(__file__).resolve().parent / "notes"
notes_dir.mkdir(exist_ok=True)

note_path = notes_dir / f"{date.today():%Y-%m-%d}.md"

if note_path.exists():
    print(f"이미 오늘 메모가 있습니다: {note_path}")
else:
    note_path.write_text("# 오늘의 메모\n\n- 할 일: \n", encoding="utf-8")
    print(f"메모를 만들었습니다: {note_path}")
