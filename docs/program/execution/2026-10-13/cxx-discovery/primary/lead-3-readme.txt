# Conditional-Entropy-Based-Causal-Discovery
This work aims to find the causal rules using conditional entropy in Cyberstalking data set. In cyberstalking, someone is harassed, using the internet and different technologies by one or several people. This data set is prepared from high school students and contains 15 features and each of the students responded the questions (where, each feature is mapped to one question) by one of the presented variables. An algoritm (COJEC) is proposed to find the causal rules of this data set. For the proposed algorithm our inputs are the set of features of dataset i.e., F = {F1, F2, . . . , Ff } and the threshold value τ . Each feature i  contains different values denoted by V . Thus we can represent feature i is as Fi = {V1,Fi , V2,Fi , . . . , V|Fi|,Fi } where |Fi| denotes the number of values of feature i. For example, in the cyberstalking data set the third feature is "Age" where its has three 15, 16 and 17 values. Thus we can write this feature as F3 = {V(1,3), V(2,3), V(3,3)} = {15, 16, 17}. The out put will be the set of causal rules (X → Y) determined using the algorithm. This algorithm starts by determining all sub sets of F with m elements. This algorithm checks all the possible subsets of F by the end of the algorithm. After determining F^(m) which is all the subsets of F for a certain m starting from 1 to f − 1, selects each subset of it (F_s^(m)) and for each (F_s^(m)) computes the Cartesian product (F_C^(m)). Set of Cartesian product of sub set (F_s^(m)) are denoted as X = {X1, X2, . . . , Xm}. Then this process will be replicated for other subsets of features and Cartesian product of them will be done and denoted as Y = {Y1, Y2, . . . , Yn}. Now we haveX and Y sets. If X ∩ Y = ∅ and H(Y |X) ≤ τ  conditions are satisfied for X and Y ,  (X → Y ) will be considered as a causal rule  and will be adde to the output set of rules. Conditional entropy of H(Y |X) for X = {X1, X2, . . . , Xm} and Y = {Y1, Y2, . . . , Yn} is computed using the following formula:

<img width="252" alt="image" src="https://user-images.githubusercontent.com/87864575/174624362-3329cb2a-4254-447e-83a6-188fdd1495b9.png">


# Proposed  Algorithm:
ALGORITHM:  Conditional Joint Entropy-based Casual rule discovery
The pseudo-code of the proposed algorithm is presented in the figure below and the Code of this algorithm can be found in the COJEC.cpp file at code files.





<img width="215" alt="Screenshot 2022-06-20 171443" src="https://user-images.githubusercontent.com/87864575/174623196-d18297f9-0865-4d58-9feb-389a9b509024.png">

# Results
This algorithm discovers the causal rules between the features of cyberstalking data set by computing the conditional entropy of the Cartesian product of all subsets of feature. In this implementation the value of threshold τ is considered equal to 0.08. Thus the implemented algorithm discovers the causal rules of X => Y when the conditional entropy of the sub sets of features (H(Y |X)) is less than 0.08. For τ = 0.08 for cyberstalking data set, the presented algorithm found 116 causal rules for m = 2 and n = 1. Since writing all of the causal rules obtained by implementing the Algorithm 1 is not possible, some of them are represented in Casual rules.txt file.
[casual rules.txt](https://github.com/sama1habibi/Conditional-Entropy-Based-Causal-Discovery/files/8941503/casual.rules.txt)
