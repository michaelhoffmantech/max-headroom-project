"""Reproduce CYC-0001 conservative file-context viewing derivatives. No inferred speech."""
import argparse,json,subprocess,sys,re,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
import dossier as d

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--ffmpeg',required=True);p.add_argument('--output',default='derived/frames/CYC-0001');a=p.parse_args()
 ds=d.Dataset(ROOT);cycle=ds.records()['CYC-0001'][1]
 d.require(cycle['state'] in {'active','tested','reviewed'},'analysis_state','Use command-recorded start-analysis before decoding; later reproduction retains the original verified manifest')
 ds._cycle_inputs_verified(cycle)
 out=ROOT/a.output;out.mkdir(parents=True,exist_ok=False)
 manifest={'cycle_id':cycle['id'],'started_at':d.utcnow(),'tool':{'executable':a.ffmpeg,**d.hash_file(Path(a.ffmpeg))},'version':subprocess.run([a.ffmpeg,'-version'],capture_output=True,text=True,check=True).stdout.splitlines()[0],'inputs':[],'limits':['File-relative decoded coordinates only; no broadcast timing/authenticity inference','Contact sheets reduced for viewing; final image native decoded resolution; no enhancement, deinterlacing, trimming of originals, or generative processing','Audio is decoded in the full null pass but not transcribed/listened to by this script; no disputed words asserted']}
 for ref in cycle['input_assets']:
  asset=ds._verify_asset(ref['id'],True,confirmed_before=cycle['analysis_started_at']);source=ds.resolve(asset['storage']);key=asset['id']
  entry={'asset_id':key,'source_id':asset['source_id'],'input_sha256':asset['sha256'],'commands':[],'outputs':[]}
  probe=subprocess.run([a.ffmpeg,'-hide_banner','-nostdin','-i',str(source),'-f','null','-'],capture_output=True,text=True,timeout=120)
  d.require(probe.returncode==0,'decode_failure','Full decode failed')
  duration=re.search(r'Duration: (\d+):(\d+):([\d.]+)',probe.stderr)
  d.require(duration,'duration','Container duration missing')
  seconds=int(duration[1])*3600+int(duration[2])*60+float(duration[3]);rows=math.ceil(seconds/6)
  entry['container_duration_seconds']=seconds
  jobs=[('decode.log',['-i',str(source),'-vf','blackdetect=d=0.1:pix_th=0.1:pic_th=0.98','-f','null','-'],None),
        ('contact.png',['-i',str(source),'-vf',f'fps=1,scale=320:-1,tile=6x{rows}','-frames:v','1','-update','1'], 'one-second samples from file start; row-major 6columns; empty trailing tiles are padding'),
        ('end.png',['-sseof','-3','-i',str(source),'-vf','fps=5,scale=320:-1,tile=5x3','-frames:v','1','-update','1'],'final3seconds sampled5fps; seek/decoder time alignment is approximate, not exact historical boundary'),
        ('last.png',['-i',str(source),'-an','-vf','reverse','-frames:v','1','-update','1'],'last decoded video frame from full stream reversal; native decoded resolution; avoids audio/container-tail seek ambiguity'),
        ('frames.md5',['-i',str(source),'-map','0:v:0','-an','-f','framemd5'],'all decoded video frames; unscaled checksums and timebase in header')]
  for suffix,args,notes in jobs:
   dest=out/(key+'-'+suffix);cmd=[a.ffmpeg,'-hide_banner','-nostdin',*args]
   if suffix!='decode.log':cmd.append(str(dest))
   result=subprocess.run(cmd,capture_output=True,text=True,timeout=120)
   log=dest if suffix=='decode.log' else out/(key+'-'+suffix+'.log')
   log.write_text(result.stdout+result.stderr,encoding='utf-8')
   entry['commands'].append({'arguments':cmd,'returncode':result.returncode,'log':log.relative_to(ROOT).as_posix(),**d.hash_file(log)})
   d.require(result.returncode==0,'decode_failure',str(log))
   if suffix!='decode.log':entry['outputs'].append({'path':dest.relative_to(ROOT).as_posix(),'notes':notes,**d.hash_file(dest)})
  d.require(d.hash_file(source)['sha256']==asset['sha256'],'input_changed','Acquired original changed')
  manifest['inputs'].append(entry)
 manifest['finished_at']=d.utcnow();(out/'manifest.json').write_bytes(d.json_bytes(manifest))
 print(json.dumps({'manifest':str(out/'manifest.json'),'input_count':len(manifest['inputs']),'started_at':manifest['started_at'],'finished_at':manifest['finished_at']}))
if __name__=='__main__':main()
