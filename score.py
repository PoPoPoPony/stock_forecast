from sklearn.model_selection import KFold
import model

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
	
	print(sum(error) / len(error))

