#!/usr/bin/env python3
"""Interactive tool to append text and generate DB files."""

from pathlib import Path


def ask_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if value < 1:
                print("1 이상의 숫자를 입력하세요.")
                continue
            return value
        except ValueError:
            print("숫자를 입력하세요.")


def append_text(target: Path, text: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and target.stat().st_size > 0:
        with target.open("a", encoding="utf-8") as f:
            f.write("\n" + text + "\n")
    else:
        with target.open("a", encoding="utf-8") as f:
            f.write(text + "\n")


def create_db_files(output_dir: Path, count: int, prefix: str, text: str) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []

    for idx in range(1, count + 1):
        db_file = output_dir / f"{prefix}_{idx}.txt"
        with db_file.open("w", encoding="utf-8") as f:
            f.write(f"DB_INDEX={idx}\n")
            f.write(text + "\n")
        created.append(db_file)

    return created


def main() -> None:
    print("=== 파일 하단 텍스트 삽입 + DB 파일 생성 도구 ===")
    target_path = Path(input("수정할 대상 파일 경로를 입력하세요: ").strip())
    insert_text = input("파일 하단에 넣을 텍스트를 입력하세요: ").strip()
    db_count = ask_int("생성할 DB 개수를 입력하세요: ")

    out_raw = input("DB 파일을 생성할 디렉터리(기본값: ./generated_dbs): ").strip()
    output_dir = Path(out_raw) if out_raw else Path("generated_dbs")

    prefix = input("생성 파일 접두어(기본값: db): ").strip() or "db"

    append_text(target_path, insert_text)
    created_files = create_db_files(output_dir, db_count, prefix, insert_text)

    print("\n작업 완료:")
    print(f"- 대상 파일 수정: {target_path.resolve()}")
    print(f"- 생성된 DB 파일 수: {len(created_files)}")
    print(f"- 생성 경로: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
