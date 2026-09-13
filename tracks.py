import requests
import json
from pathlib import Path

def fetch_spark_tracks(lang="en-US"):
    url = f"https://fortnitecontent-website-prod07.ol.epicgames.com/content/api/pages/fortnite-game/spark-tracks?lang={lang}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def extract_all_tracks(data):
    tracks = []
    for key, val in data.items():
        if not isinstance(val, dict) or "track" not in val:
            continue
        track_data = val["track"]
        track_info = {k: v for k, v in track_data.items()}
        track_info["_dataKey"] = key
        try:
            qi_parsed = json.loads(track_data.get("qi", "{}"))
            track_info["sid"] = qi_parsed.get("sid", "")
            track_info["instrumentalId"] = qi_parsed.get("instrumentalId", "")
        except Exception:
            track_info["sid"] = ""
            track_info["instrumentalId"] = ""
        track_info["year"] = track_data.get("ry", "N/A")
        tracks.append(track_info)
    return tracks

def save_to_json(tracks, filename="song.json"):
    Path(filename).write_text(json.dumps(tracks, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ {len(tracks)} 件のトラック情報を保存しました")

def main():
    try:
        data = fetch_spark_tracks()
    except Exception as e:
        print(f"❌ データ取得エラー: {e}")
        return

    tracks = extract_all_tracks(data)
    if not tracks:
        print("⚠️ トラック情報が見つかりませんでした")
        return

    save_to_json(tracks)

if __name__ == "__main__":
    main()
