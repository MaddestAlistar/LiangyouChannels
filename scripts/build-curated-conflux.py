#!/usr/bin/env python3
"""Build the ten-section editorial draft and the verified-only Conflux v1 list.

Only `valid` room checks enter the verified list. A resolved account without a
room, access challenges, network failures and unchecked entries stay in the
draft. Never infer deletion from an offline state or a CAPTCHA.
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
        entries.append({**entry,'validationStatus':check['status']})
        if check['status']=='valid':
            if not check.get('checkedAt') or not check.get('sourceUrl') or not check.get('ownerUid'):
                raise ValueError('Verified entry has incomplete evidence: '+c['id'])
            if not check.get('resolvedRoomId'):
                raise ValueError('Account-only entry cannot enter verified list: '+c['id'])
            checked_day=datetime.fromisoformat(check['checkedAt']).astimezone(ZoneInfo('Asia/Shanghai')).date()
            if checked_day != day:
                raise ValueError('Recheck rooms before publishing a new dated list: '+c['id'])
            verified.append(entry)
    order={x['id']:i for i,x in enumerate(sections)}
    entries.sort(key=lambda e:order[e['sections'][0]])
    verified.sort(key=lambda e:order[e['sections'][0]])
    common={'schemaVersion':1,'author':{'name':'良哥看未来','url':'https://github.com/MaddestAlistar/LiangyouChannels'},
            'updatedAt':day.isoformat(),'sections':sections}
    label=f'由小红书：良哥看未来整理，更新时间：{day.year} 年 {day.month} 月 {day.day} 日。'
    verified_doc={**common,'name':'良友频道库 · 汇流直播（已核验）',
        'description':label+f'共 {len(verified)} 个已确认房间，按内容分为10区，每条附一句简介。核验确认房间归属，不代表当前正在开播。',
        'entries':verified}
    draft_doc={**common,'name':'良友频道库 · 全量分类整理稿（待完成核验）',
        'description':label+f'共 {len(entries)} 条，分区和简介已整理；全量房间核验尚未完成。只确认到账号、访问受限及未检查的条目保留在此整理稿，不计入已核验名单。',
        'auditSummary':audit['summary'],'entries':entries}
    write('liangyouchannels-conflux-verified.json',verified_doc)
    write('drafts/liangyouchannels-conflux-categorized.json',draft_doc)
    return {'source':len(channels),'draft':len(entries),'verified':len(verified),'invalidExcluded':len(excluded),
            'sections':len(sections),'verifiedByPlatform':dict(Counter(e['platform'] for e in verified)),
            'verifiedBySection':dict(Counter(e['sections'][0] for e in verified))}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--updated-at',default=datetime.now(ZoneInfo('Asia/Shanghai')).date().isoformat())
    print(json.dumps(build(p.parse_args().updated_at),ensure_ascii=False))
