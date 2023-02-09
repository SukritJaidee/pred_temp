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
|main_pro.py|<p><a href="https://github.com/SukritJaidee/pred_temp/blob/main/main_pro.py">main_pro.py</a></p>| โค้ดนี้ไม่ได้มีการใส่ schedule ให้รันทุกชั่วโมง เป็นการรันครั้งเดียว ณ เวลานั้น  |
|run_schedule.py|<p><a href="https://github.com/SukritJaidee/pred_temp/blob/main/run_schedule.py">run_schedule.py</a></p>| เป็นการรันแบบ schedule ทุกๆชั่วโมงโดยใข้ schedule package โปรแกรมถูกตั้งให้รันทุกๆชั่วโมงในนาทีที่ 5 เข่น 9.05, 10.05|	
|run_schedule_v1.py|<p><a href="https://github.com/SukritJaidee/pred_temp/blob/main/run_schedule_v1.py">run_schedule_v1.py</a></p>| เป็นการรันแบบ schedule ทุกๆชั่วโมงโดยใข้ BlockingScheduler package|	
|run_schedule_v2.py|<p><a href="https://github.com/SukritJaidee/pred_temp/blob/main/run_schedule_v2.py">run_schedule_v2.py</a></p>| เป็นการรันแบบ schedule ทุกๆชั่วโมงโดยใข้ timedelta package|	
|run_schedule_v3.py|<p><a href="https://github.com/SukritJaidee/pred_temp/blob/main/run_schedule_v3.py">run_schedule_v3.py</a></p>| เป็นการรันแบบ schedule ทุกๆชั่วโมงโดยใข้วิธีการเปรียบเทียบ string datetime|	

5. ข้อมูลความเร็วในการรันโมเดล

	| CPU | Time-consuming | Code |
	| :---:|:---:|:---: |
	| Intel(R) Core(TM) i7-10750H </br> CPU@2.60GHz 2.59GHz(pycaret)|31.46|Main_pro|
	| Google Colab (pycaret)| 56.28|Main_pro|
	| Google Colab (keras-no gpu)| 48.32|Main_pro|
	| Google Colab (keras gpu)| 43.67|Main_pro|

	- รายละเอียดโปรแกรม
	- เอาต์พุตของโปรแกรม
	- ประกอบไปด้วย 2 ไพล์ได้แก่ 
	- data_ddmmyy_hhmm_data.csv ไพล์นี้ประกอบไปด้วย 6 คอลัมน์ ได้แก่ 
		1. latitude
		2. longitude 
		3. prediction(predicted temperature)
		4. tc (tmd forecast temperature)
		5. temperature (ibm temperature)
		6. datetime
	- data_ddmmyy_hhmm_info.csv ไพล์นี้ประกอบไปด้วย 4 คอลัมน์ ได้แก่ 
		1. datetime
		2. start_compute(เวลาที่เริ่มต้นคำนวณ), 
		3. end_compute (เวลาที่ใช้จนคำนวณเสร็จสิ้น)

6. Resources
	- My GitHub <a href="https://github.com/SukritJaidee/pred_temp">Click here</a>
	- ผลการรันโปรแกรม (Historical data)  https://drive.google.com/drive/folders/1IjGllgAneG-dWDKNAOAu-E80tBzgORRw?usp=sharing

7. การรันโปรแกรมบน google colab
	- ดาวน์โหลดไพล์จาก https://github.com/SukritJaidee/pred_temp
	- Open google colab จาก link ในตารางข้างล่าง
	- <b><strong>ตาราง program link ที่รันจาก google colab</strong></b>
	
	| ชื่อไพล์ | ลิ้ง | หมายเหตุ |
	| :---:|:---:|:--- |
	| weather_submit_v1_04025566_1250.ipynb|<p><a href="https://colab.research.google.com/drive/1hSSRyLhanIMrE4L9xIknK1uW0atAmFT_?usp=sharing">weather_submit_v1_04025566_1250.py</a></p>| - Code นี้ไม่ได้มีการใส่ schedule ให้รันทุกชั่วโมง เป็นการรันครั้งเดียว ณ เวลานั้น <br> - เพิ่มการ predict ด้วย keras model เพื่อลดเวลาการประมวลผล <br> - ใช้ crontab|
	| weather_schedule_v3_07022566_0949.ipynb|<p><a href="https://colab.research.google.com/drive/1njNxGtyAwKQsiRqt9ypwwqW58B_iUfGk?usp=sharing">weather_schedule_v3_07022566_0949.py</a></p>| - เป็นการรันแบบ schedule ทุกๆชั่วโมงโดยใข้ BlockingScheduler package <br> - เพิ่มการ predict ด้วย keras model เพื่อลดเวลาการประมวลผล <br>- running <br>|
	| Google Colab (keras-no gpu)| 48.32|Main_pro|
	| Google Colab (keras gpu)| 43.67|Main_pro|	