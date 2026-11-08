"""Render protected source pages for image/text verification; no OCR or generated enhancement."""
from pathlib import Path
import json
import sys
root=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root/'tools'))
sys.path.insert(0,str(root/'work/pdf-tools'))
import dossier as d
import pymupdf

ds=d.Dataset(root)
items=d.load_json(root/'work/baseline-acquisitions.json')
out=root/'derived/frames/newspaper-pages';out.mkdir(parents=True,exist_ok=True)
manifest={'method':'Mechanical PDF page rendering; no OCR or enhancement','pymupdf_version':pymupdf.VersionBind,'python':sys.version,'items':[]}
for item in items:
 asset=ds._verify_asset(item['asset_id'],True)
 path=ds.resolve(asset['storage'])
 if item['key']=='sun_times':
  manifest['items'].append({**item,'original_image':str(path),'input_sha256':asset['sha256']})
  continue
 doc=pymupdf.open(path)
 pages=[]
 for index,page in enumerate(doc):
  text=page.get_text()
  if item['key']=='tribune' or 'headroom' in text.lower():
   dest=out/(item['asset_id']+f'-page-{index+1}.png')
   page.get_pixmap(dpi=160,alpha=False).save(dest)
   pages.append({'page_number':index+1,'output':dest.relative_to(root).as_posix(),**d.hash_file(dest)})
 manifest['items'].append({**item,'input_sha256':asset['sha256'],'page_count':len(doc),'rendered_pages':pages})
(root/'work/rendered-scans.json').write_bytes(d.json_bytes(manifest))
print(json.dumps(manifest,indent=2))
