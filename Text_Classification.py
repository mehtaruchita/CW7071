import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
sns.set_style("whitegrid")
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LogisticRegression
import warnings
warnings.filterwarnings('ignore')
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import model_selection
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import classification_report
sns.set_style("whitegrid")
input = r'C:\Ruchita\MSc_Data_Science\Module-7-7071-Information_Retrieval\CW-7071\Text_classification\fake_job_postings.csv'
data_file = pd.read_csv(input)
data_file.info()
data_file.describe()
data_file[data_file['fraudulent'] == 1]
data_file = data_file[data_file['description'].notna()]
lancaster=LancasterStemmer()
stop_words = stopwords.words('english')

def pre_pro(text_prepros):
    #Tokinizing sentence into letters
    text_prepros = re.sub('[^a-zA-Z\s]', '', text_prepros)
    # Converting text into lower case
    text = text_prepros.lower()
    #Taking out stop words
    split = text.split()
    for word in split :
      if word in stop_words :
        word = ''
      else :
        lancaster.stem(word)
    return ' '.join([word for word in split])
data_file['description'] = data_file['description'].apply(pre_pro)
data_file['description'].sample(10)
# splitting train and test dataset
train_x, test_x, train_y, test_y = model_selection.train_test_split(data_file['description'], data_file['fraudulent'],test_size=0.25)

# encoding training and testing data
encoder = LabelEncoder()
train_y = encoder.fit_transform(train_y)
test_y = encoder.fit_transform(test_y)
MAX = 3500
vect = TfidfVectorizer(max_features = MAX)
vect.fit(train_x)

# vectorize train and test sets
train_x_vec = vect.transform(train_x)
test_x_vec = vect.transform(test_x)
log_regress = LogisticRegression()
log_regress.fit(train_x_vec, train_y)

# prediction
pred = log_regress.predict(test_x_vec)

# Accuracy Score
print("accuracy:", accuracy_score(pred, test_y), "\n")

# Confusion Matrix
cm = confusion_matrix(test_y, pred)
print("confusion matrix :\n", cm, "\n")

# create a classifcation report
print("classification report:\n", classification_report(test_y, pred), "\n")
