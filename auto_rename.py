import os
import shutil
import sys

try:
    from mutagen.id3 import ID3NoHeaderError
    from mutagen.mp3 import MP3
except ImportError:
    print("❗ 'mutagen' 패키지가 설치되지 않았습니다.")
    print("터미널에 'pip install mutagen'을 입력하여 설치한 후 다시 실행해주세요.")
    sys.exit(1)

# 현재 파이썬 스크립트 위치 기준 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
old_folder = os.path.join(current_dir, "old")
new_folder = os.path.join(current_dir, "new")


def sanitize_filename(filename):
    invalid_chars = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]
    for char in invalid_chars:
        filename = filename.replace(char, "")
    return filename.strip()


def fix_encoding(text):
    """깨진 한글 태그(Latin1 -> CP949)를 정상적인 한글로 복구하는 함수"""
    try:
        return text.encode("latin1").decode("cp949")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return text


def process_music_files_by_tag():
    # ✨ [변경] old 폴더가 없으면 새로 생성합니다.
    if not os.path.exists(old_folder):
        os.makedirs(old_folder)
        print(
            "📁 'old' 폴더를 새로 만들었습니다. 이 폴더에 변환할 음악 파일들을 넣어주세요!"
        )
        return  # 새로 만들었을 때는 안에 파일이 없으므로 종료합니다.

    # ✨ [변경] new 폴더가 없으면 새로 생성합니다.
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
        print("📁 'new' 폴더를 새로 만들었습니다.")

    files = os.listdir(old_folder)

    # old 폴더에 파일이 하나도 없는 경우 안내
    if not files:
        print(
            "ℹ️ 'old' 폴더가 비어 있습니다. 변환할 .mp3 파일들을 'old' 폴더에 넣고 다시 실행해주세요."
        )
        return

    count = 0

    for filename in files:
        if filename.endswith(".mp3"):
            src_file = os.path.join(old_folder, filename)

            try:
                audio = MP3(src_file)

                if audio.tags and "TIT2" in audio.tags:
                    raw_title = audio.tags["TIT2"].text[0]
                    song_title = fix_encoding(raw_title)
                else:
                    print(
                        f"⚠️ 제목 태그 없음 (건너뜀): {filename}"
                    )
                    continue

                song_title = sanitize_filename(song_title)

                if not song_title:
                    print(
                        f"⚠️ 태그 제목이 유효하지 않음 (건너뜀): {filename}"
                    )
                    continue

                new_filename = f"{song_title}.mp3"
                dst_file = os.path.join(new_folder, new_filename)

                shutil.copy(src_file, dst_file)
                print(f"✅ 변환 완료: {filename} -> new/{new_filename}")
                count += 1

            except ID3NoHeaderError:
                print(
                    f"❌ 태그 정보가 아예 없는 파일입니다: {filename}"
                )
            except Exception as e:
                print(f"❌ 오류 발생 ({filename}): {e}")

    if count > 0:
        print(
            f"\n🎉 총 {count}개의 파일 처리가 완료되었습니다. 'new' 폴더를 확인해 보세요!"
        )


if __name__ == "__main__":
    process_music_files_by_tag()