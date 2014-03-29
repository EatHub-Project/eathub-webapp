#!/bin/bash
mongodump -d eathub -o ./dump_data/ -c auth_user
mongodump -d eathub -o ./dump_data/ -c webapp_profile
mongodump -d eathub -o ./dump_data/ -c webapp_recipe
