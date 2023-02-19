## <u>The Thailand Temperature Prediction Program</u>
### Program installation process
	1. Install an Anaconda environment.
		- conda create --name yourenvname python=3.8 : Ex. conda create --name pycaret_v1 python=3.8
	2. Activate the CONDA environment
		- conda activate yourenvname
	3. Install the PyCaret library (optional)
		- pip install pycaret (stable version)
		- pip install --pre pycaret (new version/developer version)
		- pip install --pre pycaret[full] (full package developer version)
	4. Create notebook kernel (optional) 
		- python -m ipykernel install --user --name yourenvname --display-name "display-name"	
### Install packages	
	- pip install -q meteostat
	- pip install -q mercantile
	- pip install -q mpmath
	- pip install -q APScheduler==3.0.0 (There is no need to install the library when using Linux crontab.)
	- pip install tensorflow-gpu
### How to run the program
	- cd  pred_temp/
	- python env_test.py 
	
### Source code
<b><ins>Table1 Python files</ins></b>
| **Link** | **Note** |
| -------- | -------- |
|<p><a href="https://github.com/SukritJaidee/pred_temp/blob/main/main_pro.py">main_pro.py</a></p>| for linux crontab  |
|<p><a href="https://github.com/SukritJaidee/pred_temp/blob/main/run_schedule.py">run_schedule.py</a></p>| It is run on a schedule every hour by using the schedule package. The program is set to run in the 5th minute of every hour, for example, at 9.05 and 10.05.|	
|<p><a href="https://github.com/SukritJaidee/pred_temp/blob/main/run_schedule_v1.py">run_schedule_v1.py</a></p>| It is run on a schedule every hour using the <ins>**BlockingScheduler**</ins> package.|	
|<p><a href="https://github.com/SukritJaidee/pred_temp/blob/main/run_schedule_v2.py">run_schedule_v2.py</a></p>| It is run on a schedule every hour using the <ins>**timedelta package**</ins>.|
|<p><a href="https://github.com/SukritJaidee/pred_temp/blob/main/run_schedule_v3.py">run_schedule_v3.py</a></p>| It runs a schedule every hour using a string datetime comparison method.|	

### My Google colab Code
<b><ins>Table2 My Google colab Code</ins></b>
| **Google colab file** | **Note** |
|:---|:--- |
|<p><a href="https://colab.research.google.com/drive/1hSSRyLhanIMrE4L9xIknK1uW0atAmFT_?usp=sharing">**weather_submit_v1_04025566_1250.ipynb**</a></p>|for linux crontab|
|<p><a href="https://colab.research.google.com/drive/1njNxGtyAwKQsiRqt9ypwwqW58B_iUfGk?usp=sharing">**weather_schedule_v3_07022566_0949.ipynb**</a></p>| It is run on a schedule every hour using the <ins>**BlockingScheduler**</ins> package|
|<p><a href="https://colab.research.google.com/drive/1Hph2GJnLzXHbnmkrJTeFBiLE65w3ygmc?usp=sharing">**weather_schedule_v2_07022566_1228.ipynb**</a></p>| It is run on a schedule every hour using the <ins>**timedelta package**</ins>.|	
|<p><a href="https://colab.research.google.com/drive/1CroHoo--kFfY_oxd4pHTarCiaBKOcTLQ?usp=sharing">**weather_schedule_v4_07022566_2566.ipynb**</a></p>| It runs a schedule every hour using a string datetime comparison method.|	
|<p><a href="https://colab.research.google.com/drive/18C98Jv7HjBfLt7JonwTJtRQrd2fqQVes?usp=sharing">**weather_schedule_v5_17012566_2243.ipynb**</a></p>|It is run on a schedule every hour by using the schedule package. The program is set to run in the 5th minute of every hour, for example, at 9.05 and 10.05.|
|<p><a href="https://colab.research.google.com/drive/1TdUTEecJV7iTOKKQOv5uH6tRip7Mh92_?usp=sharing">**weather_backup_17012566_2119.ipynb**</a></p>|Backup code|
|<p><a href="https://colab.research.google.com/drive/16in5kpmcy4t-colTDOi7eOKunMI5tv2k?usp=sharing">**Training_04022566_2028.ipynb**</a></p>| Main Code for trainng|
|<p><a href="https://colab.research.google.com/drive/1c8-_nqiMsFPpslSEmVZNBrypx9iw4N93?usp=sharing">**result_visualization.ipynb**</a></p>| result visualization|

### Speed performance
<b><ins>Table3 Speed Performance</ins></b>
| **CPU** | **Time-consuming** | **Code** |
|:---:|:---:|:---: |
| Intel(R) Core(TM) i7-10750H </br> CPU@2.60GHz 2.59GHz(pycaret)|31.46|Main_pro|
| Google Colab (pycaret)| 56.28|Main_pro|
| Google Colab (keras-no gpu)| 48.32|Main_pro|
| Google Colab (keras gpu)| 43.67|Main_pro|

### Program Description
	- The output of the program consists of two files:
		1. data_ddmmyy_hhmm_data.csv: This file consists of 6 columns:
			1. latitude,
			2. longitude,
			3. prediction(predicted temperature),
			4. tc (tmd forecast temperature),
			5. temperature (ibm temperature),
			6. datetime
		2. data_ddmmyy_hhmm_info.csv This file consists of 4 columns:
			1. datetime,
			2. start_compute(Calculation start time), 
			3. end_compute (Time taken to complete the calculation)
### Result
<p align="center"></p>
<table>
    <thead>
        <tr>
            <th align="center">MSE Error</th>
            <th align="center">Compare the values from each model</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="center"><img src="https://lh6.googleusercontent.com/9AVa0E2Prsctlfxa67_uoD3MQALGT5bF5Q_hBlr1noJ1mlKiz83Z5xHI4rQFT1FOfVo=w2400" width="400" high="300" style="display: margin: 0 auto; max-width: 400px"></td>
            <td align="center"><img src="https://lh4.googleusercontent.com/rySKw7SUG6AicwbMqcFQ16FH9Nc0IYvonubmdVQN6zg4KKcoPMirUsW9fRhILRHz0o8=w2400" width="400" high="300" style="display: margin: 0 auto; max-width: 400px"></td>
        </tr>
        <tr>
            <td align="center"><img src="https://lh5.googleusercontent.com/R6ytHZu6ekc1GtoSYcPAD5nd2bhr4Ly1JrzD4l68hI4RotHBb4u9rJths_upmnJ-xpc=w2400" width="600" high="300" style="display: margin: 0 auto; max-width: 600px"></td>
            <td align="center"><img src="https://lh3.googleusercontent.com/kq-3zCN315c5u92u8AxjTW37HntpIw55DnvrxVxzGwkQV5NCsGEoN8zjgeE0tUA1gcM=w2400" width="600" high="300" style="display: margin: 0 auto; max-width: 600px"></td>
        </tr>
    </tbody>
</table>
<p></p>

### My Resources
- My Github: <a href="https://github.com/SukritJaidee/pred_temp">Click here</a>
- Result data (Historical data): <a href="https://drive.google.com/drive/folders/1IjGllgAneG-dWDKNAOAu-E80tBzgORRw?usp=sharing">Download here</a>
- Training data <a href="https://drive.google.com/file/d/1M-6o2ovKUzw2vFWTmE7T1Uo2NZPm2PK7/view?usp=sharing">Download here</a>
- Pre-trained model <a href="https://drive.google.com/file/d/1gDv4Q0msQvMPhq-3rqcTSdXqs32tGsNR/view?usp=sharing">Download here</a>
	
### Phase2
- <p><a href="https://colab.research.google.com/drive/11Ft7moDQ0XLUoUYI70bCLapZtzy3tOCI?usp=sharing">Phase2_backup_04022566_1503.ipynb</a></p>
	  
### **Thank you** 
	- Jeffrey M. Gawrych, Senior Solutions Engineer/Meteorologist, IBM Sustainability Software for sharing IBM Weather Company Data
	- Chulalongkorn university

### Reference
	- 
### Donate
- If you want to donate coffee to me, you can donate via the QR code below. </br>
	<img
	  src="https://lh6.googleusercontent.com/4Dni4jkpIs0L_iFNIC7jGFMryoqNS3E74qym_9pLkiyta5W8Jkz41yvTVqk8Nc8CxXc=w2400"
	  width="250" high="250" style="display: margin: 0 auto; max-width: 300px">
