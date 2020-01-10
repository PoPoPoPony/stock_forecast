from sklearn.model_selection import KFold
import model
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import gradient_boosting
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
import output

def KFold_cross_validation(df_X , df_Y , n , model_flag) : 
	kf = KFold(n_splits = n , shuffle = True)
	error = []

	for train_idx , test_idx in kf.split(df_X) : 
		train_X = df_X.iloc[train_idx , :]
		train_Y = df_Y.iloc[train_idx , :]
		test_X = df_X.iloc[test_idx , :]
		test_Y = df_Y.iloc[test_idx , :]


		if model_flag == 1 : 
			error.append(model.linear_reg(train_X , train_Y , test_X , test_Y))
		
		if model_flag == 2 : 
			error.append(model.poly_reg(train_X , train_Y , test_X , test_Y))

		if model_flag == 3 : 
			error.append(model.GDBT(train_X , train_Y , test_X , test_Y))
		
		if model_flag == 4 : 
			error.append(model.DNN(train_X , train_Y , test_X , test_Y , activation_function = "softmax"))
	



	train_mean_error = 0
	test_mean_error = 0

	for i in range(n) : 
		train_mean_error += error[i][0]
		test_mean_error += error[i][1]
	
	train_mean_error = train_mean_error / n
	test_mean_error = test_mean_error / n

	print("training error = {}".format(train_mean_error))
	print("testing error = {}".format(test_mean_error))

def adjust_hyper_param(df_X , df_Y , model_flag) : 

	if model_flag == 3 : 
		param = [{"learning_rate" : [0.05 , 0.07 , 0.1] , 
		"n_estimators" : [60 , 70 , 80 , 90 , 100] , 
		"max_depth" : [3 , 4 , 5] , 
		"subsample" : [0.6 , 0.7 , 0.8]
		}]

		gdbt = gradient_boosting.GradientBoostingRegressor(loss = "ls" , criterion = "friedman_mse" , warm_start = True)
		
		grid = GridSearchCV(gdbt , 
		param_grid = param , 
		scoring = "neg_mean_squared_error" , 
		n_jobs = -1 , 
		cv = 5 , 
		return_train_score = True)
		
		grid.fit(df_X , df_Y)

		print(grid.best_params_)
		print(grid.best_score_)
		print(grid.best_estimator_)

		res = grid.cv_results_
		output.write_csv(pd.DataFrame(res) , 2207 , "2207_GDBT_grid_search")