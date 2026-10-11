# 파일과 폴더를 다루기 위해 os 모듈을 불러온다
import os

# 이 스크립트가 있는 폴더(claude-practice)의 경로를 구한다
base_dir = os.path.dirname(os.path.abspath(__file__))

# 폴더별 파일 수를 담을 딕셔너리를 만든다 (예: {"txt": 13, ".": 6})
counts = {}


# 열 수 없는 폴더를 만나면 멈추지 않고 알려준 뒤 건너뛴다
def on_walk_error(error):
    print(f"폴더를 열 수 없어 건너뜁니다: {error.filename}")


# 폴더 안의 모든 하위 폴더와 파일을 차례로 돈다
for folder, subfolders, files in os.walk(base_dir, onerror=on_walk_error):
    # .git 폴더는 내부 관리용이므로 탐색에서 제외한다
    if ".git" in subfolders:
        subfolders.remove(".git")
    # 기준 폴더로부터의 상대 경로를 폴더 이름으로 쓴다 (루트는 ".")
    relative_folder = os.path.relpath(folder, base_dir)
    # 현재 폴더의 파일 수를 기록한다
    counts[relative_folder] = len(files)

# 폴더별 파일 수를 이름 순으로 출력한다
for relative_folder in sorted(counts):
    label = "(루트)" if relative_folder == "." else relative_folder
    print(f"{label}: {counts[relative_folder]}개")

# 전체 파일 수를 출력한다
print(f"전체 파일 수: {sum(counts.values())}개 (.git 폴더 제외)")
