# 파일과 폴더를 다루기 위해 os, shutil 모듈을, 실행 옵션을 읽기 위해 argparse 모듈을 불러온다
import argparse
import os
import shutil
import sys


# 잘못된 옵션을 넣었을 때 영어 오류 대신 한국어 안내를 보여주는 파서
class FriendlyParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"잘못된 옵션입니다. ({message})")
        print("사용법: python organize.py [--dry-run]")
        print("자세한 도움말: python organize.py --help")
        sys.exit(2)


# --dry-run 옵션을 주면 실제로 옮기지 않고 어디로 이동할지만 보여준다
parser = FriendlyParser(description="루트의 파일을 확장자별 폴더로 정리한다")
parser.add_argument("--dry-run", action="store_true", help="파일을 옮기지 않고 이동 계획만 출력")
args = parser.parse_args()

# 이 스크립트가 있는 폴더(claude-practice)의 경로를 구한다
base_dir = os.path.dirname(os.path.abspath(__file__))

# 정리하지 않고 루트에 남겨둘 파일 이름들
keep_files = {"CLAUDE.md", "file_list.txt"}
# 정리하지 않을 확장자들 (스크립트는 루트에 있어야 실행하기 편하다)
keep_exts = {"py"}

# 옮긴 파일 수와 옮기지 못한 파일 수를 센다
moved = 0
failed = 0
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
    # 같은 이름의 "파일"이 있으면 폴더를 만들 수 없으므로 미리 알려주고 건너뛴다
    if os.path.exists(target_dir) and not os.path.isdir(target_dir):
        print(f"{name}: '{ext}'라는 이름의 파일이 이미 있어서 {ext} 폴더를 만들 수 없습니다. "
              f"그 파일의 이름을 바꾼 뒤 다시 실행해 주세요.")
        failed += 1
        continue

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
        moved += 1
        continue

    # 확장자 폴더를 만들고(이미 있으면 그대로 쓴다) 파일을 옮긴다
    # 한 파일에서 문제가 생겨도 멈추지 않고 안내만 한 뒤 다음 파일로 넘어간다
    try:
        os.makedirs(target_dir, exist_ok=True)
        shutil.move(src, os.path.join(target_dir, new_name))
    except FileNotFoundError:
        print(f"{name}: 파일을 찾을 수 없어 건너뜁니다. (정리 도중 삭제되거나 이름이 바뀌었을 수 있습니다)")
        failed += 1
        continue
    except PermissionError:
        print(f"{name}: 다른 프로그램에서 열려 있거나 권한이 없어 옮기지 못했습니다. "
              f"파일을 닫고 다시 실행해 주세요.")
        failed += 1
        continue
    except OSError as e:
        print(f"{name}: 옮기는 중 문제가 생겨 건너뜁니다. ({e})")
        failed += 1
        continue
    print(f"{name} -> {ext}/{new_name}")
    moved += 1

# 작업이 끝났다는 메시지와 파일 개수를 출력한다
if args.dry_run:
    print(f"{moved}개 파일이 이동될 예정입니다. (실제로 옮기지 않았습니다)")
else:
    print(f"{moved}개 파일을 정리했습니다.")
if failed:
    result = "옮길 수 없습니다" if args.dry_run else "옮기지 못했습니다"
    print(f"{failed}개 파일은 {result}. 위의 안내를 확인해 주세요.")
    sys.exit(1)
