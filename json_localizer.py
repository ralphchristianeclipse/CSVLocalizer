import os
import sys
import csv

def start_localize_json(CURRENT_DIR, BASE_PATH, IN_PATH, OUT_PATH, LANG_KEYS):

  base_out_dir = os.path.join(BASE_PATH, OUT_PATH)
  # top most
  if not os.path.exists(base_out_dir):
      os.makedirs(base_out_dir)

  # each languages
  for lang in LANG_KEYS:
    lang_path = os.path.join(base_out_dir, "{0}/".format(lang))
    if not os.path.exists(lang_path):
      os.makedirs(lang_path)

  full_out_paths = [os.path.join(base_out_dir, "{0}/".format(langKey) + "{0}.json".format(langKey)) for langKey in LANG_KEYS]
  allwrites = [open(out_path, 'w') for out_path in full_out_paths]

  for dirname, dirnames, filenames in os.walk(os.path.join(CURRENT_DIR, IN_PATH)):

    [fwrite.write('{') for fwrite in allwrites]
    # [fwrite.write('<resources>') for fwrite in allwrites]

    for f in filenames:
      filename, ext = os.path.splitext(f)
      if ext != '.csv':
        continue
      fullpath = os.path.join(dirname, f)
      print 'Localizing: ' + filename + ' ...'

      with open(fullpath, 'rb') as csvfile:
        [fwrite.write('\n// {0} \n'.format(filename)) for fwrite in allwrites]

        reader = csv.reader(csvfile, delimiter=',')

        iterrows = iter(reader);
        next(iterrows) # skip first line (it is header).
        for row in iterrows:
          row_key = row[0]

          # comment
          if row_key[:2] == '//':
            continue

          row_values = [row[i+1] for i in range(len(LANG_KEYS))]

          # if any row is empty, skip it!
          if any([value == "" for value in row_values]):
            [fwrite.write('\n') for idx, fwrite in enumerate(allwrites)]
          else:
            [fwrite.write('\t"{key}":"{lang}",\n'.format(key=row_key, lang=row_values[idx])) for idx, fwrite in enumerate(allwrites)]
    [fwrite.write('}') for fwrite in allwrites]
  [fwrite.close() for fwrite in allwrites]
