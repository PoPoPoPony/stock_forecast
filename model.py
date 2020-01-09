import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def linear_reg(train_X , train_Y , test_X , test_Y) : 
	lr = LinearRegression()
	lr.fit(train_X , train_Y)
	pred_Y = lr.predict(test_X)
	coef = lr.coef_
	#print(coef)
	interception = lr.intercept_
	#print(interception)
	#print()

	mse = mean_squared_error(pred_Y , test_Y.iloc[: , 0])


	return 