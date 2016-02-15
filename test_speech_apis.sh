run_cmd() {
  echo $1 $2
  T="$(date +%s)"
  if [ $1 == "watson" ];then
    curl -u 3a223acf-c31e-403d-bca0-da88c124a99a:aEzxZ8KGNDVw -X POST --header "Content-Type: audio/flac" --header "Transfer Encoding: chunked" --data-binary @$2 "https://stream.watsonplatform.net/speech-to-text/api/v1/recognize?continuous=true" > temp
  elif [ $1 == "google" ];then
    curl -X POST --header "Content-Type: audio/x-flac; rate=44100" --header "Transfer-Encoding: chunked" --header "User-agent: Chrome/47.0.2526.106" --data-binary @$2 "https://www.google.com/speech-api/full-duplex/v1/up?pair=14567389246789134&output=json&lang=en-us&client=chromium&key=AIzaSyA38WJIWToFtEE3t3ExicjPtM55_rek-j0" > temp
  fi
  T="$(($(date +%s)-T))"

  python process_json.py temp results.txt $2 $1 

  echo "$1: ${T} seconds" >> time_results.txt
}

FILES=/Users/pedrovmoura/Documents/Code/speech-text/audio-files/*
ABSOLUTE_PATH=/Users/pedrovmoura/Documents/Code/speech-text/audio-files
for f in $FILES
do
  base=`basename "$f"`
  filename="${base%.*}"
  filepath="${base##*.}"
  if [ $filepath != "flac" ];then
    ffmpeg -i $f -ar 44100 -f flac $ABSOLUTE_PATH/$filename.flac
    mv $f non-flac
  fi
  echo "$filename" >> time_results.txt
  run_cmd "watson" "$ABSOLUTE_PATH/$filename.flac"
  run_cmd "google" "$ABSOLUTE_PATH/$filename.flac"
  echo >> time_results.txt
done
rm temp
