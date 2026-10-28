"""Render coordinator-only Apps Script; no cloud execution, publishing or invitations."""
import argparse
from pathlib import Path
from benchmarks import quality_review as q
from benchmarks.quality_human import embed

def render(out):
 q.verify(out);packets={}
 for who in ('A','B'):
  cases=q.read(out/'packets'/f'{who}.json');packets[who]={'reviewer':who,'packet_digest':q.digest(cases),'cases':cases}
 folder=out/'forms-coordinator';folder.mkdir(exist_ok=True)
 path=folder/'Code.gs';path.write_text((q.ROOT/'benchmarks/reviewer_forms.gs').read_text().replace('__PACKETS__',embed(packets)))
 q.save(folder/'appsscript.json',{'timeZone':'Asia/Ho_Chi_Minh','runtimeVersion':'V8','oauthScopes':['https://www.googleapis.com/auth/forms']})
 q.save(folder/'manifest.json',{'source_digest':q.digest(path.read_bytes()),'packet_bindings':{k:v['packet_digest'] for k,v in packets.items()},'cloud_execution':'not executed','publish':'never automatic','source_to_inventory':'manual transcription with reviewer approval; preserve raw exports; no automated parser or human quality claims','quality_forms':'requires reviewer-approved frozen source inventory first','scope':'Google Forms access; do not grant broader scopes'})
 return path
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);print(render(p.parse_args().output.resolve()))
