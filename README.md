## ขั้นตอนการติดตั้งโปรแกรม predicted temperature
1. Create a conda environment 
	- conda create --name yourenvname python=3.8
	- ex. conda create --name pycaret_v1 python=3.8
2. Activate conda environment: activate environment ที่เราสร้างขึ้น
	- conda activate yourenvname
	- ex. conda activate pycaret_v1
3. Install pycaret 
	- หากต้องการใช้ pycaret framework ในการทำนายค่า temperature หากไม่ต้องการให้ข้ามขั้นตอนที่ 3 ไป
		- pip install pycaret (ติดตั้ง version stable)
		- pip install --pre pycaret (ติดตั้ง new version/developer version แต่ unstable)
		- pip install --pre pycaret[full] (ติดตั้ง developer version แบบ full package)
4. Create notebook kernel (optional) (สร้าง notebook kernel)
	- python -m ipykernel install --user --name yourenvname --display-name "display-name"
2. ติดตั้ง package ที่จำเป็น
	- pip install -q meteostat
	- pip install -q mercantile
	- pip install -q mpmath
	- pip install -q APScheduler==3.0.0 ( หากใช้ crontab ไม่จำเป็นต้อง install the library)
	- pip install tensorflow-gpu
3. ขั้นตอนการทดสอบการติดตั้ง environment
	- cd  pred_temp/
	- python env_test.py ถ้าไม่ติด error ใดๆแปลว่า การติดตั้งสมบูรณ์
4. รันโปรแกรม
	- ตาราง Program link ที่รันจาก บนเครื่อง local/server
	
| Filename     | Link      | Note     |
| ------------- | ------------- | -------- |
| python main_pro.py          	| https://github.com/SukritJaidee/pred_temp/blob/main/main_pro.py| โค้ดนี้ไม่ได้มีการใส่ schedule ให้รันทุกชั่วโมง เป็นการรันครั้งเดียว ณ เวลานั้น|
| run_schedule.py           	| https://github.com/SukritJaidee/pred_temp/blob/main/run_schedule.py| เป็นการรันแบบ schedule ทุกๆชั่วโมงโดยใข้ schedule package โปรแกรมถูกตั้งให้รันทุกๆชั่วโมงในนาทีที่ 5 เข่น 9.05, 10.05   |	
| run_schedule_v1.py           	| https://github.com/SukritJaidee/pred_temp/blob/main/run_schedule_v1.py| เป็นการรันแบบ schedule ทุกๆชั่วโมงโดยใข้ BlockingScheduler package   |	
| run_schedule_v2.py           	| https://github.com/SukritJaidee/pred_temp/blob/main/run_schedule_v2.py| เป็นการรันแบบ schedule ทุกๆชั่วโมงโดยใข้ timedelta package   |	
| run_schedule_v3.py           	| https://github.com/SukritJaidee/pred_temp/blob/main/run_schedule_v3.py| เป็นการรันแบบ schedule ทุกๆชั่วโมงโดยใข้วิธีการเปรียบเทียบ string datetime  |	
| python main_pro.py          	| <p><a href="https://github.com/SukritJaidee/pred_temp/blob/main/main_pro.py">python</a></p>| โค้ดนี้ไม่ได้มีการใส่ schedule ให้รันทุกชั่วโมง เป็นการรันครั้งเดียว ณ เวลานั้น  |
