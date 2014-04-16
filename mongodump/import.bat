@echo off

set OUT_DIR=exported_json

for %%x in (webapp_recipe, webapp_profile, auth_user, ajax_uploadedimage) do (
  mongoimport -d eathub -c %%x --file %OUT_DIR%/%%x.json --drop --jsonArray
)
