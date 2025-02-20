# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 14:12:48 2016

@author: Zarmeen
"""

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import gensim
from gensim.models import Word2Vec
import CategoryDetectionTrain
import OTE
import PolarityDetection
import sys
from gooey import Gooey, GooeyParser
sys.path.insert(0, sys.path[0]+'\\flaskWebApp')
import flaskDemo

@Gooey(advanced=True,program_name='ABSA Toolkit',image_dir='images/')
def main():
	#print sys.argv
	# sys.argv[1] -- > 'data/restaurants/train.csv'
	# sys.argv[2] -- > 'data/restaurants/test.csv'
	# sys.argv[3] -- > 'vectors_yelp_200.txt'
	# sys.argv[4] -- > 'lexicons/Yelp-restaurant-reviews-AFFLEX-NEGLEX-unigrams.txt'

	# python absa.py data/restaurants/train.csv data/restaurants/test.csv vectors_yelp_200.txt lexicons/Yelp-restaurant-reviews-AFFLEX-NEGLEX-unigrams.txt
	# python absa.py data/laptops/laptopTrain3.csv data/laptops/laptopTest3.csv  amazon200.txt lexicons/Amazon-laptops-electronics-reviews-AFFLEX-NEGLEX-unigrams.txt
	#  python absa.py data/camera/camera_train.csv data/camera/camera_test.csv  amazon200.txt lexicons/Amazon-laptops-electronics-reviews-AFFLEX-NEGLEX-unigrams.txt
	# python absa.py data/hotels/train_hotel.csv data/hotels/test_hotel.csv vectors_yelp_200.txt lexicons/Yelp-restaurant-reviews-AFFLEX-NEGLEX-unigrams.txt

	parser = GooeyParser(description="ABSA Toolkit!") 
	parser.add_argument('trainF',metavar='Train Set',help="Upload CSV file for training model", widget="FileChooser")
	parser.add_argument('testF',metavar='Test Set',help="Upload CSV file for testing model", widget="FileChooser")
	parser.add_argument('vecF',metavar='Word Embeddings',help="Upload text file containing Word embeddings", widget="FileChooser")
	parser.add_argument('lexF',metavar='Lexicon',help="Upload text file containing sentiment scores", widget="FileChooser")
	parser.add_argument('algCD',metavar='Category Detection Algorithm',help="Choose algorithm for training Category Detection Models",choices = ['XgBoost', 'Random Forest','Naive Bayes','SVM'])
	parser.add_argument('algPD',metavar='Polarity Detection Algorithm',help="Choose algorithm for training Sentiment Polarity Classifiers",choices = ['XgBoost', 'Random Forest','Naive Bayes','SVM'])
	args = parser.parse_args()

	trainF = args.trainF#user provided
	testF =  args.testF#user provided

	vectors_filename = args.vecF #user provided
	lex_file =  args.lexF
	algCD = args.algCD
	algPD = args.algPD
	#trainF =   str(sys.argv[1])#user provided
	#testF =    str(sys.argv[2])#user provided

	#vectors_filename = "wordembeddings/" + str(sys.argv[3]) #user provided
	#lex_file =  str(sys.argv[4])
	#trainF = 'data/laptops/laptopTrain3.csv' #user provided
	#testF = 'data/laptops/laptopTest3.csv'   #user provided

	#trainF = 'data/laptops/laptop_train_ote.csv' #user provided
	#testF = 'data/laptops/laptop_test_ote.csv'   #user provided

	#vectors_filename = "gloveVec200.txt" #user provided
	#vectors_filename = "wordembeddings/amazon200.txt"
	#print algCD
	print("Reading training and testing files")
	train_SF = pd.read_csv(trainF,sep = '\t')
	test_SF = pd.read_csv(testF,sep = '\t')

	print "Loading Word2Vec Model..."
	model = gensim.models.Word2Vec.load_word2vec_format(vectors_filename,binary=False)

	print "******************** Step 1/3 : Aspect Term Extraction     ********************"
	f1_ote = OTE.main(train_SF,test_SF,model)

	print "******************** Step 2/3 : Aspect Category Extraction ********************"
	f1_cat = CategoryDetectionTrain.main(train_SF,test_SF,model,algCD)


	print "******************** Step 3/3 : Aspect Polarity Detection  ********************"
	acc,fsco = PolarityDetection.main(train_SF,test_SF,model,lex_file,algPD)

	#f1_ote=0.72
	#f1_cat=0.72
	
	#acc=0.84
	#fsco=0.84
	print ""
	print ""
	print "\t*****    Training and Evaluation of ABSA System Complete    *****"
	print ""
	print ""
	print "\t*****        Summary of ABSA-Toolkit Training Phase        *****"
	print ""
	print ""
	print ""
	print "\t*	Aspect Term Extraction Model 		(F1 - Measure)   : %.2f	"%round(f1_ote, 2)
	print ""
	print ""
	print "\t*	Aspect Category Detection Model 	(F1 - Measure)   : %.2f	"%round(f1_cat,2)
	print ""
	print ""
	print "\t*	Polarity Identification Model 		(Accuracy)       : %.2f	"%round(acc,2)
	print "\t*	Polarity Identification Model 		(F1- Measure)       : %.2f	"%round(fsco,2)
	print ""
	print "\t*****        --------------------------------------        *****"


	print ""
	print ""
	print ""
	print " Start your Flask Web Application using command shown below"
	#print "python absaweb.py -vectorsFile -lexiconFile"
	while(True):
	  flaskDemo.runMain(vectors_filename,lex_file)
		
main()
    
    
    	
    