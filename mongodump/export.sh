OUT_DIR="exported_json"
for col in "webapp_recipe" "webapp_profile" "auth_user" "webapp_food_type" "webapp_language" "webapp_special_condition" "webapp_temporality"
do
  mongoexport -d eathub -c $col -o $OUT_DIR/$col.json.tmp --jsonArray
  cat $OUT_DIR/$col.json.tmp | python -m json.tool > $OUT_DIR/$col.json
  rm $OUT_DIR/$col.json.tmp
done

# La colección de imágenes la exporta con una query condicional
col="ajax_uploadedimage"
mongoexport -d eathub -c $col -o $OUT_DIR/$col.json.tmp --jsonArray -q '{image: {$regex: ".+\.persist\..+"}}'
cat $OUT_DIR/$col.json.tmp | python -m json.tool > $OUT_DIR/$col.json
rm $OUT_DIR/$col.json.tmp
