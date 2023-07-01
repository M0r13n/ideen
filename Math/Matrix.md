- rectangular array of values (numbers, symbols or expressions)
- arranged in rows and columns
- used to represent a mathematical object or a property of such object

$$
\begin{equation*}
A = 
\begin{pmatrix}
1 & 2 \\
4 & 5 \\
7 & 8 
\end{pmatrix}
\end{equation*}
$$
- is a "three by two matrix" or a matrix of dimension $3 \times 2$
- a matrix with _m_ rows and _n_ columns is called an $m \times n$ matrix, or _m_-by-_n_ matrix
- boxed brackets and rounded parentheses typically mean the same
- $a_{i,j}$ refers to the entry $i<=m$ and $j<=n$ at the i-th row and j-th colum
- $a_{3,1}$ refers to the value $8$ in the above matrix

## Addition

$A+B$ of two $m \times n$ matrices the result is calculated entrywise:

$A_{i,j} + B_{i,j}$ where $1<=i<=m$ and $1<=j<=n$

$$
\begin{equation*}
\begin{pmatrix}
1 & 2 \\
4 & 5 \\
7 & 8 
\end{pmatrix}
+
\begin{pmatrix}
1 & 4 \\
2 & 5 \\
3 & 6 
Matrix
=
\begin{pmatrix}
2 & 6 \\
6 & 10 \\
10 & 14 
\end{pmatrix}
\end{equation*}
$$


## Scalar Multiplication

The product of $c \cdot A$  is computed by multiplying every entry with $c$:
$c \cdot A_{i,j}$

$$
\begin{equation*}
2 \cdot
\begin{pmatrix}
1 & 2 \\
4 & 5 \\
7 & 8 
\end{pmatrix}
=
\begin{pmatrix}
2 \cdot 1 & 2 \cdot 2 \\
2 \cdot 4 & 2 \cdot 5 \\
2 \cdot 7 & 2 \cdot 8 
\end{pmatrix}
=
\begin{pmatrix}
2 & 4 \\
8 & 10 \\
14 & 16 
\end{pmatrix}
\end{equation*}
$$
## Transposition
 
The _transpose_ of an _m_-by-_n_ matrix **A** is the _n_-by-_m_ matrix $A^T$ formed by turning rows into columns and vice versa:

$(A^{T})_{i,j}= A_{j,i}$

$$
\begin{equation*}
\begin{pmatrix}
1 & 2 \\
4 & 5 \\
7 & 8 
\end{pmatrix}^T
=
\begin{pmatrix}
1 & 4 & 7 \\
2 & 5 & 8
\end{pmatrix}

\end{equation*}
$$

## Matrix Multiplication

_Multiplication_ of two matrices is defined if and only if the number of columns of the left matrix is the same as the number of rows of the right matrix. If **A** is an _m_-by-_n_ matrix and **B** is an _n_-by-_p_ matrix, then their _matrix product_ $A \times B$  is the _m_-by-_p_ matrix whose entries are given by dot product of corresponding row of **A** and column of **B**:

![example that shows how to compute the product of two matrices](https://upload.wikimedia.org/wikipedia/commons/e/e5/MatrixMultiplication.png)


$$
\begin{equation*}
A = 
\begin{pmatrix}
1 & 2 \\
4 & 5 \\
7 & 8 
\end{pmatrix}
\begin{pmatrix}
1 & 2 & 3\\
4 & 5 & 6
\end{pmatrix}
=
\begin{pmatrix}
9 & 12 & 15\\
24 & 33 & 42\\
39 & 54 & 69
\end{pmatrix}
\end{equation*}
$$

## Hadamard Product
For two matrices A and B of the same dimensions $m \times n$ the Hadamard product is defined as:

$A \odot B = A_{i,j} \cdot B_{i,j}$

$$
\begin{equation*}
A = 
\begin{pmatrix}
1 & 2 \\
4 & 5 \\
7 & 8 
\end{pmatrix}
\begin{pmatrix}
9 & 8 \\
7 & 6 \\
5 & 4 
\end{pmatrix}
=
\begin{pmatrix}
1 \cdot 9 & 2 \cdot 8 \\
4 \cdot 7 & 5 \cdot 6 \\
7 \cdot 5 & 8 \cdot 4 \\
\end{pmatrix}
\end{equation*}
$$

