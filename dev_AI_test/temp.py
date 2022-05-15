import numpy as np

class Feature:
	def __init__(self):
		t=1

	def view_print(self, text, arg):
		print("\n------------------")
		print(text)
		print("------------------")
		print(arg)

	def RMSE(self, y_true, y_pred):
	    return np.sqrt(np.mean((np.array(y_true) - np.array(y_pred))**2))