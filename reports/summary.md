# claude-practice 폴더 요약 보고서

작성일: 2026-10-13
대상: `claude-practice` 폴더 전체 (`.git` 폴더 제외, 이 보고서 제외)
파일 수: 총 34개 (그중 내용이 없는 빈 파일 16개)

## 최상위 폴더 (6개)

| 파일 | 설명 |
|---|---|
| `CLAUDE.md` | Claude Code에 주는 규칙. 답변은 한국어로, 파일을 수정하기 전에는 먼저 설명할 것 |
| `count_files.py` | 폴더별 파일 수를 세어 출력하는 스크립트 |
| `daily-note.py` | `notes` 폴더에 오늘 날짜 이름으로 메모 파일을 만드는 스크립트 |
| `list_files.py` | 모든 파일의 이름과 크기를 `file_list.txt`에 저장하는 스크립트 |
| `organize.py` | 파일을 확장자별 폴더로 옮기는 정리 스크립트. `--dry-run` 옵션을 주면 실제로 옮기지 않고 결과만 미리 보여줌 |
| `file_list.txt` | `list_files.py`로 만든 파일 목록과 크기. 이후에 생긴 파일은 들어 있지 않음 |

## csv/ (1개)

| 파일 | 설명 |
|---|---|
| `data.csv` | 빈 파일 |

## md/ (3개)

| 파일 | 설명 |
|---|---|
| `memo.md` | 학습 메모 (파일을 대화로 만들고 고치는 법, CLAUDE.md 규칙) |
| `notes.md` | 빈 파일 |
| `todo.md` | 2026-09-28 할 일 목록. 4개 항목 모두 완료 |

## notes/ (1개)

| 파일 | 설명 |
|---|---|
| `2026-10-07.md` | `daily-note.py`로 만든 메모 양식. 할 일 칸은 비어 있음 (아직 git에 커밋되지 않음) |

## pdf/ (4개)

| 파일 | 설명 |
|---|---|
| `invoice.pdf`, `invoice_1.pdf` | 빈 파일 (연습용) |
| `report.pdf`, `report_1.pdf` | 빈 파일 (연습용) |

## png/ (3개)

| 파일 | 설명 |
|---|---|
| `photo.png`, `photo1.png`, `photo1_1.png` | 빈 파일 (연습용) |

## txt/ (15개)

| 파일 | 설명 |
|---|---|
| `memo.txt` | Claude Code 5일차 학습 메모 |
| `note.txt` | git 학습 메모 (2줄) |
| `todo.txt` | 2026-10-02 할 일 3개 (모두 미완료) |
| `practice.txt`, `test.txt` | "안녕하세요" 한 줄 |
| `meeting_20261002_01.txt`, `memo_20261002_01.txt` | "테스트 내용" 한 줄 |
| `photo_20261002_01.txt` ~ `_03.txt` | "테스트 내용" 한 줄 (3개) |
| `memo_1.txt`, `note1.txt`, `notes.txt`, `report.txt`, `todo_1.txt` | 빈 파일 |

## 내소개/ (1개)

| 파일 | 설명 |
|---|---|
| `index.html` | "토베니 소개" 자기소개 웹페이지 |

## 참고

- `_1`이 붙은 파일(`invoice_1.pdf`, `memo_1.txt` 등)은 `organize.py`로 옮길 때 같은 이름의 파일이 이미 있어서 이름이 바뀐 것으로 보입니다.
- 빈 파일과 "테스트 내용"만 있는 파일은 대부분 연습용이라 정리해도 될 후보입니다.
