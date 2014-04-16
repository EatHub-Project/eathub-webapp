OUT_DIR="exported_json"
for col in "webapp_recipe" "webapp_profile" "auth_user"
do
  mongoexport -d eathub -c $col -o $OUT_DIR/$col.json.tmp --jsonArray
  cat $OUT_DIR/$col.json.tmp | python -m json.tool > $OUT_DIR/$col.json
  rm $OUT_DIR/$col.json.tmp
done
