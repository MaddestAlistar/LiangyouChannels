#!/usr/bin/env python3
"""Build the complete ten-section Conflux v1 subscription and legacy aliases.

Include unverified records with their editorial notes. Keep validation metadata
in data/room-validation.json, separate from the public subscription. Exclude only
confirmed invalid rooms; an offline state or CAPTCHA is not proof of invalidity.
"""
import argparse
import json
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]


def read(relative):
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError('Catalog paths must stay inside the repository')
    return json.loads(path.read_text(encoding='utf-8'))


def write(relative, document):
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    header = {k: v for k, v in document.items() if k != 'entries'}
    text = json.dumps(header, ensure_ascii=False, indent=2)[:-2]
    text += ',\n  "entries": [\n'
    text += ',\n'.join('    '+json.dumps(e,ensure_ascii=False,separators=(',',':')) for e in document['entries'])
    text += '\n  ]\n}\n'
    if len(text.encode('utf-8')) > 20_000_000:
        raise ValueError('Conflux list exceeds 20 MB')
    if json.loads(text) != document:
        raise ValueError('Serialization changed the document')
    path.write_text(text,encoding='utf-8')


def build(updated_at):
    day=date.fromisoformat(updated_at)
    source=read('channel-data.json')
    channels=list(source['channels'])
    for filename in source.get('monthlyAuthorFiles',[]):
        channels.extend(read(filename)['channels'])
    if len(channels)!=source.get('total',len(channels)):
        raise ValueError('Incomplete source catalog')
    curation=read('data/channel-curation.json')
    audit=read('data/room-validation.json')
    editorial={x['id']:x for x in curation['entries']}
    checks={x['id']:x for x in audit['entries']}
    ids={c['id'] for c in channels}
    if ids!=set(editorial) or ids!=set(checks):
        raise ValueError('Every source channel needs editorial and audit records')
    sections=curation['sections']
    section_ids={x['id'] for x in sections}
    if len(sections)!=10 or len(section_ids)!=10:
        raise ValueError('Exactly ten unique content sections are required')

    entries=[]
    verified=[]
    excluded=[]
    seen=set()
    for c in channels:
        room_id=c['roomId']
        if not isinstance(room_id,str) or not room_id or room_id!=c['copyValue']:
            raise ValueError('Room identifiers must remain exact strings: '+c['id'])
        if c['platform'] not in {'douyin','douyu','huya','bilibili','yy'}:
            raise ValueError('Unsupported platform: '+c['platform'])
        key=(c['platform'],room_id)
        if key in seen:raise ValueError('Duplicate room: '+repr(key))
        seen.add(key)
        e=editorial[c['id']]
        check=checks[c['id']]
        if check['platform']!=c['platform'] or check['roomId']!=room_id:
            raise ValueError('Audit identifier differs: '+c['id'])
        if not e['note'] or not 6<=len(e['note'])<=22:
            raise ValueError('Missing or overly long note: '+c['id'])
        if e['section'] not in section_ids:
            raise ValueError('Unknown section: '+c['id'])
        entry={'platform':c['platform'],'roomId':room_id,'name':c['name'],
               'avatar':c['avatar'],'sections':[e['section']],'note':e['note']}
        if not entry['name'] or not entry['avatar'].startswith('https://'):
            raise ValueError('Invalid name/avatar: '+c['id'])
        if check['status']=='invalid':
            excluded.append(c['id'])
            continue
        entries.append(entry)
        if check['status']=='valid':
            if not check.get('checkedAt') or not check.get('sourceUrl') or not check.get('ownerUid'):
                raise ValueError('Verified entry has incomplete evidence: '+c['id'])
            if not check.get('resolvedRoomId'):
                raise ValueError('Verified audit record is missing a room: '+c['id'])
            verified.append(entry)
    order={x['id']:i for i,x in enumerate(sections)}
    entries.sort(key=lambda e:order[e['sections'][0]])
    common={'schemaVersion':1,'author':{'name':'良哥看未来','url':'https://github.com/MaddestAlistar/LiangyouChannels'},
            'updatedAt':day.isoformat(),'sections':sections}
    label=f'由小红书：良哥看未来整理，更新时间：{day.year} 年 {day.month} 月 {day.day} 日。'
    document={**common,'name':'良友频道库 · 汇流直播',
        'description':label+f'共 {len(entries)} 个频道与作者。抖音月度精选包含短视频作者，按官方抖音号收录；开播情况以平台显示为准。',
        'entries':entries}
    # Keep previously shared URLs working with the same complete, clean content.
    for output in ('liangyouchannels-conflux.json',
                   'liangyouchannels-conflux-verified.json',
                   'drafts/liangyouchannels-conflux-categorized.json'):
        write(output,document)
    return {'source':len(channels),'entries':len(entries),'recordedValidRooms':len(verified),
            'invalidExcluded':len(excluded),'sections':len(sections),
            'byPlatform':dict(Counter(e['platform'] for e in entries)),
            'bySection':dict(Counter(e['sections'][0] for e in entries))}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--updated-at',default=datetime.now(ZoneInfo('Asia/Shanghai')).date().isoformat())
    print(json.dumps(build(p.parse_args().updated_at),ensure_ascii=False))


if __name__=='__main__':
    main()
