from pathlib import Path
import sys,json,argparse
root=Path(__file__).resolve().parents[2];sys.path.insert(0,str(root/'tools'));sys.path.insert(0,str(root/'work/pdf-tools'))
import dossier as d
import pymupdf
p=argparse.ArgumentParser(description='Reproduce protected record pages into a new output directory');p.add_argument('--output',required=True);args=p.parse_args()
out=root/args.output;out.mkdir(parents=True,exist_ok=False)
ds=d.Dataset(root);items=[{'asset_id':x} for x in ['AST-0011','AST-0012']];manifest={'method':'Mechanical 160dpi PDF page render; alpha=False; no OCR or enhancement','python':sys.version,'pymupdf_version':pymupdf.VersionBind,'settings':{'dpi':160,'alpha':False},'items':[]}
for item in items:
 asset=ds._verify_asset(item['asset_id'],True);doc=pymupdf.open(ds.resolve(asset['storage']));pages=[]
 for n,page in enumerate(doc):
  p=out/(item['asset_id']+'-page-'+str(n+1)+'.png');page.get_pixmap(dpi=160,alpha=False).save(p)
  pages.append({'page_number':n+1,'output':p.relative_to(root).as_posix(),**d.hash_file(p)})
 manifest['items'].append({**item,'input_sha256':asset['sha256'],'page_count':len(doc),'rendered_pages':pages})
(out/'manifest.json').write_bytes(d.json_bytes(manifest));print(json.dumps({'path':str(out/'manifest.json'),'pages':sum(len(i['rendered_pages']) for i in manifest['items'])}))
