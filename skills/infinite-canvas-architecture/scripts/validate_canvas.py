import argparse
import json
from pathlib import Path
from canvas_model import normalize

def main():
    p=argparse.ArgumentParser(description='Validate architecture scene references and geometry, not its architectural claims.')
    p.add_argument('scene',type=Path);args=p.parse_args()
    try:
        scene,warnings=normalize(json.loads(args.scene.read_text(encoding='utf-8-sig')))
    except (ValueError,OSError,json.JSONDecodeError) as e:
        p.exit(1,f'INVALID: {e}\n')
    print(json.dumps({'valid':True,'boards':len(scene['boards']),'nodes':len(scene['nodes']),'relationships':len(scene['edges']),'warnings':warnings},ensure_ascii=False))

if __name__=='__main__':main()
