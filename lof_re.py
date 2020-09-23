import numpy as np
import pandas as pd
import os
import csv
import matplotlib.pyplot as plt
from sklearn.neighbors import LocalOutlierFactor
from matplotlib.pyplot import figure

from matplotlib import font_manager, rc
font_location = "C:/Windows/Fonts/gulim.ttc"
font_name = font_manager.FontProperties(fname=font_location).get_name()
plt.rc('font',family=font_name)

def trial(year,month,day1,day2,PM):

    PM10_2019 = pd.read_excel('{year}_전국_{PM}.xlsx'.format(year=year,PM=PM))

    PM10_2019 = pd.DataFrame(PM10_2019)
    PM10_2019 = PM10_2019.set_index('측정일시')

    start_day = int('{day1}'.format(day1=day1))
    last_day = int('{day2}'.format(day2=day2))

    if month < 10 :
        mon = '0{mon}'.format(mon=month)
    else:
        mon = '{mon}'.format(mon=month)
        

    for a in range(start_day, last_day):

        if a < 10:
            a = '0{b}'.format(b=a)
        else:
            a = '{b}'.format(b=a)

        for i in range(0, 24) :
            if i<10:
                hourly = "{year}-{month}-{day} 0{hour}:00:00".format(year=year,month=mon,hour=i,day=a)
            else: 
                hourly = "{year}-{month}-{day} {hour}:00:00".format(year=year,month=mon,hour=i,day=a)

            test = pd.DataFrame(PM10_2019.loc["{time}".format(time=hourly)])
            test = test
            test = test.fillna(test.mean())
            index_num = np.linspace(1,len(test),len(test))

            station = pd.DataFrame(test.index)
            station = station.to_numpy()
            test = test.to_numpy()

            X = np.c_[index_num, test]

            n_outliers = len(index_num)
            ground_truth = np.ones(len(X), dtype=int)
            ground_truth[-n_outliers:] = -1

            clf = LocalOutlierFactor(n_neighbors=20, contamination=0.1)

            y_pred = clf.fit_predict(X)
            n_errors = (y_pred != ground_truth).sum()
            X_scores = abs(clf.negative_outlier_factor_)


            #---------------------------------------------------
            figure(num=None, figsize=(20, 10), dpi=80, facecolor='w', edgecolor='k')
            plt.title("{time} {PM} Conc. (unit: ㎍/㎥)".format(time=hourly,PM=PM), fontsize=30)
            plt.ylim(0, 1500)
            plt.yticks(fontsize=20)
            plt.ylabel('Local Outlier Factors'.format(PM=PM), fontsize=30)
            #plt.ylabel('PM Conc. (unit: ㎍/㎥)'.format(PM=PM), fontsize=30)
            plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom=False,      # ticks along the bottom Edge are off
            top=False,         # ticks along the top Edge are off
            labelbottom=False) # labels along the bottom Edge are off
            plt.xlabel('Station', fontsize=30)
            plt.scatter(X[:, 0], test, color='b', s=3.5)
            
            #radius = (X_scores.max() - X_scores) / (X_scores.max() - X_scores.min()) #오홍 minmax scaling으로 radius를 정햇네
            
            #plt.scatter(X[:, 0], X[:, 1], s=1000 * radius, edgecolors='r',
            #        facecolors='none', label='Outlier scores')
            n=np.copy(X_scores)
            n[n<1.5]=np.nan
            n=np.round(n,2)
            for y, txt in enumerate(n):
                if np.isnan(txt):continue
                txt_int = float(txt)
                if txt_int < 1.6 :
                    plt.annotate(txt, xy=(X[y,0], X_scores[y]), xytext=(X[y,0]+5, X_scores[y]+2), arrowprops=dict(arrowstyle='->',color='r'),fontsize=30)
                elif txt_int < 2.0 :
                    plt.annotate(txt, xy=(X[y,0], X_scores[y]), xytext=(X[y,0]+7, X_scores[y]+3), arrowprops=dict(arrowstyle='->',color='r'),fontsize=30)
                else:
                    plt.annotate(txt, xy=(X[y,0], X_scores[y]), xytext=(X[y,0]+5, X_scores[y]+2), arrowprops=dict(arrowstyle='->',color='r'),fontsize=30)
            
            #legend = plt.legend(loc='upper left')
            plt.savefig('D:/OneDrive - inu.ac.kr/대기연구실/201905 미세먼지 재난사태 선포/논문 그림 데이터/지역별 데이터 정리/LOF/{year}_{month}_{day}_{hour}_{PM}.png'.format(year=year,month=mon,hour=i,day=a,PM=PM))
            #print('save')
            #plt.show()
            plt.close()

# edit test branch 1
            
            
#trial(2017,5,5,6,'PM10') # year, month, start day, last day

#trial(2017,5,5,8,'PM10') # year, month, start day, last day
#trial(2017,5,5,8,'PM25') # year, month, start day, last day

#trial(2018,11,26,31,'PM10') # year, month, start day, last day
#trial(2018,11,26,31,'PM25') # year, month, start day, last day

#trial(2019,1,1,4,'PM10') # year, month, start day, last day
#trial(2019,1,1,4,'PM25') # year, month, start day, last day

#trial(2019,2,27,29,'PM10') # year, month, start day, last day
#trial(2019,2,27,29,'PM25') # year, month, start day, last day

#trial(2019,3,6,8,'PM10') # year, month, start day, last day
trial(2019,3,6,8,'PM25') # year, month, start day, last day
