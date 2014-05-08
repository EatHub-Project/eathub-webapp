OUT_DIR="exported_json"
for col in "webapp_recipe" "webapp_profile" "auth_user" "ajax_uploadedimage" "webapp_food_type" "webapp_language" "webapp_special_condition" "webapp_temporality"
do
  mongoimport -d eathub -c $col --file $OUT_DIR/$col.json --drop --jsonArray
done
