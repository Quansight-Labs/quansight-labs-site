<!--
.. title: What's next for PyData/Sparse
.. slug: whats-next-for-pydatasparse
.. date: 2020-02-17 05:11:42 UTC-06:00
.. tags: Sparse, SciPy, NumPy, Tensors, Big data
.. type: text
.. author: Hameer Abbasi
-->

# What have we been doing so far? 🤔
## Research 📚
A lot of behind the scenes work has been taking place on PyData/Sparse. Not so much in terms of code, more in terms of research and community/team building. I've decided more-or-less to use the structure and the research behind the [Tensor Algebra Compiler](https://github.com/tensor-compiler/taco), the work of Fredrik Kjolstad and his collaborators at MIT. 🙇🏻‍♂️ To this end, I've read/watched the following talks and papers:

<!-- TEASER_END -->

* Fredrik Kjolstad, Shoaib Kamil, Stephen Chou, David Lugato, and Saman Amarasinghe. 2017. The tensor algebra compiler. Proc. ACM Program. Lang. 1, OOPSLA, Article 77 (October 2017), 29 pages. DOI:[https://doi.org/10.1145/3133901](https://doi.org/10.1145/3133901)
* Fredrik Kjolstad, Peter Ahrens, Shoaib Kamil, and Saman Amarasinghe. 2018. Sparse Tensor Algebra Optimizations with Workspaces. [https://arxiv.org/abs/1802.10574](https://arxiv.org/abs/1802.10574)
* Chou, Stephen, Fredrik Kjolstad, and Saman Amarasinghe. “Format Abstraction for Sparse Tensor Algebra Compilers.” Proceedings of the ACM on Programming Languages 2.OOPSLA (2018): 1–30. Crossref. Web. [https://arxiv.org/abs/1804.10112](https://arxiv.org/abs/1804.10112)
* Ryan Senanayake, Fredrik Kjolstad, Changwan Hong, Shoaib Kamil, and Saman Amarasinghe. 2019. A Unified Iteration Space Transformation Framework for Sparse and Dense Tensor Algebra [https://arxiv.org/abs/2001.00532](https://arxiv.org/abs/2001.00532)
* Stephen Chou, Fredrik Kjolstad, Saman Amarasinghe. Automatic Generation of Efficient Sparse Tensor Format Conversion Routines. 2019. Automatic Generation of Efficient Sparse Tensor Format Conversion Routines [https://arxiv.org/abs/2001.02609](https://arxiv.org/abs/2001.02609)
* The Sparse Tensor Algebra Compiler [https://www.youtube.com/watch?v=0OP8WjFyU-Q](https://www.youtube.com/watch?v=0OP8WjFyU-Q)
* Format Abstraction for Sparse Tensor Algebra Compilers [https://www.youtube.com/watch?v=sQOq3Ci4tB0](https://www.youtube.com/watch?v=sQOq3Ci4tB0)
* The Tensor Algebra Compiler [https://www.youtube.com/watch?v=yAtG64qV2nM](https://www.youtube.com/watch?v=yAtG64qV2nM)

A bit heavy, so don't feel obliged to go through them. 😉

## Resources 👥
I've also had conversations with Ralf Gommers about getting someone experienced in Computer Science on board, as a lot of this work is very heavy on Computer Science.

## Strategy 🦾
The original TACO compiler requires a compiler at runtime, which isn't ideal for many users. However, what's nice is that we have Numba as a Python package. One, instead of emitting C code, can emit Python AST to be transpiled to LLVM by Numba, and then to machine code. I settled on this after researching Cppyy, which also requires a compiler, and pybind11, which wouldn't work as TACO itself is built to require a compiler.

# API Changes 👨🏻‍💻
I'd also like to invite anyone who's interested into the discussion about API changes. The discussion can be found in [this issue](https://github.com/pydata/sparse/issues/326), but essentially, we're planning on moving to a lazy model for an asymptotically better runtime performance.

# So what does this mean for the user? 😕
Why, support for a lot more operations across a lot more formats, really. 😄 And don't forget the performance. 🚀 With the downstream being lazy operations a-la Dask.
