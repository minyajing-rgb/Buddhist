#!/usr/bin/env python3
"""Rebuild flagged relations from a pinned official SuttaCentral snapshot.
Only use groups containing the target as an unmarked member. Do not infer links
between two '~' entries that merely resemble a third group. Keep segment locators.
This validates source encoding, not independent philological equivalence.
"""
from __future__ import annotations
import argparse,hashlib,json,pathlib,re,urllib.request
COMMIT='46cfa52c25a5cff9acd296794e5e9b8b388121a5'
SHA256='129ec287aaa0e90f47f6315b4355ad5ea07804bea18a274e39107b93ce17c7f2'
URL=f'https://raw.githubusercontent.com/suttacentral/sc-data/{COMMIT}/relationship/parallels.json'
SOURCE=f'https://github.com/suttacentral/sc-data/blob/{COMMIT}/relationship/parallels.json'
FLAGGED=['DA-W-0005','DA-W-0006','DA-W-0007','DA-W-0008','DA-W-0010','DA-W-0033','DA-W-0034','DA-W-0036','DA-W-0037','DA-W-0038','DA-W-0040','DA-W-0042','DA-W-0044','DA-W-0045','DA-W-0046','DA-W-0048','DA-W-0050','DA-W-0051']
def run(root:pathlib.Path,raw:bytes):
    if hashlib.sha256(raw).hexdigest()!=SHA256:raise ValueError('Pinned source integrity mismatch')
    groups=json.loads(raw);works=json.loads((root/'data/deep_crosswalk_100_v0.6.json').read_text())['records'];results=[]
    for work in works:
        if work['work_id'] not in FLAGGED:continue
        uid=re.sub(r'\s+','',work['canonical_ids']['suttacentral']).lower()
        full=set();similar=set();segments=[];evidence=[]
        for index,group in enumerate(groups):
            tokens=group.get('parallels',[])
            if uid not in tokens:continue
            evidence.append({'json_pointer':f'/{index}/parallels','tokens':tokens})
            for token in tokens:
                target=token.lstrip('~')
                if target==uid:continue
                relation='resembling' if token.startswith('~') else 'full'
                if '#' in target:segments.append({'target_with_locator':target,'source_relation':relation})
                else:(similar if relation=='resembling' else full).add(target)
        if not evidence:raise ValueError('No unmarked anchor group for '+uid)
        if full&similar:raise ValueError('Unresolved source conflict for '+uid)
        old=work['typed_relations']['suttacentral_work_level']
        results.append({'work_id':work['work_id'],'suttacentral_id':uid,'status':'source_encoding_checked','relations':{'full':sorted(full),'resembling':sorted(similar),'mentions':old.get('mentions',[]),'retells':old.get('retells',[])},'segment_relations':segments,'source_url':SOURCE,'source_groups':evidence,'old_overlap_count':len(set(old.get('full',[]))&set(old.get('resembling',[]))),'summary_zh':'已按官方分组与~标记重建完整/近似平行，去除组间误推；段落关系单列。','limits_zh':'仅核对本次快照的parallels编码；mentions/retells保留旧值，未独立复核。没有逐段校勘，也不等于两部文本完全相同。'})
    assert len(results)==18
    data={'version':'0.8','reviewed_at':'2026-09-19','source_commit':COMMIT,'source_sha256':SHA256,'source_url':SOURCE,'method':'Use only official parallels groups where the queried exact work UID is unmarked. Unmarked partners = full; ~ partners = resembling. Do not take transitive closure or generate relations between two marked neighbours. Preserve # locators separately.','source_interpretation_reference':'https://suttacentral.net/introduction','scope':'Correct source-encoding/category duplication in 18 flagged Crosswalks; not an independent scholarly review.','counts':{'reviewed_works':len(results),'old_overlapping_targets':sum(r['old_overlap_count'] for r in results),'new_overlapping_targets':0,'work_level_full_relations':sum(len(r['relations']['full']) for r in results),'work_level_resembling_relations':sum(len(r['relations']['resembling']) for r in results),'segment_relations':sum(len(r['segment_relations']) for r in results)},'records':results}
    out=root/'data/parallel_review_v0.8.json';out.write_text(json.dumps(data,ensure_ascii=False,indent=2))
    print(json.dumps(data['counts'],ensure_ascii=False))
    return data
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source');ap.add_argument('--root',default=str(pathlib.Path(__file__).resolve().parents[1]));args=ap.parse_args()
    if args.source:raw=pathlib.Path(args.source).read_bytes()
    else:
        with urllib.request.urlopen(urllib.request.Request(URL,headers={'User-Agent':'DharmaAtlas-RelationReview/0.8'}),timeout=30) as response:raw=response.read(2000000)
    run(pathlib.Path(args.root),raw)
