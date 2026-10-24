## OpenGM requires an explicit optimization and inference contract

The pinned historical OpenGM source is a reference for separating factor
representation, algebra and algorithms. Its README declares the project
unmaintained; CMake declares version 2.3.1 and optional solver dependencies.
The genuine 2012 paper explains the design, not current operational support.
The proposal retains a reference choice and a conditional isolated worker.
Complete binary rights and a maintenance owner remain prerequisites.
\citep{exec24_opengm_source,exec24_opengm_paper,exec24_opengm_choice}

An authored joint-mode example shows that selecting a component of the most
probable joint state can disagree with the best marginal decision. In the
illustrative 10,000-case portfolio at 100 USD per error, the difference is
200,000 USD. A second finite example shows an early search incumbent of four
against a complete optimum of zero. The selected brute-force source can
return NORMAL after visitor cancellation, so the wrapper needs an independent
termination and completion record. These are exact mathematical and source
witnesses, not observed native failures.
\citep{exec24_opengm_source,exec24_opengm_choice}

Public tests should distinguish probability, energy optimization and causal
queries; preserve factor axes and repeated-evidence semantics; and test
infinite penalties, invalid values, bounds and incomplete results. A proposed
CLI/MCP worker must retain these distinctions. Hypothetical expenditure of
18,000 USD over 600 submitted, 450 completed and 300 qualified requests gives
30, 40 and 60 USD respectively. No downloaded code was executed; current
support, native qualification and actual bank value remain open.
\citep{exec24_opengm_choice}
