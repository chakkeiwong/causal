# Causal_discovery-Experiment  
<img src="./images/top.png">  
The idea is to use deep learning to directly estimate g and f in the post-nonlinear model in an attempt to perform nonlinear causal search. However, we impose a constraint to maximize the independence between residuals.  
The calculation assumes the existence of an unobserved common cause $`\mu`$.
This is not practical at all because the computation time exceeds the acceptable limit.

 **post-nonlinear model**  
 $` y=g^{-1} (f(x) + \epsilon ) `$
  
We are experimenting with a similar model of post-nonlinear model.  
 $` y=g^{-1} (f(x, \,\,\boldsymbol{\mu}) + \epsilon ) `$  
$` \mu `$ is a generalized Gaussian distribution $`\,`$  
$` \mu(x) = \frac{\beta^{1/2}}{2\Gamma(1+1/\rho)} exp(-\beta^{1/2}|x-\tilde{x}|^{\rho})`$  

<img src="./images/fig1.png"  width="30%">  

$`\beta`$ and $`\rho`$ are parameters to be determined and estimated by optimization.  

$` loss = max(w1 \,max(\epsilon_{i}), w2\,max(MI(e_{i},e_{j})))+\epsilon\,(w1 \,max(\epsilon_{i}), w2\,max(MI(e_{i},e_{j})))`$

$`e_{i}`$ is the noise component of variable $`x_{i}`$  
$`\epsilon_{i}`$ is the RMSE of $`e_{i}`$   

MI is an independent variable if it is zero in the mutual information content.   
In other words, $`\mu`$ is obtained so that both the residuals and
 the mutual information content between residuals are minimized.   
 Loss loss is an expanded Tchebyshev scalarization function.  

- $`\epsilon`$=0.0001
- $`w1`$=0.7
- $`w2`$=0.4

---
## Experiment
- Causal structure compared  
<img src="./images/image5.png"  width="40%">  
reference https://proceedings.mlr.press/v177/uemura22a/uemura22a.pdf   

Solid and dashed lines are estimated edges and ground truths, respectively.

- ICA-LiNGAM  
<img src="./images/image4.png" width="40%"> <img src="./images/image11.png" width="34%">    
   

The numbers mean the correlation coefficient in parentheses and the linear coefficient outside the parentheses.  
The green arrow line is the result of ICA-LiNGAM  

- Experiment  

<img src="./images/fMRI_sim2/Digraph_dot.png" width="35%"> <img src="./images/image10.png" width="35%">    
    

The values in parentheses indicate the correlation coefficient, the values outside the parentheses indicate the feature importance, and the percentage values indicate the confidence level.
Feature Importance is a relative value when the maximum is 1.0.  
The green arrow line is the result of the experiment  

- Causal structure compared  
<img src="./images/image7.png" width="30%">  
reference https://proceedings.mlr.press/v177/uemura22a/uemura22a.pdf   

Solid and dashed lines are estimated edges and ground truths, respectively.  

- ICA-LiNGAM  
<img src="./images/image13.png" width=120>  

- Experiment  
<img src="./images/fMRI_sim1/Digraph_dot.png" width="30%">  <img src="./images/image9.png" width="35%">    
The values in parentheses indicate the correlation coefficient, the values outside the parentheses indicate the feature importance, and the percentage values indicate the confidence level.
Feature Importance is a relative value when the maximum is 1.0.  
The green arrow line is the result of the experiment  
      

---
## Probability of possible causality from each variable  
<img src="./images/b_probability.png" width="20%">  

## Examples of output other than causal structure  
<img src="./images/Causal_effect.png" width="20%">  

## Error for each variable in the causal structure model  
<img src="./images/causal_multi_histgram.png" width="40%">  

---
## Estimate contributions from unobserved variables  
<img src="./images/Digraph_0.png" width="50%">  

---


---
## Note  
This is still an experimental implementation.
Therefore, the optimization is close to a parameter brute force approach,   
where randomly generated parameters are set and computed, and the optimal solution is updated as the LOSS becomes smaller.   
Therefore, it is very difficult to determine at what point to stop the calculation.  
<img src="./images/Digraph_2.png" width="20%">
<img src="./images/loss.png" width="53%">  
In this example, it took 59 iterations to obtain the correct result, which I believe is very rare.
This is a very fortunate case.
In other experiments, it has often occurred that 20,000 calculations are required.  

The causal structure is correct when the LOSS drops the most, even though it may change only slightly.  

- loss  1->2->3->4  
<img src="./images/fMRI_sim2/Digraph_0.png/" width="30%">  

- 1  
<img src="./images/fMRI_sim2/Digraph_1.png" width="30%">  

- 2  
<img src="./images/fMRI_sim2/Digraph_2.png" width="30%">  

- 3  
<img src="./images/fMRI_sim2/Digraph_3.png" width="30%">  

- 4   
<img src="./images/fMRI_sim2/Digraph_dot.png" width="30%">  

---
Roughly speaking, ICA-LiNGAM is used. However, LiNGAM is used to obtain the B matrix, so it does not have to be LiNGAM.  
The B matrix is used as a causal (parent-child) structure and ignored for their linear relationship.  
Adding fluctuations to the input data changes the causal structure (B matrix) that is computed and calculated.  
In other words, different causal (parent-child) structures are obtained.

In the case of ICA-LiNGAM, it is a linear model, so it is as follows.  


```math
\begin{pmatrix}
x_{1} \\
x_{2} \\
 \vdots \\
x_{n} \\
\end{pmatrix} = \begin{pmatrix}
0 & 0 & \cdots & 0 \\
B_{21} & 0 & \cdots & 0 \\
 \vdots & \vdots & \cdots & \vdots \\
B_{n1} & B_{n2} & \cdots & 0 \\
\end{pmatrix}\begin{pmatrix}
x_{1} \\
x_{2} \\
 \vdots \\
x_{n} \\
\end{pmatrix} + \begin{pmatrix}
\epsilon_{1} \\
\epsilon_{2} \\
 \vdots \\
\epsilon_{n} \\
\end{pmatrix}
```

$`x_{1} = \epsilon_{1}`$  
$`x_{2} = {B_{21}\,x}_{1} + \epsilon_{2}`$  
$`x_{3} = {B_{31}\,x}_{1} + {B_{32}\,x}_{2} + \epsilon_{3}`$  
$`x_{4} = {B_{41}\,x}_{1} + {B_{42}\,x}_{2}  + {B_{43}\,x}_{3}+ \epsilon_{4}`$  
$`\cdots `$  

$`x^{\prime} \leftarrow x - (distribution\_rate* normal\_distribution\_random() + \mu(x)\_random()\,distribution\_rate)`$
  
Based on the causal relationship (parent-child relationship) based on the structure of this B matrix  
$`x \rightarrow y`$   
relationship can be obtained.   

$`x_{1} = \epsilon_{1}`$  
$`x_{2} = (g^{-1}f)_{1}(x_{1},\,\,\, \mu_{1}\,u1\_param)`$  
$`x_{3} = (g^{-1}f)_{2}(x_{1}, x_{2},\,\,\,\mu_{1}\,u1\_param,\mu_{2}\,u1\_param)`$  
$`x_{4} = (g^{-1}f)_{3}(x_{1}, x_{2}, x_{3},\,\,\,\mu_{1}\,u1\_param,\mu_{2}\,u1\_param,\mu_{3}\,u1\_param)`$  
$`\cdots `$  

$`u1\_param`$  is used for scale adjustment.   

<!-- 
$`y=g^{-1}f(x, \mu)`$  
and   
$`g(y) = f(x, \mu) `$   
is estimated by deep learning.
In other words, the optimization is performed so that   
$`\|(y_{pred} - y_{obs})\|`$   
is minimized, but   
$`\|g(y_{pred}) - y_{obs}\|`$   
must also be minimized. 
In addition, adjust the undetermined parameters so that the loss is minimized.  
$` loss = max(w1 \,max(e_{i}), w2\,max(MI(e_{i},e_{j})))+\epsilon\,(w1 \,max(e_{i}), w2\,max(MI(e_{i},e_{j})))`$  
-->  

$`f`$ and $`g`$ are trained as follows using deep learning.  
I understand this is pretty redundant.  
$`output = F(x)`$

$`output2 = G(y)`$  
Train output2 to be the same value as output  
$`|output2 - output| \rightarrow 0  \rightarrow G(y)  = F(x)`$  

$`output3 = H(output)`$  
Train output3 to be the same value as output at the same time  
$`|y - output3| \rightarrow 0 \rightarrow y  = H(F(x))= H(G(y))`$  

By training F, G, and H at the same time  
$`F(x) = f(x)\rightarrow f=F`$,  
$`F(x) = G(y)\rightarrow g=G`$,  
$`H( G(y)) = y \rightarrow H=G^{-1}\rightarrow g^{-1} = G^{-1}`$    
can be obtained.

In the above, we have
$`y = g^{-1}(f(x)+ε)`$
can be obtained.  

Further, the parameters are updated so that LOSS is minimized.  
$` loss = max(w1 \,max(e_{i}), w2\,max(MI(e_{i},e_{j})))+\epsilon\,(w1 \,max(e_{i}), w2\,max(MI(e_{i},e_{j})))`$  

---
  
#### Deleting Redundant Edges  

A causal relationship that is presumed in the opposite direction of the known correct answer or certain knowledge is clearly erroneous.  
However, useless relationships may be inferred even when they are not supposed to be in the opposite direction. Of these, it is possible to delete relations that are omissible or considered unnecessary.
However, arbitrarily deleting them is an erroneous practice.  
When the correct answer is unknown to begin with, such an action makes no sense at all and may lead to an arbitrary causal relationship as the solution.  

Therefore, such “edge deletion” may only be specified under the following conditions.  

- Limit the size of the causal effect and invalidate the causal relationship if the estimated effect is smaller than the specified value.
- Invalidate the causal relationship if the estimated independence index is smaller than the specified value (the smaller the value, the more irrelevant).
- Limit the magnitude of the correlation and invalidate the causal relationship if the estimated correlation is smaller than the specified value.
- Disable causality by setting the coefficients of characteristics (explanatory variables) that are considered unnecessary for forecasting in a lass regression to 0.  


These four ways can be implemented. Combinations are also possible, but the order cannot be specified.   

The magnitude of the causal effect is the magnitude of the absolute value of the coefficient of the relevant relationship in the B matrix in the case of a causal search for a linear relationship

$`x_{i} \rightarrow x_{j}`$  

$`x_{i} = \sum_{n=1}^NB_{i,j}x_{j}`$   

The magnitude of the absolute value of the IMPORTANCE in the non-linear case.  

Algorithmically, it often takes a long time to converge to an optimal solution, depending on the choice of parameters.

This makes it very difficult to decide where to stop the iterative computation.
Losses may initially go down toward the optimal solution, but at some point they may stall.
The difficulties are.  

1. to assume that the solution has already converged, stop the calculation, and assume that the solution at that point is the correct solution.
2. to continue the calculation assuming that it has not yet converged.  

In many cases, 1. identifies the causal structure of the correct solution, but in other cases it does not.  
be patient and continue the calculation, which may result in a sudden decrease in loss.  
In such cases, a decision must still be made as to whether or not to assume that point as the solution.  


In [abpnl](https://github.com/rafcc/abpnl), the calculation is stopped at n_epoch(default:100).
In this project, epoch(default:60) is used, but 30000 times is set by default for sampling of causal structure patterns.
In the meantime, `early_stopping` can be specified.  

This difficulty is due to the fact that both of these methods use deep-learning, which has a hyperparameter that can be adjusted, and depending on how well it is adjusted, it may be possible to get to the correct answer immediately.
Some of them lead to the correct answer immediately, others not so much.  

I recognize that this is a very big issue, but I don't know how to solve it at the moment.
We have tried many things, but nothing has worked. The source code is therefore very messy.  


<img src="./images/Nonlinear2.png" width="60%">  
<img src="./Causal_Search_Experiment/output/nonlinear2/Digraph_2.png" width="50%">  

it can be determined that the loss has converged at 53 times. 
We can determine that the loss will not decrease any further if we continue the calculation.  

<img src="./Causal_Search_Experiment/output/nonlinear2/loss.png" width="50%">  

That the effects would be removed in order from smallest to largest,
In this case, we remove up to a causal effect of 0.498 or less.

<img src="./Causal_Search_Experiment/output/nonlinear2/Digraph.png" width="50%">  


For reference, try [abpnl](https://github.com/rafcc/abpnl) and get the following results  
<img src="./images/dag.png" width="20%">  

 $`z \rightarrow y`$ This is completely wrong and backwards.

**I think it's a problem that we are currently relying on such a somewhat sneaky method.**  

---


## dataset
- **fMRI_sim1.csv , fMRI_sim2.csv**  
fMRI simulation data 
https://www.fmrib.ox.ac.uk/datasets/netsim/index.html
(Smith et al., 2011).   

- fMRI_sim1  
<img src="./images/image14.png" width="20%">  

- fMRI_sim2  
<img src="./images/image15.png" width="20%">  


--- 
<img src="./images/image12.png" width="25%">   

In the test, f1 and f2 are not entered because we want to test whether the correct causal structure can be estimated even with unobserved data.  


- **LiNGAM_latest3.csv**  
<img src="./images/LiNGAM_latest3.png" width="60%">  

- **nonlinear_LiNGAM_latest3a.csv**  
<img src="./images/nonlinear_LiNGAM_latest3a.png" width="60%">  
<img src="./images/image16.png" width="20%">  

- **nonlinear_LiNGAM_latest3b.csv**  
<img src="./images/nonlinear_LiNGAM_latest3b.png" width="60%">  
<img src="./images/image17.png" width="20%">  

---    
- **nonlinear_LiNGAM_latest3c.csv**  
<img src="./images/nonlinear_LiNGAM_latest3c.png" width="60%">  
<img src="./images/image18.png" width="20%">  

- **nonlinear.csv**  
<img src="./images/nonlinear.png" width="60%">  

- **nonlinear2.csv**  
<img src="./images/Nonlinear2.png" width="60%">  
[Nonlinear causal discovery with additive noise models](https://proceedings.neurips.cc/paper_files/paper/2008/file/f7664060cc52bc6f3d620bcedc94a4b6-Paper.pdf)

---
## comparison  
The following comparison ignores most of the assumptions made by each algorithm.   
Algorithms that assume linearity of data are given nonlinear data, 
and algorithms that assume no unobserved common variables are given data with unobserved common variables.  
The reason for this seemingly meaningless comparison is that it begs the question, 
“What if the user does not know the algorithm in detail?” In most cases, 
users enter data without considering the assumptions of the algorithm.  
Furthermore, we have noticed that such users tend to evaluate results harshly, 
even if the assumptions of the algorithm are wrong.  

For output edges, one-way edges are counted as 1 and 
bi-directional edges are counted as 1 together.Error counting  method 

- Reverse direction = +1
- Bidirectional edge not where it should be = +1
- Edge not where it should be = +1  

<img src="./images/image30.png" width="100%">  
<img src="./images/image31.png" width="100%">  
<img src="./images/image32.png" width="100%">  

ICA-LiNGAM outputs better results on average, except for
Our methods have yielded relatively good results.  

<img src="./images/image33.png" width="100%">  
<img src="./images/image38.png" width="100%">  
<img src="./images/image39.png" width="100%">  

<img src="./images/image34.png" width="100%">  
<img src="./images/image35.png" width="100%">  
<img src="./images/image36.png" width="100%">  
<img src="./images/image37.png" width="100%">  

Overall, it can be seen that ICA-LiNGAM produces good results on average, regardless of the presence of unobserved common causes and nonlinear relationships.  

## Things to watch out for
These comparison results are for reference only.  
They are for reference only and do not immediately 
imply that one is better than the other.  

The data may be the same, but the adjustable parameters are 
not the same and the assumptions are different.  
It should also be noted that my experimental implementation of the 
results is based on the removal of useless edges due to known 
correct answers.  

However, not done anything to correct the reverse causal direction.  

As for the calculation time, as explained above, the end of the calculation has not yet been determined.  
Therefore, the calculation is continued until the loss is no longer expected to fall, 
so the result adopted as the solution could have been found earlier.   
Therefore, the calculation time has increased considerably due to the excessive 
amount of time required to continue the calculation.

--
## method ICA-LiNGAM  
| data |  Direction reversal|Direction missing|Wasted Edge|  
|---------------------|-------------|----------| ---------|
|fMRI_sim1| 0|0|0|
|fMRI_sim2|2|0|2|
|LiNGAM_latest3|0|2|0|
|nonlinear_LiNGAM_latest3a|0|3|0|
|nonlinear_LiNGAM_latest3b|1|2|1|
|nonlinear_LiNGAM_latest3c|1|0|0|
|nonlinear|1|0|1|
|nonlinear2|0|3|0|

---
## Experiment  
| data |  Direction reversal|Direction missing|Wasted Edge|   
|---------------------|-------------|----------|  ---------|
|fMRI_sim1| 0|0|0|
|fMRI_sim2|0|0|0|
|LiNGAM_latest3|0|0|3|
|nonlinear_LiNGAM_latest3a|0|0|3|
|nonlinear_LiNGAM_latest3b|0|0|5|
|nonlinear_LiNGAM_latest3c|0|0|5|
|nonlinear|0|0|0|
|nonlinear2|0|0|0|


A wasted edge is an edge that could not be deleted because deleting that edge would cause other valid edges to disappear.  

---

---
## requirements
- [pytorch(libtorch) > 2.5.0](https://pytorch.org/)
- [ >= R-4.2.3](https://www.r-project.org/)
- [gnuplot](http://www.gnuplot.info/)
- [Graphviz](http://www.graphviz.org/)
- [Rtools](https://cran.r-project.org/bin/windows/Rtools/history.html)  
※Rtools must match R version  

## Modifications required to run in your environment  
Please modify the init.bat according to the installation location and version of R.  
Describe the bus where **gnuplot** is installed in ``Causal_Search_Experiment/bin/gnuplot_path.txt``  
Describe the bus where **graphviz** is installed in ``Causal_Search_Experiment/bin/graphviz_path.txt``


## build  
When installed, the pre-built binary files are also automatically placed in bin.  
To rebuild it yourself, simply rebuild the following and overwrite bin with the generated binaries  

[Statistical_analysis](https://github.com/Sanaxen/Statistical_analysis)  
https://github.com/Sanaxen/Statistical_analysis/tree/master/example/LiNGAM  
build :**Release_pytorch** binary:**LiNGAM_cuda.exe**

[cpp_torch](https://github.com/Sanaxen/cpp_torch)  
buld : project **rnn6** binary:**rnn6.dll**

---  


<!--
## command line option
Command_Line_Options.md  
[command line option](https://github.com/Sanaxen/Causal_discovery-Experiment/blob/main/Command_Line_Options.md)
-->


# Command Line Options

|  | Command Line Option|Description | Number of Arguments | Details | Default |
|---------------------|-------------|----------|---------------------|---------|---------|
|  | --csv | CSV file name | 1 | Mandatory |  |
|  | --header | 0 or 1 | 0-1 | If a header (column name) exists, set to 1 | 0 |
|  | --col | Number | 0-1 | Number of columns to skip (starting from the first column) | 0 |
|  | --iter | Number | 0-1 | Maximum iterations for convergence in independent component analysis | 1000000 |
|  | --lasso | LASSO parameter | 0-1 | Prune edges using LASSO regularization (LASSO parameter) | 0 |
|  | --sideways | 0 or 1 | 0-1 | Set to 1 for a horizontal diagram | 0 |
|  | --output_diaglam_type | File extension | 0-1 | File extension for diagram output | png |
|  | --diaglam_size | Number | 0-1 | Scaling factor for diagram output size | 20 |
|  | --x_var | Column name | Variable | Explanatory variable column name or index |  |
|  | --y_var | Column name | Variable | Target variable column name or index |  |
|  | --ignore_constant_value_columns | 0 or 1 | 0-1 | Specify 1 to ignore items consisting of only a few fixed values, such as constant values or categorical values. | 0 |
|  | --unique_check_rate | numeric1 | 0-1 | If the pattern of values is less than the data rows or the difference between the maximum and minimum values is within the specified value, it is considered a categorical value.<br>Jittering is performed for categorical variables | 0 |
|  | --error_distr | 0 or 1 | 0-1 | Set to 1 to perform residual analysis and output error_distr.csv | 1 |
|  | --error_distr_size | Number,Number | 0-1 | Size (scaling factor) for residual analysis result images (height and width) | 1,1 |
|  | --min_cor_delete | Value > 0 | 0-1 | Remove relationships with correlation (absolute value) below this value | -1 |
|  | --min_delete | Value > 0 | 0-1 | Remove relationships with causal effects (absolute value) below this value | -1 |
|  | --cor_range_d | Value > 0 | 0-1 | Lower bound of correlation range for relationship output | 0 |
|  | --cor_range_u | Value > 0 | 0-1 | Upper bound of correlation range for relationship output | 0 |
|  | --lasso_tol | Value | 0-1 | Convergence threshold for LASSO pruning | 0.0001 |
|  | --lasso_itr_max | Number | 0-1 | Maximum iterations for LASSO pruning convergence | 10000 |
|  | --load_model | Model file name | Optional | Reevaluate using precomputed data without causal search calculations |  |
|Experiment  | --prior_knowledge | Prior knowledge data | Optional | Specify prior causal knowledge |  |
|Experiment  | --prior_knowledge_rate | 1 ≥ Value > 0 | 0-1 | Accuracy of prior causal knowledge | 1 |
|  | --pause | 0 or 1 | 0-1 | Prevent console from closing after execution by setting to 1 | 0 |
|  | --normalize_type | 0, 1, or 2 | 0-1 | Normalize (1), standardize (2), or keep data as is (0) | 0 |
|  | --min_delete_srt | Number | 0-1 | Remove variables with causal effects smaller than the specified number of top variables | 0 |
|  | --use_adaptive_lasso | 0 or 1 | 0-1 | Use adaptive LASSO for variable selection in LASSO | 1 |
|  | --R_cmd_path |R path |Optional |  "R path" CMD BATCH --slave --vanilla  script.r |  |
|  | --layout | graphviz layout option |  dot,circo,osage,sfdp,twopi | dot |
|  | --plot_max_loss | Number | Y maximum| loss plot( gnuplt) Y axis max value|2.0|
|Experiment  | --independent_variable_skip | 0 or 1  |  0-1 | 0 |
|Experiment  | --unique_check_rate | 0 or 1  | Number of unique elements  > all size*unique_check_rate -> category| 0.1 |
|||||||
|Experiment   with unobserved variables  | --confounding_factors | 0 or 1 | 0-1 | Set to 1 for latent common variable calculations | 0 |
|Experiment  with unobserved variables  | --mutual_information_cut | Value | 0-1 | Cut edges using mutual information threshold | 0 |
|Experiment  with unobserved variables  | --mutual_information_values | 0 or 1 | 0-1 | Set to 1 to output mutual information values between variables in the graph | 0 |
|Experiment  with unobserved variables  | --distribution_rate | Value > 0 | 0-1 | Multiply this value to generate distribution for μ | 1 |
|Experiment  with unobserved variables  | --temperature_alp | 1 > Value > 0 | 0-1 | Coefficient for probabilistic transitions in optimization | 0.95 |
|Experiment  with unobserved variables  | --rho | Value > 0 | 0-1 | Distribution parameter $`rho`$ range (12 times the specified value is set as the mean of μ distribution) | 3 |
|Experiment  with unobserved variables  | --bins | Value > 0 | 0-1 | Number of bins for mutual information integration | 30 |
|Experiment  with unobserved variables   | --early_stopping | Number | 1 | Stop calculations when optimization loss does not change for the specified iterations |  |
|Experiment  with unobserved variables  | --use_intercept | 0 or 1 | 0-1 | Include intercept term in regression results if set to 1 | 0 |
|Experiment  with unobserved variables  | --loss_data_load | 0 or 1 | 0-1 | Load loss data from model generation when loading a model | 0 |
|Experiment  with unobserved variables & nonlinear| --nonlinear | 0 or 1 | 0-1 | Applying nonlinear models | 0 |
|Experiment  with unobserved variables & nonlinear | --use_gpu | 0 or 1 | 0-1 |using pytorch to estimate a nonlinear model. Does it use GPU for computation? | 0 |
|Experiment  with unobserved variables & nonlinear | --activation_fnc | activation fucntion name|  SELU,tanh,leakyrelu,relu,mish |Specify activation function | tanh |
|Experiment  with unobserved variables & nonlinear | --use_hsic |  0 or 1 |  0-1 |Should HSIC be used to calculate independence? | 0 |
|Experiment  with unobserved variables & nonlinear| --use_pnl | 0 or 1 | 0-1 | Use PNL for nonlinear models? | 0 |
|Experiment  with unobserved variables & nonlinear| --learning_rate | Number | 0-1 | learning_rate| 0.001 |
|Experiment  with unobserved variables & nonlinear| --n_unit | Number | 1 | Number of units for fully-connected layer|  |
|Experiment  with unobserved variables & nonlinear| --n_epoch | Number | 1 | Number of epochs| 20 |
|Experiment   with unobserved variables & nonlinear| --optimizer | optimizer name | rmsprop,adam,adagrad,sgd | optimizer| rmsprop |
|Experiment   with unobserved variables & nonlinear| --minbatch | Number | 1 | minbatch size, 0or1->row, min(2000,row)|  row/5|
|Experiment  with unobserved variables & nonlinear| --dropout_rate | Number | 0-1 | dropout rate| 0.01 |
|Experiment  with unobserved variables & nonlinear| --view_confounding_factors | 0 or 1 | 0-1 |Set to 1 if you want estimated unobserved common variables to be plotted. | 0 |
|Experiment  with unobserved variables & nonlinear| --confounding_factors_upper2 | Number | 0-1 |A lower bound on the estimated causal effect of unobserved common variables.
Causal effects below this bound are not considered to be unobserved common variables. | 0.05 |
|Experiment  with unobserved variables & nonlinear| --u1_param | Number | 0-1 | | 0.001 |
|Experiment  with unobserved variables & nonlinear| --L1_loss | 0 or 1 | 0-1 | 1:use torch.nn.L1Loss | use torch.nn.MSELoss |
|Experiment  with unobserved variables & nonlinear| --random_pattern | 0 or 1 | 0-1 |Randomly generate substitution patterns for the B matrix? | 0 |
|Experiment  with unobserved variables & nonlinear| --_Causal_Search_Experiment | 0 or 1 | 0-1 | | 0 |
|  | --@ | Response file name | 0-1 | Specify a file describing command-line options (first character in the file must be blank) |  |
|||||||
---

| solver type | option | note|
|------------|-------------|--|
|ICA-LiNGAM|--confounding_factors 0|This is regular ica LiNGAM.|
|Finding causal relationships while allowing for unmeasured confounding factors, <br>but assuming that all relationships are **linear**|--confounding_factors 1||
|Find causal relationships while accounting for unmeasured confounding factors,  <br>without the need to assume that relationships are **nonlinear or linear**|--confounding_factors 1 <br> --nonlinear 1||
|It finds causal relationships without assuming that relationships are **nonlinear or linear**,<br> assuming there are no unmeasured confounding factors.|--confounding_factors 1 <br> --nonlinear 1<br> --confounding_factors_upper2 100<br>--u1_param 0.00001|This can be done by setting a large value for confounding_factors_upper2 <br>and<br> a small value for u1_param.|
|Plot estimated unobserved confounders in a graph|--view_confounding_factors 1<br>--confounding_factors 1||
|||||||



## reference document  
- https://www.ds.shiga-u.ac.jp/inga/
- https://www.jst.go.jp/kisoken/aip/result/event/jst-riken_sympo2021/pdf/shimizu.pdf
- https://www.socialpsychology.jp/seminar/pdf/2016SS_SShimizu.pdf  
- https://github.com/cdt15/lingam
- https://github.com/rafcc/abpnl
- S. Shimizu, P. O. Hoyer, A. Hyv舐inen, and A. Kerminen. A linear non-gaussian acyclic model for causal discovery. Journal of Machine Learning Research, 7: 2003--2030, 2006. [PDF]
- S. Shimizu, T. Inazumi, Y. Sogawa, A. Hyv舐inen, Y. Kawahara, T. Washio, P. O. Hoyer and K. Bollen. DirectLiNGAM: A direct method for learning a linear non-Gaussian structural equation model. Journal of Machine Learning Research, 12(Apr): 1225--1248, 2011.
- Y. Zeng, S. Shimizu, H. Matsui, F. Sun. Causal discovery for linear mixed data. In Proc. First Conference on Causal Learning and Reasoning (CLeaR2022). PMLR 177, pp. 994-1009, 2022. 
- T. N. Maeda and S. Shimizu. RCD: Repetitive causal discovery of linear non-Gaussian acyclic models with latent confounders. In Proc. 23rd International Conference on Artificial Intelligence and Statistics (AISTATS2020), Palermo, Sicily, Italy. PMLR 108:735-745, 2020. 
- T. N. Maeda and S. Shimizu. Causal additive models with unobserved variables. In Proc. 37th Conference on Uncertainty in Artificial Intelligence (UAI). PMLR 161:97-106, 2021.
- Diviyan Kalainathan et.al., Structural Agnostic Modeling: Adversarial Learning of Causal Graphs
- A Multivariate Causal Discovery based on Post-Nonlinear Model, CLeaR 2022
- Estimation Of Post-Nonlinear Causal Models Using Autoencoding Structure, ICASSP 2020


