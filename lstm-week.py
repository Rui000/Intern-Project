# -*- coding: utf-8 -*-

import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cross_validation import train_test_split
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from numpy import concatenate
import math
#dateparse = lambda dates:pd.datetime.strptime(dates,'%Y-%m-%d')
#df= pd.read_csv('result.csv',parse_dates=['date'],index_col='date',date_parser=dateparse)

df = pd.read_csv('08-12week.csv',encoding='utf-8',header = 0,index_col=0)
print df.head()
print df.shape
#del df[u'销售日期']
df = df.drop([u'销售日期'], axis=1)
#print df.head()
df = df.fillna(0)

dd = df[u'数量']
del df[u'数量']
df[u'week_sal'] = dd
print df.head()

values = df.head(52).values
print values


'''
#画线图看特征趋势
groups = range(11,12)
i = 1
plt.figure()
for group in groups:
    plt.subplot(len(groups),1,i)
    plt.plot(values[:,group])
    plt.title(df.columns[group])
    i+=1
plt.show()

'''

values = values.astype('float32')

scaler = MinMaxScaler(copy=False,feature_range = (0,1))

print scaler

scaled = scaler.fit_transform(values)
#print scaled

x = scaled[:,:11]
y = scaled[:,11]


#x = df.iloc[:,:13]
#y = df.iloc[:,14]

train_X, test_X, train_y, test_y = train_test_split(x, y, test_size = 0.3)

train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)


# design network
model = Sequential()
model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam')
# fit network
history = model.fit(train_X, train_y, epochs=50, batch_size=72, validation_data=(test_X, test_y), verbose=2, shuffle=False)
# plot history
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='test')
plt.legend()
plt.show()

# design network
model = Sequential()
model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))
model.add(Dense(1))
model.compile(loss='mae', optimizer='adam')
# fit network
history = model.fit(train_X, train_y, epochs=50, batch_size=74, validation_data=(test_X, test_y), verbose=2, shuffle=False)
# plot history
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='test')
plt.legend()
plt.show()


yhat = model.predict(test_X)
#print 'yhat',yhat.shape
test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))
#print test_X,test_X.shape


inv_yhat = concatenate((test_X[:, 0:],yhat), axis=1)
inv_yhat = scaler.inverse_transform(inv_yhat)
inv_yhat = inv_yhat[:,11]

print 'yhat:',inv_yhat


test_y = test_y.reshape((len(test_y), 1))
inv_y = concatenate((test_X[:, 0:],test_y), axis=1)
inv_y = scaler.inverse_transform(inv_y)
inv_y = inv_y[:,11]
print 'y:',inv_y

rmse = math.sqrt(mean_squared_error(inv_y, inv_yhat))
print 'Test RMSE: %.3f' % rmse



j = 0
for i in inv_y:
    if (i == 0):
        j+=1

if (j==0):#说明实际销量值中没有为0 的值
    error = sum(abs((inv_yhat - inv_y) / inv_yhat) * 100) / len(inv_y)
    print 'test error: ', error
else:
    error = sum(abs((inv_yhat-inv_y)/inv_y)*100)/len(inv_y)
    print 'test error: ', error





