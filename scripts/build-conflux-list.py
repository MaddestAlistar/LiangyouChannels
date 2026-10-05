#!/usr/bin/env python3
"""Build Conflux's schemaVersion 1 streamer list from the channel catalog."""
import argparse
import json
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "liangyouchannels-conflux.json"
PLATFORMS = [("douyin", "抖音"), ("douyu", "斗鱼"), ("huya", "虎牙"), ("bilibili", "B站"), ("yy", "YY")]


def read(relative_path):
    path = (ROOT / relative_path).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError("Data file must be inside the repository")
    return json.loads(path.read_text(encoding="utf-8"))


def build(updated_at):
    updated_at = date.fromisoformat(updated_at).isoformat()
    source = read("channel-data.json")
    channels = list(source["channels"])
    for filename in source.get("monthlyAuthorFiles", []):
        channels.extend(read(filename)["channels"])
    if source.get("total", len(channels)) != len(channels):
        raise ValueError("Incomplete source catalog")

    monthly = read("monthly-selected.json")
    authors = list(monthly.get("authors", []))
    for filename in monthly.get("authorFiles", []):
        authors.extend(read(filename)["authors"])
    memberships = {a["channelId"]: a["selectedMonths"] for a in authors}
    platform_ids = {p for p, _ in PLATFORMS}
    if any(c["platform"] not in platform_ids for c in channels):
        raise ValueError("Unmapped platform")

    entries, seen = [], set()
    for platform, _ in PLATFORMS:
        for c in channels:
            if c["platform"] != platform:
                continue
            room_id = c["roomId"]
            if not isinstance(room_id, str) or not room_id or room_id != c["copyValue"]:
                raise ValueError("Room identifiers must remain exact strings")
            if not isinstance(c["name"], str) or not c["name"].strip():
                raise ValueError("Every entry requires a display name")
            key = (platform, room_id)
            if key in seen:
                raise ValueError("Duplicate platform and roomId: " + repr(key))
            seen.add(key)
            entry = {"platform": platform, "roomId": room_id, "name": c["name"], "avatar": c["avatar"], "sections": [platform]}
            if not isinstance(entry["avatar"], str) or not entry["avatar"].startswith("https://"):
                raise ValueError("Avatar must be an absolute HTTPS URL")
            if c["id"] in memberships:
                entry["sections"].append("douyin-monthly")
                entry["note"] = "抖音月度精选：" + "、".join(memberships[c["id"]]) + "。"
            entries.append(entry)

    d = date.fromisoformat(updated_at)
    document = {
        "schemaVersion": 1,
        "name": "良友频道库 · 汇流直播",
        "description": f"由小红书：良哥看未来整理，更新时间：{d.year} 年 {d.month} 月 {d.day} 日。共 {len(entries)} 个频道与作者。抖音月度精选包含短视频作者，按官方抖音号收录；开播情况以平台显示为准。",
        "author": {"name": "良哥看未来", "url": "https://github.com/MaddestAlistar/LiangyouChannels"},
        "updatedAt": updated_at,
        "sections": [{"id": p, "name": name} for p, name in PLATFORMS] + [{"id": "douyin-monthly", "name": "抖音月度精选"}],
        "entries": entries,
    }
    section_ids = {s["id"] for s in document["sections"]}
    assert len(section_ids) == len(document["sections"])
    assert all(set(e["sections"]) <= section_ids for e in entries)
    header = json.dumps({k: v for k, v in document.items() if k != "entries"}, ensure_ascii=False, indent=2)
    text = header[:-2] + ',\n  "entries": [\n' + ',\n'.join('    ' + json.dumps(e, ensure_ascii=False, separators=(',', ':')) for e in entries) + '\n  ]\n}\n'
    assert json.loads(text) == document
    if len(text.encode("utf-8")) > 20_000_000:
        raise ValueError("Conflux streamer lists must be under 20 MB")
    OUTPUT.write_text(text, encoding="utf-8")
    return {"entries": len(entries), "sections": len(section_ids), "monthlyAuthors": sum("douyin-monthly" in e["sections"] for e in entries), "bytes": OUTPUT.stat().st_size, "updatedAt": updated_at}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--updated-at", default=datetime.now(ZoneInfo("Asia/Shanghai")).date().isoformat())
    args = parser.parse_args()
    print(json.dumps(build(args.updated_at), ensure_ascii=False))
