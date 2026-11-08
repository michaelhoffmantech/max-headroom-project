from pathlib import Path
import sys,json
root=Path.cwd();sys.path.insert(0,str(root/'tools'));sys.path.insert(0,str(root/'work/pdf-tools'))
import dossier as d
import pymupdf
out=root/'derived/frames/records-pages';out.mkdir(parents=True,exist_ok=True)
ds=d.Dataset(root);items=d.load_json(root/'work/records-acquisitions.json');manifest={'method':'Mechanical 160dpi PDF page render; alpha=False; no OCR or enhancement','python':sys.version,'pymupdf_version':pymupdf.VersionBind,'settings':{'dpi':160,'alpha':False},'items':[]}
for item in items:
 asset=ds._verify_asset(item['asset_id'],True);doc=pymupdf.open(ds.resolve(asset['storage']));pages=[]
 for n,page in enumerate(doc):
  p=out/(item['asset_id']+'-page-'+str(n+1)+'.png');page.get_pixmap(dpi=160,alpha=False).save(p)
  pages.append({'page_number':n+1,'output':p.relative_to(root).as_posix(),**d.hash_file(p)})
 manifest['items'].append({**item,'input_sha256':asset['sha256'],'page_count':len(doc),'rendered_pages':pages})
(root/'work/records-rendered.json').write_bytes(d.json_bytes(manifest));print(json.dumps({'path':'work/records-rendered.json','pages':sum(len(i['rendered_pages']) for i in manifest['items'])}))
