# Clustering-based-EOAS
Implemenation of Clustering based EOAS 
We have proposed a hybrid meta-heuristic FS method using clustering based Equilibrium Optimization (EO) and Atom Search Optimization (ASO) algorithms abbreviated as CEOAS algorithm. 
After reducing the feature dimension, the optimal feature subset is fed to the Support Vector Machine (SVM) and K-Nearest Neighbors (KNN) classifiers. 
Here, the combination of Linear Predictive Coding (LPC) and Linear Prediction Cepstral Coefficients (LPCC) based feature vectors are considered as the input features, and these features 
are optimized by using the proposed CEOAS algorithm.

The file feature extraction.py contains the code for feature extraction using LPC and LPCC. 
For an example SAVEE_FEATURE_EXTRACTION.csv file contains the extracted features of SAVEE dataset having dimension of 480 X 730. 
The function readWavFile(wav) will read the .wav files. 
The folder should be in a certain format to read all these files. Next work is generation of clusters where two parameters, number of initial of population is set to 15 and the no of cluster centers is chosen as 5. This results 5 binarized standard solution vectors which are to be fed to further optimization algorithm.   

Thus both ASO and EO are fed with clustering-based population with number of clusters equals to 5, for each case. ASO and EO further optimize their respective clustering-based population. 
After execution of this stage we have to note the top twenty solutions with the accuracies for both the optimization algorithms and save them to a CSV file.
We have uploaded two CSV files named as BestPopulationEO.csv and BestPopulationASO.csv, where both the optimized best population is stored. 
Finally the CSV file having the dimension of 40 X 730 will enter into the AWCM part and optimal solution will be obtained.
For classification part we have used SVM and KNN classifier. The classification code is embadded in the both EO.py and ASO.py part. 
