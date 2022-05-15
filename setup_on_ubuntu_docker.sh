cd /w209_spring_2022_thu_4_pm_team_4_web
chmod -R 777 ./*.*
./rd.sh &
sleep 15
cd /
jupyter notebook --no-browser --ip=0.0.0.0 --allow-root 
