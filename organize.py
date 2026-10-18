"""폴더 안의 파일들을 확장자별 하위 폴더로 분류하는 스크립트.

사용법:
    python organize.py              # test_files 폴더 정리
    python organize.py <폴더경로>   # 지정한 폴더 정리
"""

import shutil
import sys
from pathlib import Path


def organize(folder: Path) -> None:
    if not folder.is_dir():
        print(f"폴더를 찾을 수 없습니다: {folder}")
        sys.exit(1)

    moved = 0
    for item in folder.iterdir():
        if not item.is_file():
            continue

        # 확장자가 없는 파일은 no_extension 폴더로
        ext = item.suffix.lower().lstrip(".") or "no_extension"
        target_dir = folder / ext
        target_dir.mkdir(exist_ok=True)

        # 같은 이름의 파일이 이미 있으면 덮어쓰지 않고 번호를 붙임
        target = target_dir / item.name
        count = 1
        while target.exists():
            target = target_dir / f"{item.stem}_{count}{item.suffix}"
            count += 1

        shutil.move(str(item), str(target))
        print(f"{item.name} -> {ext}/{target.name}")
        moved += 1

    print(f"\n총 {moved}개 파일을 정리했습니다.")


if __name__ == "__main__":
    target_folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("test_files")
    organize(target_folder)
