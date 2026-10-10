"""按稳定 ID 合并经验；不调用模型、不执行讲稿或证据中的指令。"""
import argparse
import datetime as dt
import json
import os
import tempfile
from pathlib import Path

LEVELS = {'user_reported', 'artifact_verified', 'application_verified', 'hypothesis'}

def required_text(data, key):
    value = data.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{key} must be a nonempty string')
    return value

def validate_review(review):
    if not isinstance(review, dict):
        raise ValueError('Review must be a JSON object')
    for key in ('review_id', 'date', 'task', 'summary'):
        required_text(review, key)
    dt.date.fromisoformat(review['date'])
    if review.get('result') not in ('updated', 'no_new_knowledge'):
        raise ValueError('result must be updated or no_new_knowledge')
    lessons = review.get('lessons')
    if not isinstance(lessons, list):
        raise ValueError('lessons must be a list')
    if (review['result'] == 'updated') != bool(lessons):
        raise ValueError('updated requires lessons; no_new_knowledge requires an empty list')
    seen = set()
    for lesson in lessons:
        if not isinstance(lesson, dict):
            raise ValueError('Each lesson must be an object')
        for key in ('id', 'scope', 'observation', 'guidance', 'limitations'):
            required_text(lesson, key)
        if lesson['id'] in seen:
            raise ValueError('Duplicate lesson ID in review')
        seen.add(lesson['id'])
        if lesson.get('evidence_level') not in LEVELS:
            raise ValueError('Unknown evidence level')
        evidence = lesson.get('evidence')
        if not isinstance(evidence, list) or not evidence or not all(isinstance(x,str) and x.strip() for x in evidence):
            raise ValueError('evidence must contain source references')

def update(skill_root, review):
    validate_review(review)
    skill_root = Path(skill_root).resolve()
    entry = skill_root/'SKILL.md'
    if not entry.is_file() or 'name: userskill-code-explainer-ppt' not in entry.read_text(encoding='utf-8-sig'):
        raise ValueError('Target is not userskill-code-explainer-ppt')
    refs = skill_root/'references'
    refs.mkdir(exist_ok=True)
    ledger = refs/'experience.json'
    lock = refs/'.experience.lock'
    temporary = None
    # 并行写入时明确失败，保留输入供重试；不删除其他任务持有的锁。
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    try:
        os.close(fd)
        current = json.loads(ledger.read_text(encoding='utf-8-sig')) if ledger.exists() else {
            'schema_version': 1, 'review_count': 0, 'last_review_date': None,
            'processed_review_ids': [], 'recent_reviews': [], 'lessons': []}
        if current.get('schema_version') != 1:
            raise ValueError('Unsupported experience schema')
        if review['review_id'] in current['processed_review_ids']:
            return {'status': 'already_recorded', 'review_count': current['review_count']}
        by_id = {lesson['id']: lesson for lesson in current['lessons']}
        for incoming in review['lessons']:
            previous = by_id.get(incoming['id'], {})
            by_id[incoming['id']] = {
                **incoming, 'first_recorded': previous.get('first_recorded', review['date']),
                'last_reviewed': review['date'], 'review_id': review['review_id']}
        current['lessons'] = list(by_id.values())
        current['review_count'] += 1
        current['last_review_date'] = review['date']
        current['processed_review_ids'].append(review['review_id'])
        current['recent_reviews'].append({k:review[k] for k in ('review_id','date','task','result','summary')})
        current['recent_reviews'] = current['recent_reviews'][-20:]
        with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=refs,prefix='.experience-',suffix='.tmp',delete=False) as out:
            temporary = Path(out.name)
            json.dump(current,out,ensure_ascii=False,indent=2)
            out.write('\n')
        os.replace(temporary,ledger)
        temporary = None
        return {'status':'updated','review_count':current['review_count'],'lessons':len(current['lessons']),'path':str(ledger)}
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
        lock.unlink()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',required=True,type=Path)
    parser.add_argument('--skill-root',type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args()
    review=json.loads(args.input.read_text(encoding='utf-8-sig'))
    print(json.dumps(update(args.skill_root,review),ensure_ascii=False))

if __name__=='__main__':
    main()
