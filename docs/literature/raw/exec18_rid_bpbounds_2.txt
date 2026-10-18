#' Nonparametric Bounds for the Average Causal Effect due to Balke and Pearl.
#'
#' @param p Object of class "table" containing either cell counts or conditional
#' probabilities. For trivariate data these are for the
#' phenotype/treatment-outcome association given Z, i.e. P(X, Y | Z).
#'
#' Cell counts could be generated from `xtabs(~ x + y + z, data = data)`.
#' And then conditional probabilities obtained by calling
#' `prop.table(..., margins = 3)` on your object from `xtabs()`.
#'
#' If you only know the conditional probabilities you can enter these, e.g.
#' for the Balke and Pearl Vitamin A example:
#' ```r
#' cp   <- c(.0064, 0, .9936, 0, .0028, .001, .1972, .799)
#' tabp <- as.table(array(
#'   cp,
#'   dim = c(2, 2, 2),
#'   dimnames = list(
#'     x = c(0, 1),
#'     y = c(0, 1),
#'     z = c(0, 1)
#'   )
#' ))
#' ```
#' And then call `bpbounds()` using this object.
#'
#' For bivariate data this object contains cell conditional probabilities for
#' the outcome-instrument (Y|Z) association.
#' @param t Specified for bivariate data. Object with
#' treatment/phenotype-instrument cell counts or conditional probabilities,
#' i.e. (X|Z).
#' @param fmt A character string which should be either "bivariate"
#' (i.e. X, Z in one dataset and Y, Z in another dataset) or
#' "trivariate" (X, Y, Z in the same dataset).
#' @export
#' @return List with the following elements:
#' \describe{
#' \item{fmt}{whether the data is bivariate or trivariate}
#' \item{nzcats}{2 or 3, the number of instrument categories}
#' \item{inequality}{Logical, indicating whether the IV inequality is satisfied}
#' \item{bplb}{Lower bound of ACE}
#' \item{bpub}{Upper bound of ACE}
#' \item{bplower}{Vector of lower bound probabilities}
#' \item{bpupper}{Vector of upper bound probabilities}
#' \item{p11low}{Lower bound of P(Y=1|do(X=1))}
#' \item{p11upp}{Upper bound of P(Y=1|do(X=1))}
#' \item{p10low}{Lower bound of P(Y=1|do(X=0))}
#' \item{p10upp}{Upper bound of P(Y=1|do(X=0))}
#' \item{p11lower}{Vector of probabilities for lower bound of P(Y=1|do(X=1))}
#' \item{p11upper}{Vector of probabilities for upper bound of P(Y=1|do(X=1))}
#' \item{p10lower}{Vector of probabilities for lower bound of P(Y=1|do(X=0))}
#' \item{p10upper}{Vector of probabilities for upper bound of P(Y=1|do(X=0))}
#' \item{crrlb}{Lower bound of CRR}
#' \item{crrub}{Upper bound of CRR}
#' \item{monoinequality}{Logical, indicating whether the monotonicity inequality
#' is satisfied}
#' \item{monobplb}{Lower bound of ACE assuming monotonicity}
#' \item{monobpub}{Upper bound of ACE assuming monotonicity}
#' \item{monobplower}{Vector of probabilities for lower bound of ACE assuming
#' monotonicity}
#' \item{monobpupper}{Vector of probabilities for upper bound of ACE assuming
#' monotonicity}
#' \item{monop11low}{Lower bound of P(Y=1|do(X=1)) assuming monotonicity}
#' \item{monop11upp}{Upper bound of P(Y=1|do(X=1)) assuming monotonicity}
#' \item{monop10low}{Lower bound of P(Y=1|do(X=0)) assuming monotonicity}
#' \item{monop10upp}{Upper bound of P(Y=1|do(X=0)) assuming monotonicity}
#' \item{monop11lower}{Vector for corresponding bound above}
#' \item{monop11upper}{Vector for corresponding bound above}
#' \item{monop10lower}{Vector for corresponding bound above}
#' \item{monop10upper}{Vector for corresponding bound above}
#' \item{monocrrlb}{Lower bound of CRR assuming monotonicity}
#' \item{monocrrub}{Upper bound of CRR assuming monotonicity}
#' }
#'
#' @examples
#' \donttest{
#' # Vitamin A example, using cell counts
#'
#' require(tidyr)
#' require(bpbounds)
#'
#' tab1dat <- data.frame(
#'   z = c(0, 0, 1, 1, 1, 1, 0, 0),
#'   x = c(0, 0, 0, 0, 1, 1, 1, 1),
#'   y = c(0, 1, 0, 1, 0, 1, 0, 1),
#'   freq = c(74, 11514, 34, 2385, 12, 9663, 0, 0)
#' )
#' tab1inddat <- uncount(tab1dat, freq)
#' xt         <- xtabs(~ x + y + z, data = tab1inddat)
#' p          <- prop.table(xt, margin = 3)
#' bpres      <- bpbounds(p)
#' sbpres     <- summary(bpres)
#' print(sbpres)
#' }
#'
#' \donttest{
#' # Vitamin A example, using conditional probabilities
#'
#' require(bpbounds)
#' cp = c(.0064, 0, .9936, 0, .0028, .001, .1972, .799)
#' tabp = as.table(array(
#'   cp,
#'   dim = c(2, 2, 2),
#'   dimnames = list(
#'     x = c(0, 1),
#'     y = c(0, 1),
#'     z = c(0, 1)
#'   )
#' ))
#' bpbounds(tabp)
#' }
#'
bpbounds <- function(p, t = NULL, fmt = "trivariate") {
  # Check arguments

  ## check fmt specified correctly
  if (fmt != "bivariate" && fmt != "trivariate") {
    stop('fmt argument must be either "bivariate" or "trivariate"')
  }

  ## check t has been specified along with if fmt is bivariate
  if (fmt == "bivariate" && is.null(t)) {
    stop(
      't, a matrix of treatment/phenotype-instrument conditional probabilities, must be specified for bivariate data'
    )
  }

  ## check p of class "table"
  if (!is.table(p)) {
    stop('p must be of class "table"')
  }

  ## check length of p
  if (fmt == "trivariate") {
    if (length(p) != 8 && length(p) != 12) {
      stop("The length of p must be 8 or 12, i.e. for a 2 or 3 category instrument.")
    }
  } else {
    if (length(p) != 4 && length(p) != 6) {
      stop("p seems to have the incorrect number of dimensions")
    }
  }

  ## check length of t
  if (fmt == "bivariate") {
    if (length(t) != 4 && length(t) != 6) {
      stop("t seems to have the incorrect number of dimensions")
    }
  }

  ## check if p conditional probabilities
  #  if (sum(p <= 1) != length(p)) {
  #	  stop('p seems to be a mix of cell counts and probabilities')
  #  }
  if (sum(p <= 1) == length(p)) {
    # already in conditional probabilities
  } else if (all(p == floor(p))) {
    if (fmt == "trivariate") {
      p <- prop.table(p, margin = 3)
    }	else {
      p <- prop.table(p, margin = 2)
    }
  } else {
    stop("All elements of p must either be conditional probabilities or cell counts.")
  }

  ## p should now be conditional probabilities
  ## check they sum to approximately the number of instrument categories
  if (fmt == "trivariate" && length(p) == 8) {
    nzcats <- 2
    if (abs(sum(p) - 2) > 0.1) {
      stop("The conditional probabilities add up to ",
           sum(p),
           " instead of 2.")
    }
  } else if (fmt == "trivariate" && length(p) == 12) {
    nzcats <- 3
    if (abs(sum(p) - 3) > 0.1) {
      stop("The conditional probabilities add up to ",
           sum(p),
           " instead of 3.")
    }
  }

  # check that t is either cell counts or conditional probabilities
  if (sum(t <= 1) == length(t)) {
    # conditional probabilities
  } else if (all(t == floor(t))) {
    # convert to conditional probabilities if cell counts
    if (fmt == "bivariate") {
      t <- prop.table(t, margin = 2)
    }
  } else {
    stop("All elements of t must either be conditional probabilities or cell counts.")
  }

  # Control flow for bivariate or trivariate data
  if (fmt == "bivariate") {
    if (length(p) == 4) {
      cp = numeric(8)
      cp[1] = p[1] # g00
      cp[2] = p[2] # g10
      cp[3] = p[3] # g01
      cp[4] = p[4] # g11
      cp[5] = t[1] # t00
      cp[6] = t[2] # t10
      cp[7] = t[3] # t01
      cp[8] = t[4] # t11
      nzcats <- 2
      bp <- bpbounds_biv_x2y2z2(p = cp)
      bpres = bpbounds_calc_biv_z2(g = p, t = t)
    } else if (length(p) == 6) {
      cp = numeric(12)
      cp[1]  = p[1] # g00
      cp[2]  = p[2] # g10
      cp[3]  = p[3] # g01
      cp[4]  = p[4] # g11
      cp[5]  = p[5] # g02
      cp[6]  = p[6] # g12
      cp[7]  = t[1] # t00
      cp[8]  = t[2] # t10
      cp[9]  = t[3] # t01
      cp[10] = t[4] # t11
      cp[11] = t[5] # t02
      cp[12] = t[6] # t12
      nzcats <- 3
      bp <- bpbounds_biv_x2y2z3(p = cp)
      bpres = bpbounds_calc_biv_z3(g = p, t = t)
    }
  } else if (fmt == "trivariate") {
    if (length(p) == 8) {
      bp <- bpbounds_tri_x2y2z2(p = p)
      bpres = bpbounds_calc_tri_z2(p)
    } else if (length(p) == 12) {
      bp <- bpbounds_tri_x2y2z3(p = p)
      bpres = bpbounds_calc_tri_z3(p)
    }
  }

  # return objects
  retlist <- list(
    "fmt" = fmt,
    "nzcats" = nzcats,
    "inequality" = bp$inequality,
    "bplb" = bp$bplow,
    "bpub" = bp$bpupp,
    "bplower" = bp$bplower,
    "bpupper" = bp$bpupper,
    "p11low" = bpres$p11low,
    "p11upp" = bpres$p11upp,
    "p10low" = bpres$p10low,
    "p10upp" = bpres$p10upp,
    "p11lower" = bpres$p11lower,
    "p11upper" = bpres$p11upper,
    "p10lower" = bpres$p10lower,
    "p10upper" = bpres$p10upper,
    "crrlb" = bpres$crrlb,
    "crrub" = bpres$crrub,
    "monoinequality" = bpres$monoinequality,
    "monobplb" = bpres$monobplb,
    "monobpub" = bpres$monobpub,
    "monobplower" = bpres$monolower,
    "monobpupper" = bpres$monoupper,
    "monop11low" = bpres$monop11lb,
    "monop11upp" = bpres$monop11ub,
    "monop10low" = bpres$monop10lb,
    "monop10upp" = bpres$monop10ub,
    "monop11lower" = bpres$monop11lower,
    "monop11upper" = bpres$monop11upper,
    "monop10lower" = bpres$monop10lower,
    "monop10upper" = bpres$monop10upper,
    "monocrrlb" = bpres$monocrrlb,
    "monocrrub" = bpres$monocrrub
  )
  class(retlist) <- "bpbounds"
  return(retlist)
}


#' @export
summary.bpbounds <- function(object, ...) {
  ans = list()
  bp = object
  ans$fmt             = bp$fmt
  ans$nzcats          = bp$nzcats
  ans$inequality      = bp$inequality
  ans$monoinequality  = bp$monoinequality

  boundscolnames = c("Causal parameter", "Lower bound", "Upper bound")
  causalparameternames = c("ACE", "P(Y|do(X=0))", "P(Y|do(X=1))", "CRR")

  if (bp$inequality) {
    lb = c(bp$bplb, bp$p10low, bp$p11low, bp$crrlb)
    ub = c(bp$bpub, bp$p10upp, bp$p11upp, bp$crrub)
    ans$bounds = data.frame(causalparameternames, lb, ub)
    colnames(ans$bounds) = boundscolnames

    if (bp$monoinequality) {
      monolb = c(bp$monobplb, bp$monop10low, bp$monop11low, bp$monocrrlb)
      monoub = c(bp$monobpub, bp$monop10upp, bp$monop11upp, bp$monocrrub)
      ans$monobounds = data.frame(causalparameternames, monolb, monoub)
      colnames(ans$monobounds) = boundscolnames
    }
  }

  class(ans) <- "summary.bpbounds"
  ans
}


#' @export
print.summary.bpbounds <-
  function(x, digits = getOption("digits"), ...) {
    cat("\n")
    cat("Data:                    ", x$fmt, "\n", sep = "")
    cat("Instrument categories:   ", x$nzcats, "\n\n", sep = "")
    cat("Instrumental inequality:", x$inequality, "\n")
    if (x$inequality) {
      print(x$bounds, digits = digits, row.names = FALSE, ...)
    }
    cat("\nMonotonicity inequality:", x$monoinequality, "\n")
    if (x$monoinequality) {
      print(x$monobounds,
            digits = digits,
            row.names = FALSE,
            ...)
    }
    crrna <- FALSE
    if (!is.null(x$bounds)) {
      crrna <- anyNA(x$bounds[x$bounds[[1]] == "CRR", -1])
    }
    if (!is.null(x$monobounds)) {
      crrna <- crrna || anyNA(x$monobounds[x$monobounds[[1]] == "CRR", -1])
    }
    if (crrna) {
      cat(
        "\nNote: CRR bounds reported as NA are unbounded because the",
        "\ncorresponding bound on P(Y|do(X=0)) is 0.\n"
      )
    }
    cat("\n")
    invisible(x)
  }


#' @export
print.bpbounds <- function(x, digits = getOption("digits"), ...) {
  print(summary(x), digits = digits, ...)
}
