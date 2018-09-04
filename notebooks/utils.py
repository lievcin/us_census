import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as ticker
from matplotlib import rc
import seaborn as sns
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


rc('font',**{'family':'serif','serif':['Palatino']})
plt.style.use('seaborn-whitegrid')


COLUMNS = ['age','class of worker','detailed industry recode','detailed occupation recode','education',
           'wage per hour','enroll in edu inst last wk','marital stat','major industry code',
           'major occupation code','race','hispanic origin','sex','member of a labor union',
           'reason for unemployment','full or part time employment stat','capital gains','capital losses',
           'dividends from stocks','tax filer stat','region of previous residence','state of previous residence',
           'detailed household and family stat','detailed household summary in household',
           'instance weight','migration code-change in msa','migration code-change in reg',
           'migration code-move within reg','live in this house 1 year ago','migration prev res in sunbelt',
           'num persons worked for employer','family members under 18','country of birth father',
           'country of birth mother','country of birth self','citizenship','own business or self employed',
           "fill inc questionnaire for veteran's admin",'veterans benefits','weeks worked in year','year',
           'salary']

CONT_COLUMNS = ['age', 'wage per hour', 'capital gains', 'capital losses', 'dividends from stocks',
                'num persons worked for employer', 'weeks worked in year']
NOM_COLUMNS = [col for col in COLUMNS if col not in CONT_COLUMNS]

def columns_types(**kwargs):
	if 'df' in kwargs:
		nominal_columns = [col for col in kwargs['df'].columns if col not in CONT_COLUMNS]
		cont_columns    = [col for col in kwargs['df'].columns if col in CONT_COLUMNS]
	else:
		nominal_columns = NOM_COLUMNS
		cont_columns    = CONT_COLUMNS

	return cont_columns, nominal_columns

def one_hot(df, excl_columns=[]):
    df = df.drop(excl_columns, axis=1, inplace=False, errors='ignore')
    cont_columns, nominal_columns = columns_types(df=df)
    df_category_onehot = pd.get_dummies(df[nominal_columns])
    return df_category_onehot

def summarise_column(df, column_name, **kwargs):

	sns.set_style("whitegrid")
	sns.set_color_codes("pastel")

	# Simple summary of the column
	print('Summary for column: {}'.format(column_name))
	print(df[[column_name]].describe(percentiles=[.25, .5, .75, .99]))

	plt.figure(figsize=(8,6))

	if column_name in cont_columns:
		if 'chart_type' in kwargs:
			CHART_TYPE = kwargs['chart_type']
		else:
			CHART_TYPE = 'Histogram'

			if CHART_TYPE=='Histogram':
				df[column_name].hist(bins=12)
			elif CHART_TYPE=='Smooth':
				sns.kdeplot(df[column_name], shade=True)
			elif CHART_TYPE=='Box Plot':
				sns.boxplot(df[column_name], color = "green", orient = "v")

	else:

		df[column_name].value_counts().sort_values(ascending=True).tail(15).plot.barh(color='b')
		plt.ylabel(column_name.title(), fontsize=12)
		plt.xlabel('Number of people', fontsize=12)

		ax = plt.gca()
		ax.yaxis.grid(False)
		ax.get_xaxis().set_major_formatter(mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

	plt.show()

def class_report(y_true, y_pred, dataset):
    print(dataset + ' Set:\n')
    print(dataset + ' Confusion Matrix:')
    print(confusion_matrix(y_true, y_pred))
    print(dataset + ' Classification report:')
    print(classification_report(y_true, y_pred))
    print(dataset + ' Accuracy: {}'.format(accuracy_score(y_true, y_pred)))