"""Extract qualified-lift frames from the matching nominal video."""
from pathlib import Path
import json
import imageio.v2 as io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
base=Path(__file__).resolve().parent
run=base.parent/'handoff_review/nominal_left'
summary=json.loads((run/'summary.json').read_text())['profiles'][0]
events=[e for e in summary['events'] if e['event']=='lift_qualified']
reader=io.get_reader(run/'compact/episode.mp4')
fig,axes=plt.subplots(2,2,figsize=(10,8),layout='constrained')
for ax,event in zip(axes.flat,events):
    t=event['time_s']+.02
    ax.imshow(reader.get_data(round(t/.02)-1));ax.axis('off')
    ax.set_title(f"{event['foot']} lift, t={t:.2f}s")
reader.close()
fig.suptitle('Four nominal scripted lifts; simulation only, target distance unmet')
fig.savefig(base/'video_frames.png',dpi=140)
plt.close(fig)
