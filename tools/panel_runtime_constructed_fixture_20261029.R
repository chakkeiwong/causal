# Authored constructed-object fixture using installed R; no acquired code sourced.
args <- commandArgs(trailingOnly=TRUE)
stopifnot(length(args)==1)
out <- args[[1]]
stopifnot(!file.exists(out))
X <- rbind(c(1,0),c(0,2),c(0,0),c(0,0))
colnames(X) <- c("a","b")
fit <- glm.fit(x=X,y=c(1,2,1,-1),family=gaussian(),intercept=FALSE)
class(fit) <- "glm"
# Deliberately supply a coherent pivoted triangular factor and original-order coefficients.
fit$qr <- structure(list(qr=diag(c(2,1)),pivot=c(2L,1L),rank=2L),class="parglmqr")
vc <- vcov(fit,dispersion=1)
aligned <- vc[colnames(X),colnames(X),drop=FALSE]
score <- matrix(c(1,0),nrow=1,dimnames=list(NULL,colnames(X)))
raw_quad <- drop(score %*% vc %*% t(score))
aligned_quad <- drop(score %*% aligned %*% t(score))
stopifnot(identical(rownames(vc),c("b","a")),
          identical(diag(vc),c(b=.25,a=1)), raw_quad==.25, aligned_quad==1)
lines <- c("Scope: constructed glm object; not native parglm or fastdid execution.",
           R.version.string,paste("stats version:",packageVersion("stats")),
           paste("covariance row order:",paste(rownames(vc),collapse=",")),
           paste("unaligned score quadratic:",raw_quad),paste("aligned score quadratic:",aligned_quad),
           "No claim that fastdid's default LINPACK path produces this full-rank pivot.",
           "Installed method bodies follow:",capture.output(print(stats:::summary.glm)),
           capture.output(print(stats:::vcov.glm)),capture.output(print(stats:::.vcov.aliased)),
           capture.output(print(stats:::qr.lm)))
writeLines(lines,out)
cat("Constructed covariance-order fixture passed; .25 versus1 under declared pivot.\n")
