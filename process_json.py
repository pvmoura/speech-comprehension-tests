import json
import sys

def file_to_array(filename, watson=False):
  with open(filename, "rb") as f:
    lines = [line.strip() for line in f.readlines()]
    lines = [''.join(lines)] if watson else lines
    return [ json.loads(line) for line in lines ]

def write_file(filename, arr, prefix):
  with open(filename, "a") as f:
    f.write(prefix)
    for i, line in enumerate(arr):
      f.write(str(i) + ": " + str(line) + "\n")
    f.write("\n\n")

def google_json_to_output(google_json):
  try:
    return [ line['transcript']
             for line in google_json['result'][google_json['result_index']]['alternative']
             if google_json.get('result_index') is not None]
  except Exception, e:
    print e
    return []

def watson_json_to_output(watson_json):
  try:
    return [ line['transcript']
             for alt in watson_json['results']  
             for line in alt['alternatives'] ]
  except Exception, e:
    print e
    return []

def run(infile, outfile, audiofilename, watson=False):
  out_func = google_json_to_output if not watson else watson_json_to_output
  for result in file_to_array(infile, watson):
    out_result = out_func(result)
    fn = audiofilename[audiofilename.rindex('/'):]
    fn += " Google" if not watson else " Watson"
    fn += "\n\n"
    if len(out_result) > 0:
      write_file(outfile, out_result, fn)
    else:
      write_file(outfile, out_result, fn + "NO RESULTS")

def test():
  arr = file_to_array("test")
  print 'now testing google'
  for result in arr:
    g = google_json_to_output(result)
    write_file("test_output.txt", g, "Google")
  print 'now testing watson'
  for result in file_to_array("test_watson", True):
    w = watson_json_to_output(result)
    write_file("test_output.txt", w, "Watson")

if __name__ == "__main__":
  if len(sys.argv) != 5:
    print "Usage: process_json.py infile outfile audiofilename watson|google"
    sys.exit(1)
  run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] == 'watson')
