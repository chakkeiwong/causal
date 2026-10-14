# Project trace of scalar expressions inspected in pcalg 2.7-12.
# This does not load or execute the pcalg package or a downloaded source file.
C <- matrix(1, 3, 3)
raw_r <- (C[1,2] - C[1,3] * C[2,3]) /
         sqrt((1 - C[2,3]^2) * (1 - C[1,3]^2))
stopifnot(is.nan(raw_r))
fallback_r <- if (is.na(raw_r)) 0 else min(.9999999, max(-.9999999, raw_r))
z <- sqrt(20 - 1 - 3) * atanh(fallback_r)
p <- 2 * pnorm(abs(z), lower.tail = FALSE)
stopifnot(is.finite(p), p == 1)
factorization <- try(chol(C), silent = TRUE)
stopifnot(inherits(factorization, "try-error"))
raw_z <- suppressWarnings(sqrt(3 - 1 - 3) * atanh(.2))
stopifnot(is.nan(raw_z))
fallback_z <- if (is.na(raw_z)) 0 else raw_z
bad_df_p <- 2 * pnorm(abs(fallback_z), lower.tail = FALSE)
stopifnot(bad_df_p == 1)
cat('{"scope":"Project scalar trace in base R; pcalg not loaded",',
    '"singular_input_raw_r":"NaN","fallback_r":0,',
    '"finite_p_after_fallback":1,"positive_definite_preflight_rejects":true,',
    '"invalid_df_finite_p_after_fallback":1,',
    '"warning":"These invalid inputs should fail the proposed preflight; no valid-input package failure demonstrated",',
    '"status":"pass"}\n', sep="")
