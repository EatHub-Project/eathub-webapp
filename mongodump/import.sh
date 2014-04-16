OUT_DIR="exported_json"
for col in "webapp_recipe" "webapp_profile" "auth_user"
do
  mongoimport -d eathub -c $col --file $OUT_DIR/$col.json --drop --jsonArray
done
