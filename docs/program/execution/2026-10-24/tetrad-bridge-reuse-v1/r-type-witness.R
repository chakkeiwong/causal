x <- c(1L,2L); stopifnot(is.integer(x), is.numeric(x)); cat(R.version.string,"
"); cat("integer_is_numeric=",is.numeric(x),"
",sep=""); cat("selected_branch=",if(is.numeric(x)) "continuous" else if(is.integer(x)) "discrete" else "other","
",sep="")
