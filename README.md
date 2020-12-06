# Clustering-based-EOAS
Implemenation of Clustering based EOAS 
We have proposed a hybrid meta-heuristic FS method using clustering based Equilibrium Optimization (EO) and Atom Search Optimization (ASO) algorithms abbreviated as CEOAS algorithm. 
After reducing the feature dimension, the optimal feature subset is fed to the Support Vector Machine (SVM) and K-Nearest Neighbors (KNN) classifiers. 
Here, the combination of Linear Predictive Coding (LPC) and Linear Prediction Cepstral Coefficients (LPCC) based feature vectors are considered as the input features, and these features 
are optimized by using the proposed CEOAS algorithm.

The file feature extraction.py contains the code for feature extraction using LPC and LPCC. 
For an example SAVEE_FEATURE_EXTRACTION.csv file contains the extracted features of SAVEE dataset having dimension of 480 X 730. 
The function readWavFile(wav) will read the .wav files. 
The folder should be in a certain format to read all these files. Next work is generation of clusters where two parameters, number of initial of population is set to 15 and the no of cluster centers is chosen as 5. This results 5 binarized standard solution vectors which are to be fed to optimization algorithm for further feature selection task.   

Thus both ASO and EO are fed with clustering-based population with number of clusters equals to 5, in place of initial random population. ASO and EO further optimize their respective clustering-based population through progression of iterations. Thereafter 20 standard candidate solutions are selected from both EO and ASO algorithms, which are further fed to Average Weighted Combination Mean (AWCM) based statistical approach which a optimal solution vector out of these. We have uploaded two CSV files of named as BestPopulationEO.csv and BestPopulationASO.csv, where both the optimized best population is stored. Each of these CSV files has a dimension of 20 X 730. 

Now the output optimal solution vector of AWCM is again fed to SOPF algorithm for the sake of nearest neighbour searching and SOPF results the optimum feature set. 
