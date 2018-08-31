import pandas as pd
import numpy as np

def process_df(interim_dir):

	df_train = pd.read_csv(interim_dir+'/census_income_learn.csv')
	df_train['set']='train'
	df_test = pd.read_csv(interim_dir+'/census_income_test.csv')
	df_test['set']='test'
	df = pd.concat([df_train, df_test], ignore_index=True, sort=True)
	df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

	bins = range(0, df['weeks worked in year'].max()+10, 10)
	df['weeks worked in year'] = pd.cut(df['weeks worked in year'], bins=bins, include_lowest=True)

	bins = range(0, df['capital gains'].max()+5000, 5000)
	df['capital gains'] = pd.cut(df['capital gains'], bins=bins, include_lowest=True)

	bins = range(0, df['capital losses'].max()+500, 500)
	df['capital losses'] = pd.cut(df['capital losses'], bins=bins, include_lowest=True)

	bins = range(0, df['dividends from stocks'].max()+5000, 5000)
	df['dividends from stocks'] = pd.cut(df['dividends from stocks'], bins=bins, include_lowest=True)

	bins = range(0, df['wage per hour'].max()+10, 10)
	df['wage per hour'] = pd.cut(df['wage per hour'], bins=bins, include_lowest=True)

	df["fill inc questionnaire for veteran's admin"].replace('Not in universe', 'No', inplace=True)
	df['family members under 18'].replace('Not in universe', 'Unknown', inplace=True)

	df['migration prev res in sunbelt'].replace('?', 'Unknown', inplace=True)
	df['migration prev res in sunbelt'].replace('Not in universe', 'Unknown', inplace=True)
	df['live in this house 1 year ago'].replace('Not in universe under 1 year old', 'Unknown', inplace=True)

	df['migration code-move within reg'].replace('?', 'Unknown', inplace=True)
	df['migration code-move within reg'].replace('Not in universe', 'Unknown', inplace=True)
	df['migration code-move within reg'].replace('Different state in South', 'Different state', inplace=True)
	df['migration code-move within reg'].replace('Different state in West', 'Different state', inplace=True)
	df['migration code-move within reg'].replace('Different state in Midwest', 'Different state', inplace=True)
	df['migration code-move within reg'].replace('Different state in Northeast', 'Different state', inplace=True)
	df['migration code-move within reg'].replace('Abroad', 'Different state', inplace=True)
	df['migration code-move within reg'].replace('Different county same state', 'Same state', inplace=True)
	df['migration code-move within reg'].replace('Same county', 'Same state', inplace=True)

	df['migration code-change in reg'].replace('?', 'Unknown', inplace=True)
	df['migration code-change in reg'].replace('Not in universe', 'Unknown', inplace=True)
	df['migration code-change in reg'].replace('Different region', 'Different state', inplace=True)
	df['migration code-change in reg'].replace('Different state same division', 'Different state', inplace=True)
	df['migration code-change in reg'].replace('Different division same region', 'Different state', inplace=True)
	df['migration code-change in reg'].replace('Different state in South', 'Different state', inplace=True)
	df['migration code-change in reg'].replace('Different state in West', 'Different state', inplace=True)
	df['migration code-change in reg'].replace('Different state in Midwest', 'Different state', inplace=True)
	df['migration code-change in reg'].replace('Different state in Northeast', 'Different state', inplace=True)
	df['migration code-change in reg'].replace('Abroad', 'Different state', inplace=True)
	df['migration code-change in reg'].replace('Different county same state', 'Same state', inplace=True)
	df['migration code-change in reg'].replace('Same county', 'Same state', inplace=True)

	df['migration code-change in msa'].replace('?', 'Unknown', inplace=True)
	df['migration code-change in msa'].replace('Not in universe', 'Unknown', inplace=True)
	df['migration code-change in msa'].replace('Not identifiable', 'Unknown', inplace=True)

	df['detailed household summary in household'].replace('Child under 18 never married', 'Under 18', inplace=True)
	df['detailed household summary in household'].replace('Child under 18 ever married', 'Under 18', inplace=True)
	df['detailed household summary in household'].replace('Group Quarters- Secondary individual', 'Nonrelative of householder', inplace=True)

	df['state of previous residence'].replace('Not in universe', 'Unknown', inplace=True)
	df['state of previous residence'].replace('?', 'Unknown', inplace=True)
	df['region of previous residence'].replace('Not in universe', 'Unknown', inplace=True)

	# Want to group all these different types into cleaner categories. Also splitting armed forces and kids
	df['full or part time employment stat'].replace('PT for econ reasons usually FT', 'Part-time', inplace=True)
	df['full or part time employment stat'].replace('PT for econ reasons usually PT', 'Part-time', inplace=True)
	df['full or part time employment stat'].replace('PT for non-econ reasons usually FT', 'Part-time', inplace=True)
	df['full or part time employment stat'].replace('Unemployed full-time', 'Unemployed', inplace=True)
	df['full or part time employment stat'].replace('Unemployed part- time', 'Unemployed', inplace=True)
	df['full or part time employment stat'].replace('Full-time schedules', 'Full-time', inplace=True)
	df.loc[((df['full or part time employment stat']=='Children or Armed Forces') & (df['age']<=18)), 'full or part time employment stat'] = 'Child'
	df['full or part time employment stat'].replace('Children or Armed Forces', 'Armed Forces', inplace=True)

	bins = range(0, df['age'].max()+5, 5)
	df['age'] = pd.cut(df['age'], bins=bins, include_lowest=True)

	df['member of a labor union'].replace('Not in universe', 'No', inplace=True)

	df['marital stat'].replace('Married-spouse absent', 'Separated', inplace=True)
	df['marital stat'].replace('Divorced', 'Separated', inplace=True)
	df['marital stat'].replace('Married-civilian spouse present', 'Married', inplace=True)
	df['marital stat'].replace('Married-A F spouse present', 'Married', inplace=True)


	df['education'].replace('Masters degree(MA MS MEng MEd MSW MBA)', 'Postgraduate', inplace=True)
	df['education'].replace('Doctorate degree(PhD EdD)', 'Postgraduate', inplace=True)
	df['education'].replace('Prof school degree (MD DDS DVM LLB JD)', 'Postgraduate', inplace=True)
	df['education'].replace('Bachelors degree(BA AB BS)', 'Undergraduate', inplace=True)
	df['education'].replace('Associates degree-occup /vocational', 'Undergraduate', inplace=True)
	df['education'].replace('Associates degree-academic program', 'Undergraduate', inplace=True)
	df['education'].replace('11th grade', 'Secondary school', inplace=True)
	df['education'].replace('10th grade', 'Secondary school', inplace=True)
	df['education'].replace('9th grade', 'Secondary school', inplace=True)
	df['education'].replace('12th grade no diploma', 'Secondary school', inplace=True)
	df['education'].replace('7th and 8th grade', 'Primary school', inplace=True)
	df['education'].replace('5th or 6th grade', 'Primary school', inplace=True)
	df['education'].replace('1st 2nd 3rd or 4th grade', 'Primary school', inplace=True)
	df['education'].replace('Less than 1st grade', 'Children', inplace=True)

	df['detailed household and family stat'].replace('Child <18 never marr not in subfamily', 'Child <18', inplace=True)
	df['detailed household and family stat'].replace('Grandchild <18 never marr child of subfamily RP', 'Child <18', inplace=True)
	df['detailed household and family stat'].replace('Child under 18 of RP of unrel subfamily', 'Child <18', inplace=True)
	df['detailed household and family stat'].replace('Child <18 never marr RP of subfamily', 'Child <18', inplace=True)
	df['detailed household and family stat'].replace('Child <18 spouse of subfamily RP', 'Child <18', inplace=True)
	df['detailed household and family stat'].replace('Grandchild <18 ever marr not in subfamily', 'Child <18', inplace=True)
	df['detailed household and family stat'].replace('Grandchild <18 never marr RP of subfamily', 'Child <18', inplace=True)
	df['detailed household and family stat'].replace('Child <18 ever marr RP of subfamily', 'Child <18', inplace=True)
	df['detailed household and family stat'].replace('Child <18 ever marr not in subfamily', 'Child <18', inplace=True)
	df['detailed household and family stat'].replace('Grandchild <18 never marr not in subfamily', 'Child <18', inplace=True)
	df['detailed household and family stat'].replace('Grandchild 18+ never marr not in subfamily', 'Child 18+', inplace=True)
	df['detailed household and family stat'].replace('Child 18+ spouse of subfamily RP', 'Child 18+', inplace=True)
	df['detailed household and family stat'].replace('Child 18+ never marr Not in a subfamily', 'Child 18+', inplace=True)
	df['detailed household and family stat'].replace('Child 18+ ever marr Not in a subfamily', 'Child 18+', inplace=True)
	df['detailed household and family stat'].replace('Child 18+ ever marr RP of subfamily', 'Child 18+', inplace=True)
	df['detailed household and family stat'].replace('Child 18+ never marr RP of subfamily', 'Child 18+', inplace=True)
	df['detailed household and family stat'].replace('Grandchild 18+ ever marr not in subfamily', 'Child 18+', inplace=True)
	df['detailed household and family stat'].replace('Grandchild 18+ ever marr RP of subfamily', 'Child 18+', inplace=True)
	df['detailed household and family stat'].replace('Grandchild 18+ spouse of subfamily RP', 'Child 18+', inplace=True)
	df['detailed household and family stat'].replace('Grandchild 18+ never marr RP of subfamily', 'Child 18+', inplace=True)
	df['detailed household and family stat'].replace('Other Rel <18 ever marr RP of subfamily', 'Other Rel <18', inplace=True)
	df['detailed household and family stat'].replace('Other Rel <18 never married RP of subfamily', 'Other Rel <18', inplace=True)
	df['detailed household and family stat'].replace('Other Rel <18 spouse of subfamily RP', 'Other Rel <18', inplace=True)
	df['detailed household and family stat'].replace('Other Rel <18 ever marr not in subfamily', 'Other Rel <18', inplace=True)
	df['detailed household and family stat'].replace('Other Rel <18 never marr child of subfamily RP', 'Other Rel <18', inplace=True)
	df['detailed household and family stat'].replace('Other Rel <18 never marr not in subfamily', 'Other Rel <18', inplace=True)
	df['detailed household and family stat'].replace('Other Rel 18+ ever marr not in subfamily', 'Other Rel 18+', inplace=True)
	df['detailed household and family stat'].replace('Other Rel 18+ never marr not in subfamily', 'Other Rel 18+', inplace=True)
	df['detailed household and family stat'].replace('Other Rel 18+ spouse of subfamily RP', 'Other Rel 18+', inplace=True)
	df['detailed household and family stat'].replace('Other Rel 18+ ever marr RP of subfamily', 'Other Rel 18+', inplace=True)
	df['detailed household and family stat'].replace('Other Rel 18+ never marr RP of subfamily', 'Other Rel 18+', inplace=True)
	df['detailed household and family stat'].replace('RP of unrelated subfamily', 'Other Rel 18+', inplace=True)
	df['detailed household and family stat'].replace('Nonfamily householder', 'Other', inplace=True)
	df['detailed household and family stat'].replace('Secondary individual', 'Other', inplace=True)
	df['detailed household and family stat'].replace('Spouse of RP of unrelated subfamily', 'Other', inplace=True)
	df['detailed household and family stat'].replace('In group quarters', 'Other', inplace=True)


	latin_america = ['Panama','Mexico','Dominican-Republic','El-Salvador','Honduras','Columbia','Guatemala','Peru','Ecuador','Nicaragua']
	caribbean = ['Trinadad&Tobago','Puerto-Rico','Jamaica','Haiti','Cuba']
	europe = ['Yugoslavia','Holand-Netherlands','Ireland','France','Germany','England','Italy','Poland','Portugal','Greece','Scotland','Hungary']
	asia = ['Iran','India','Cambodia','Hong Kong','Taiwan','China','South Korea','Japan','Vietnam','Philippines','Thailand','Laos']

	df['country of birth self'].replace('?', 'Unknown', inplace=True)
	df.loc[df['country of birth self'].isin(latin_america), 'country of birth self'] = 'Latin America'
	df.loc[df['country of birth self'].isin(caribbean), 'country of birth self'] = 'Caribbean'
	df.loc[df['country of birth self'].isin(europe), 'country of birth self'] = 'Europe'
	df.loc[df['country of birth self'].isin(asia), 'country of birth self'] = 'Asia'
	df.loc[df['country of birth self']=='Outlying-U S (Guam USVI etc)', 'country of birth self'] = 'United-States'

	df['country of birth mother'].replace('?', 'Unknown', inplace=True)
	df.loc[df['country of birth mother'].isin(latin_america), 'country of birth mother'] = 'Latin America'
	df.loc[df['country of birth mother'].isin(caribbean), 'country of birth mother'] = 'Caribbean'
	df.loc[df['country of birth mother'].isin(europe), 'country of birth mother'] = 'Europe'
	df.loc[df['country of birth mother'].isin(asia), 'country of birth mother'] = 'Asia'
	df.loc[df['country of birth mother']=='Outlying-U S (Guam USVI etc)', 'country of birth mother'] = 'United-States'

	df['country of birth father'].replace('?', 'Unknown', inplace=True)
	df.loc[df['country of birth father'].isin(latin_america), 'country of birth father'] = 'Latin America'
	df.loc[df['country of birth father'].isin(caribbean), 'country of birth father'] = 'Caribbean'
	df.loc[df['country of birth father'].isin(europe), 'country of birth father'] = 'Europe'
	df.loc[df['country of birth father'].isin(asia), 'country of birth father'] = 'Asia'
	df.loc[df['country of birth father']=='Outlying-U S (Guam USVI etc)', 'country of birth father'] = 'United-States'

	df_train = df[df['set']=='train']
	df_test = df[df['set']=='test']

	return df_train, df_test

