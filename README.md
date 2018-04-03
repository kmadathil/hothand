# hothand

Inspired by Joshua B. Miller's [tweet](https://twitter.com/jben0/status/980308385038872577), and the [paper by Miller and Sanjurjo](http://www.econ.pitt.edu/sites/default/files/Miller.%20Gambler's%20hot%20hand..pdf) discussing the Hot Hand Fallacy that I'd read about earlier in Kahnemann's [book](https://www.goodreads.com/book/show/11468377-thinking-fast-and-slow)

hothand simulates a series of basketball shooters who hit/miss their target at random with a defined probability. Given a pseudo-hot-hand (simulated as a series of shooters on the left of the current shooter all hitting), we compute the probability of the current shooter hitting.

In Miller's formulation (as in the above tweet), the answer is not 50%! That is an interesting result. Using this simulator, we see that his calculations are right (as we'd expect). 

We can also see that in a *different* formulation, the answer does become 50% as we'd expect. If we sample over all possible shooting streaks of at least 3 - by using an ensemble average, rather than an average of per iteration averages, we do get 50%. It's thus important to think of which way sampling happens in real life situations that are analogous to the hot hand problem.

## Usage
```
$ python hothand.py --help
usage: hothand.py [-h] [--n N] [--p P] [--trials TRIALS]

Plot Raman Spectrum

optional arguments:
  -h, --help       show this help message and exit
  --n N            Number of shooters
  --p P            Probability of hitting a shot
  --trials TRIALS  Number of trials

```
For example:
```
$ python hothand.py --n 12 --p 0.5 --trials 100000
Shooting simulation done 2018-04-03 18:41:23.297856
Colour assignment done 2018-04-03 18:42:15.764607
End 2018-04-03 18:42:16.106235
Per Run:
Red     35.021281
Blue    64.966296
Grey    49.972699
dtype: float64
Ensemble:
          shots    hits  percentage
Red     112508   56265   50.009777
Blue    112834   56351   49.941507
Grey    974658  486989   49.965116
Total  1200000  599605   49.967083

```
As can be seen - sampled over iterations, with each iteration equally likely to happen (and hence hot hands from it%erations with more hot hand streaks being less likely to be sampled), the probablity of a shot being hit, conditional to a hot hand seen prior, is close to 35%.

However, sampled uniformly over the ensemble, with each hot hand equally likely to be seen, we have a 50% probability. 

