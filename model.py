import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import gradient_boosting
from sklearn.preprocessing import PolynomialFeatures
from keras.models import Sequential
from keras.layers import Dense , Dropout
from keras import metrics

def linear_reg(train_X , train_Y , test_X , test_Y) : 
	lr = LinearRegression()
	lr.fit(train_X , train_Y)
	pred_test_Y = lr.predict(test_X)
	pred_train_Y = lr.predict(train_X)
	coef = lr.coef_
	#print(coef)
	interception = lr.intercept_
	#print(interception)
	#print()

	test_mse = mean_squared_error(pred_test_Y , test_Y.iloc[: , 0])
	train_mse = mean_squared_error(pred_train_Y , train_Y.iloc[: , 0])

	return [train_mse , test_mse]

def poly_reg(train_X , train_Y , test_X , test_Y) : 
	quadratic_featurizer = PolynomialFeatures(degree = 1)
	poly_train_X = quadratic_featurizer.fit_transform(train_X)
	poly_test_X = quadratic_featurizer.fit_transform(test_X)
	lr = LinearRegression()
	lr.fit(poly_train_X , train_Y)
	
	pred_test_Y = lr.predict(poly_test_X)
	pred_train_Y = lr.predict(poly_train_X)

	test_mse = mean_squared_error(pred_test_Y , test_Y.iloc[: , 0])
	train_mse = mean_squared_error(pred_train_Y , train_Y.iloc[: , 0])

	return [train_mse , test_mse]


def GDBT(train_X , train_Y , test_X , test_Y) : 
	gdbt = gradient_boosting.GradientBoostingRegressor(loss = "ls" , 
	learning_rate = 0.1 , 
	n_estimators = 70 , 
	criterion = "friedman_mse" , 
	max_depth = 4 , 
	warm_start = True , 
	subsample = 0.8)

	gdbt.fit(train_X , train_Y)

	pred_test_Y = gdbt.predict(test_X)
	pred_train_Y = gdbt.predict(train_X)

	test_mse = mean_squared_error(pred_test_Y , test_Y.iloc[: , 0])
	train_mse = mean_squared_error(pred_train_Y , train_Y.iloc[: , 0])

	return [train_mse , test_mse]
