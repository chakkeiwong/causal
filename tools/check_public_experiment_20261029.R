# Same target, rows, covariates and HC2 convention as the frozen Python study.
root <- '/home/ubuntu/workspace/causal'
out <- file.path(root, 'docs/scientific-gap-closure/2026-10-29')
d <- read.csv(file.path(out, 'analysis-data.csv'))
X <- scale(as.matrix(d[, c('age','educ','black','hisp','marr','nodegree','re74','re75')]))
frame <- data.frame(y=d$re78, a=d$treat, X)
fits <- list(unadjusted=lm(y ~ a, frame),
             common_slope=lm(y ~ ., frame),
             interacted=lm(y ~ a * (age+educ+black+hisp+marr+nodegree+re74+re75), frame))
rows <- lapply(names(fits), function(name) {
  fit <- fits[[name]]
  design <- model.matrix(fit)
  inverse <- solve(crossprod(design))
  weights <- residuals(fit)^2 / (1-hatvalues(fit))
  V <- inverse %*% crossprod(design, weights*design) %*% inverse
  data.frame(method=name, estimate=unname(coef(fit)['a']), variance=V['a','a'],
             standard_error=sqrt(V['a','a']), max_leverage=max(hatvalues(fit)))
})
write.csv(do.call(rbind,rows),file.path(out,'r-comparison.csv'),row.names=FALSE)
capture.output(sessionInfo(),file=file.path(out,'r-session.txt'))
capture.output(stats::lm,stats::lm.fit,getS3method('hatvalues','lm'),stats::model.matrix.default,
               file=file.path(out,'r-functions-inspected.txt'))
capture.output(tools::Rd2txt(utils:::.getHelpFile(help('lm',package='stats'))),
               file=file.path(out,'r-lm-help.txt'))
print(do.call(rbind,rows))
