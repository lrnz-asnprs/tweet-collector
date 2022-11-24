# Thesis writing plan



## Terminology Alignment

+ Twitter API
+ Fake News Users / True News Users? 

## General Style Alignment

+ Always reference the code with links to the specific script file e.g., 
+ reference sections with the function \ref{sec:section_title}
+ Add labels after code snippet, figures, tables, so we can use \ref on them.
    + \label{code:code_snippet_title},
    + \label{fig:figure_title}
    + \label{tbl:table_title}
+ MATH syntax
    + Longer math formulas (not in-text) \[ x < \sqrt{2^{53}/n} \]
    + $ signs etc. for in-text math equation \emph{n} = $2^x$ with $x>0$.
+ use the texttt tag for references to python file or libraries etc. \texttt{your_script.py}



### Example of Code Snippet
\begin{lstlisting}[language=Python, caption={Pipeline from Assignment I. The pipeline comprises various \emph{transformers} and a final \emph{learner} step using \texttt{LinearRegression()}. See Appendix \ref{app:wind_direction_transformer_code_snippet} for details about the \emph{transformer} \texttt{numeric\_wind\_directions()}.}]
pipeline = Pipeline([
    ("wind_direction", numeric_wind_directions()),
    ("std_scaler_specific", ColumnTransformer([
                            ("scaler", StandardScaler(), ["Speed"])],
                            remainder="passthrough")),
    ("imputer", SimpleImputer(strategy="median", copy=False)),
    ("poly", PolynomialFeatures(include_bias=False, degree=5)), 
    ("lin_reg", LinearRegression())
])
\end{lstlisting}
\label{code_in_sec:pipe_line_assignment1_code_in_text}


### Example of Figures

\begin{figure}[H]
    \centering
    \includegraphics[width=10cm]{figures/ml_flow.png}
    \caption{Depiction of the workflow when using the improved version of the pipeline from section \ref{Ch:data_pipeline}, \texttt{GridSearchCV}, and evaluating the results all while tracking and making logs  with \texttt{ML-Flow}. The three steps reflect steps 2, 3, and 4 in the Analytics Lifecycle.}
    \label{fig:workflow_mlflow}
\end{figure}




## Pending Agreement

+ Do we write i.e., or i.e. fx
+ T

















## Thesis template

This is a template for a BSc thesis at ITU. 

For its origin and adoptions, see the header in `thesis-ITU.tex`

Logo retrieved from: https://www.itu.dk/om-itu/presse/logoer

If you use this template and have suggestions to improve it, please make a pull request :)

Here is an example with a BCs thesis https://github.com/ViktorTorp/SemEval2020-TC/blob/master/Propaganda_technique_detection.pdf

Tak
