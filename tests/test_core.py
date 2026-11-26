import unittest,tempfile,json
from pathlib import Path
from health import audit
class Test(unittest.TestCase):
 def setUp(self): self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup); self.p=Path(self.tmp.name)
 def test_missing(self): self.assertEqual(audit(self.p)[0]['level'],'error')
 def test_invalid(self): (self.p/'package.json').write_text('[]'); self.assertEqual(audit(self.p)[0]['code'],'manifest')
 def test_scripts(self): (self.p/'package.json').write_text('{}'); self.assertIn('script-test',[r['code'] for r in audit(self.p)])
 def test_clean(self):
  (self.p/'package.json').write_text(json.dumps({'scripts':{k:'true' for k in ('build','test','lint')},'engines':{'node':'>=20'}}))
  for name in ('README.md','.gitignore','package-lock.json'): (self.p/name).touch()
  self.assertEqual(audit(self.p),[])
 def test_malformed_devdeps(self):
  (self.p/'package.json').write_text('{"devDependencies":123}'); self.assertTrue(audit(self.p))
