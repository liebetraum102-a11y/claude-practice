# 파일과 폴더를 다루기 위해 os 모듈을 불러온다
import os

# 이 스크립트가 있는 폴더(claude-practice)의 경로를 구한다
base_dir = os.path.dirname(os.path.abspath(__file__))
# 결과를 저장할 파일 경로를 만든다
output_path = os.path.join(base_dir, "file_list.txt")

# 파일 정보를 담을 빈 리스트를 만든다
lines = []

# 폴더 안의 모든 하위 폴더와 파일을 차례로 돈다
for folder, subfolders, files in os.walk(base_dir):
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
        # 파일 크기를 바이트 단위로 읽는다
        size = os.path.getsize(full_path)
        # "경로 - 크기" 형태의 한 줄을 리스트에 추가한다
        lines.append(f"{relative_path} - {size} bytes")

# 결과 파일을 UTF-8로 열어서 쓰기 모드로 준비한다
with open(output_path, "w", encoding="utf-8") as f:
    # 모든 줄을 줄바꿈으로 이어서 파일에 쓴다
    f.write("\n".join(lines) + "\n")

# 작업이 끝났다는 메시지와 파일 개수를 출력한다
print(f"{len(lines)}개 파일 정보를 {output_path}에 저장했습니다.")
