import argparse,json
from pathlib import Path

def audit(root):
    root=Path(root); findings=[]
    if not root.is_dir(): raise ValueError('directory not found')
    def add(code,level,detail): findings.append({'code':code,'level':level,'detail':detail})
    try:
        pkg=json.loads((root/'package.json').read_text()); assert isinstance(pkg,dict)
    except (OSError,ValueError,AssertionError): add('manifest','error','Missing or invalid package.json'); return findings
    scripts=pkg.get('scripts',{}); scripts=scripts if isinstance(scripts,dict) else {}
    for s in ('build','test','lint'):
        if not isinstance(scripts.get(s),str) or not scripts[s].strip(): add('script-'+s,'warning',f'Add or document a {s} command')
    locks=[n for n in ('package-lock.json','pnpm-lock.yaml','yarn.lock','bun.lock','bun.lockb') if (root/n).is_file()]
    if len(locks)!=1: add('lockfile','warning',f'Expected one root lockfile; found {len(locks)}')
    for name in ('README.md','.gitignore'):
        if not (root/name).is_file(): add(name,'warning',f'Missing {name}')
    deps=pkg.get('devDependencies'); deps=deps if isinstance(deps,dict) else {}
    if not (root/'tsconfig.json').exists() and 'typescript' in deps: add('typescript','warning','TypeScript declared without root tsconfig.json')
    if not isinstance(pkg.get('engines'),dict) or not pkg['engines'].get('node'): add('node-engine','note','Consider documenting supported Node runtime')
    return findings

def main():
    p=argparse.ArgumentParser(); p.add_argument('directory'); p.add_argument('--strict',action='store_true'); a=p.parse_args()
    try: results=audit(a.directory)
    except ValueError as e: p.error(str(e))
    print(json.dumps(results,indent=2)); return int(any(x['level']=='error' or a.strict and x['level']=='warning' for x in results))
if __name__=='__main__': raise SystemExit(main())
