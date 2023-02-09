# ขั้นตอนการติดตั้งโปรแกรม predicted temperature
1. Create a conda environment 
	- conda create --name yourenvname python=3.8
	- ex. conda create --name pycaret_v1 python=3.8
2. Activate conda environment: activate environment ที่เราสร้างขึ้น
	conda activate yourenvname
	ex. conda activate pycaret_v1
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
