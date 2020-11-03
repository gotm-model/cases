import argparse
import yaml
import html

parser = argparse.ArgumentParser()
parser.add_argument('out')
parser.add_argument('path', nargs='*')
args = parser.parse_args()

ntest = 0
nfailed = 0

def draw_badge(out):
    from PIL import Image, ImageDraw, ImageFont
    nscale = 2
    w, h = 180, 24
    txt = Image.new('RGB', (nscale * w, nscale * h), (200,200,200))
    d = ImageDraw.Draw(txt)
    d.ellipse([(0.2*h*nscale,0.2*h*nscale), (0.8*h*nscale,0.8*h*nscale)], fill=(255,0,0) if nfailed > 0 else (0,255,0), outline=(0,0,0), width=1)
    status = 'all %i tests succeeded' % ntest if nfailed == 0 else '%i/%i tests failed' % (nfailed, ntest)
    txt = txt.resize((w, h))
    d = ImageDraw.Draw(txt)
    d.text((1.1*h,6), status, fill=(0,0,0))
    txt.save(out)

def get_error(task):
    errors = []
    if task.get('error') is not None:
        errors.append(task.get('error_detail') or task['error'])
    else:
        for subtask in task.get('children', []):
            suberr = get_error(subtask)
            if suberr:
                errors.extend(suberr)
    return errors

def write_result(f, result, task_name):
    global ntest, nfailed
    for task in result['children']:
        if task['name'] == task_name:
            errors = get_error(task)
            success = not errors
            ntest += 1
            if not success:
                nfailed += 1
            classname = 'success' if success else 'failed'
            f.write('        <td class="%s"%s>%s</td>\n' % (classname, (' title="%s"' % html.escape('\n'.join(errors))) if errors else '', 'SUCCESS' if success else 'FAILED'))
            break
    else:
        f.write('        <td>&nbsp;</td>')

with open(args.out, 'w') as f_html:
    f_html.write("""<!DOCTYPE html>
<html>
  <head>
    <title>GOTM test case results</title>
    <style>
      document,table {
          font-family: tahoma,arial;
          font-size:11pt;
      }
      td.success {
          background-color: green;
      }
      td.failed {
          background-color: red;
      }
    </style>
  </head>
  <body>
    <table>
""")
    rownames = set()
    results = []
    for path in args.path:
        with open(path, 'r') as f:
            result = yaml.safe_load(f)
            for c in result['children']:
                rownames.add(c['name'])
            results.append(result)
    for label, key in [('GOTM version', 'gotm_commit'), ('Cases version', 'cases_commit'), ('Extra ID', 'extra_info'), ('Date and time', 'datetime'), ('Compiler', 'compiler'), ('Platform', 'platform')]:
        f_html.write('      <tr>\n')
        f_html.write('        <th>%s</th>\n' % label)
        for result in results:
            value = result.get(key)
            f_html.write('        <th>%s</th>\n' % ('' if value is None else value))
        f_html.write('      </tr>\n')
    for name in ['git', 'cmake'] + sorted([n for n in rownames if n not in ('git', 'cmake')]):
        f_html.write('      <tr>\n')
        f_html.write('        <th>%s</th>\n' % name)
        for result in results:
            write_result(f_html, result, name)
        f_html.write('      </tr>\n')
    f_html.write("""        </table>
    </body>
    </html>
    """)

draw_badge('badge.png')