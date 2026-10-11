# 파일과 폴더를 다루기 위해 os 모듈을, 오류 시 종료하기 위해 sys 모듈을 불러온다
import os
import sys

# 이 스크립트가 있는 폴더(claude-practice)의 경로를 구한다
base_dir = os.path.dirname(os.path.abspath(__file__))
# 결과를 저장할 파일 경로를 만든다
output_path = os.path.join(base_dir, "file_list.txt")

# 파일 정보를 담을 빈 리스트를 만든다
lines = []


# 열 수 없는 폴더를 만나면 멈추지 않고 알려준 뒤 건너뛴다
def on_walk_error(error):
    print(f"폴더를 열 수 없어 건너뜁니다: {error.filename}")


# 폴더 안의 모든 하위 폴더와 파일을 차례로 돈다
for folder, subfolders, files in os.walk(base_dir, onerror=on_walk_error):
    # .git 폴더는 내부 관리용이므로 탐색에서 제외한다
    if ".git" in subfolders:
        subfolders.remove(".git")
    # 현재 폴더 안의 파일들을 하나씩 확인한다
    for name in files:
        # 파일의 전체 경로를 만든다
        full_path = os.path.join(folder, name)
        # 결과 파일 자신은 목록에서 뺀다
        if full_path == output_path:
            continue
        # 기준 폴더로부터의 상대 경로를 구한다
        relative_path = os.path.relpath(full_path, base_dir)
        # 파일 크기를 바이트 단위로 읽는다 (도중에 사라졌거나 읽을 수 없으면 표시만 해둔다)
        try:
            size = os.path.getsize(full_path)
        except OSError:
            print(f"크기를 확인할 수 없는 파일이 있습니다: {relative_path}")
            lines.append(f"{relative_path} - 크기 확인 불가")
            continue
        # "경로 - 크기" 형태의 한 줄을 리스트에 추가한다
        lines.append(f"{relative_path} - {size} bytes")

# 결과 파일을 UTF-8로 열어서 쓴다 (저장할 수 없으면 이유를 알려주고 종료한다)
try:
    with open(output_path, "w", encoding="utf-8") as f:
        # 모든 줄을 줄바꿈으로 이어서 파일에 쓴다
        f.write("\n".join(lines) + "\n")
except PermissionError:
    print(f"{output_path}에 저장할 수 없습니다. "
          f"파일이 다른 프로그램에서 열려 있거나 읽기 전용인지 확인한 뒤 다시 실행해 주세요.")
    sys.exit(1)
except OSError as e:
    print(f"{output_path}에 저장하는 중 문제가 생겼습니다. ({e})")
    sys.exit(1)

# 작업이 끝났다는 메시지와 파일 개수를 출력한다
print(f"{len(lines)}개 파일 정보를 {output_path}에 저장했습니다.")
