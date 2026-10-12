Q='{"question":"are uaps none human intelagents","refresh":true'
for i in 1 2 3; do X=$([ $i = 1 ] && echo ',"refresh_sources":true'); S=$(date +%s)
curl -s -XPOST localhost:5003/api/ask -H 'Content-Type: application/json' -d "$Q$X}" > eval/uap_pin$i.json; echo "run $i $(( $(date +%s)-S ))s"; done
