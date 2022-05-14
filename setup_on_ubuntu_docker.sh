cd /w209_spring_2022_thu_4_pm_team_4_web
chmod -R 777 ./*.*
python3 -m venv myproj
./myproj/bin/activate
./ir.sh
./rd.sh &
sleep 35
jupyter notebook --no-browser --ip=0.0.0.0 --allow-root 
