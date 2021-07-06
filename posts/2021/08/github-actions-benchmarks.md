<!--
.. title: Is GitHub Actions suitable for running benchmarks?
.. slug: github-actions-benchmarks
.. date: 2021-08-30 00:01 UTC
.. tags: github-actions, Open-Source, continuous-integration, performance
.. category:
.. link:
.. description:
.. type: markdown
.. author: Jaime Rodríguez-Guerra
-->

Benchmarking software is a tricky business. For robust results, you need dedicated
hardware that only runs the benchmarking suite under controlled conditions. No other
processes! No OS updates! Nothing else! Even then, you might find out that CPU throttling,
thermal regulation and other issues can introduce noise in your measurements.

So, how are we even trying to do it on a CI provider like GitHub Actions?
Every job runs in a separate VM instance with frequent updates and shared resources. It
looks like it would just be a very expensive random number generator.

Well, it turns out that there _is_ a sensible way to do it: **relative benchmarking**.
And we know it works because we have been collecting stability data points for a month.
Go data-driven implementations!

<!-- TEASER_END -->

# Continuous benchmarking on GitHub Actions

* Relative differences are easier to detect. More time consuming, but easier to set-up, less maintenance.

* For scikit-image, we want to be able to detect performance regressions.
* In a PR, this can be measured by benchmarking the submission against the target branch, side-by-side. Both run in the same machine.
* However, during the execution of a CI task, other workers in the same hardware might be polluting the measurements through collateral workloads.
* To make sure GHA is suitable for relative performance assessment, we have set-up a data-driven decision making: set a toy benchmark test and collect data points for different configurations along several days. This should allows to assess how reliable GHA is.

## The setup

* Test two identical commits (different hashes, but same code). Performance ratio should be 1.0 under ideal conditions.
* Run the benchmark suite 4 times a day (every six hours) for a week to account for day/time variations.
* Find a compromise between stability and performance:
    * --interleave-processes: True vs False
    * --processes: 1 vs 2 (this is NOT parallelization, but using two different processes, serially, to collect points in two different passes)

## The findings

* Default configuration (two processes, interleaved) is reliable enough! Here we show the pretty plots for the notebook, which will be linked in a Gist and fully documented.
* Since benchmarks are resource intensive and do not need to run all the time, the PR is triggered with labels. Easier than comments and no auth required!

## Gotchas

* UI can be a bit confusing at first. Label-triggered jobs are aggregated with the last push event that ran; best bet is to go to the Actions panel directly.
* Having a GHA bot post some comment about the triggered run is more complicated than expected and needed! PR permissions and different sets of triggers get in the way HARD.
* We also experimented with several single-process jobs for faster turnaround, but it was too noisy.

## Conclusions

* TLDR: CB on GHA is OK. Acronyms are cool.