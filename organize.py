# 파일과 폴더를 다루기 위해 os, shutil 모듈을, 실행 옵션을 읽기 위해 argparse 모듈을 불러온다
import argparse
import os
import shutil

# --dry-run 옵션을 주면 실제로 옮기지 않고 어디로 이동할지만 보여준다
parser = argparse.ArgumentParser(description="루트의 파일을 확장자별 폴더로 정리한다")
parser.add_argument("--dry-run", action="store_true", help="파일을 옮기지 않고 이동 계획만 출력")
args = parser.parse_args()

# 이 스크립트가 있는 폴더(claude-practice)의 경로를 구한다
base_dir = os.path.dirname(os.path.abspath(__file__))

# 정리하지 않고 루트에 남겨둘 파일 이름들
keep_files = {"CLAUDE.md", "file_list.txt"}
# 정리하지 않을 확장자들 (스크립트는 루트에 있어야 실행하기 편하다)
keep_exts = {"py"}

# 옮긴 파일 수를 센다
moved = 0
# 이번 실행에서 이미 배정한 이동 경로 (미리보기에서도 이름이 겹치지 않게 하기 위해)
planned = set()

# 루트 폴더에 바로 있는 항목들만 하나씩 확인한다 (하위 폴더 안은 건드리지 않는다)
for name in sorted(os.listdir(base_dir)):
    src = os.path.join(base_dir, name)
    # 폴더는 건너뛴다
    if not os.path.isfile(src):
        continue
    # 남겨둘 파일은 건너뛴다
    if name in keep_files:
        continue

    # 파일 이름을 "이름"과 "확장자"로 나눈다 (예: report.pdf -> report, .pdf)
    stem, ext = os.path.splitext(name)
    ext = ext.lstrip(".").lower()
    # 확장자가 없거나 남겨둘 확장자면 건너뛴다
    if not ext or ext in keep_exts:
        continue

    # 확장자 이름의 폴더 경로를 정한다
    target_dir = os.path.join(base_dir, ext)

    # 같은 이름의 파일이 이미 있거나 이번에 배정됐으면 _1, _2 ... 번호를 붙여 덮어쓰지 않게 한다
    new_name = name
    count = 1
    while (os.path.exists(os.path.join(target_dir, new_name))
           or os.path.join(ext, new_name).lower() in planned):
        new_name = f"{stem}_{count}.{ext}"
        count += 1
    planned.add(os.path.join(ext, new_name).lower())

    if args.dry_run:
        # 미리보기에서는 폴더도 만들지 않고 이동 계획만 출력한다
        print(f"[미리보기] {name} -> {ext}/{new_name}")
    else:
        # 확장자 폴더를 만들고(이미 있으면 그대로 쓴다) 파일을 옮긴다
        os.makedirs(target_dir, exist_ok=True)
        shutil.move(src, os.path.join(target_dir, new_name))
        print(f"{name} -> {ext}/{new_name}")
    moved += 1

# 작업이 끝났다는 메시지와 파일 개수를 출력한다
if args.dry_run:
    print(f"{moved}개 파일이 이동될 예정입니다. (실제로 옮기지 않았습니다)")
else:
    print(f"{moved}개 파일을 정리했습니다.")
