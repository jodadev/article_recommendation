# Overview

The Machine Learning branch used in this app is Reinforcement Learning. The problem at glance is the k-Armed Bandit. The agent is tasked with a continuous task of identifying the user's preference for articles based on their assigned tag, then recommends an article with that tag at random. The base route of this site('/') will select an action from the ML API, which maps to a tag, then use it to filter out articles with this tag and randomly select an article to display on the page under "Recommended Article". The user may select "Like" or "Ignore" for the current article being displayed. This sends a signal to the ML API about the current article's tag, and user selection. The agent receives feedback (reward or punishment) and learns from this time-step. Results will return and be displayed of this time-step along with a new recommended article. Over time, the AI will learn what tag the user prefers and use this tag to find an article to recommend. The Agent will exploit its current knowledge(use the Q-Table) but occasionally explore(randomly select a tag) - this will be viewed as articles being recommended based on a tag with the highest Q-Value, let's say "Health", but every once in a while the Agent will show an article with a different tag to see if the user prefers something different, let's say "Tech". The agent will continue to adapt to the users selections and what articles the user prefers, forever.

Note: a limit is placed on the number of requests you may make when providing input including the base route. Current rate is 25 requests with a minute cool down.

## Findings

First I tried IA(Incremental Averaging) to learn and UCB(Upper Confidence Bound) for action selection but since the action_counts array will grow infinitly, I decided to I switch to GBA(Gradient Bandit Average). However, I ran into the same issue of data growing infinitly - this included time-step, H(preference table) and total rewards.

Finally, I used ERWA(Exponential Recency-Weighted Average) to help track changes in non-stationary environment and e-greedy for action selection. This will void using any other data tracking structures that grows to infinity, tracks non-stationary and is able to learn user's article preferences but still explore. The alpha(0.1) and epsilon(0.2) were variables using decay function but are now constants.

## Web App

The web app, both back and front end, was made with a simplistic approach to have a working example. The focus of this project is the API - Machine Learning scripts and the study of the Multi-Armed Bandit Problem with an attempt at solving an Article Recommedation problem.

## My Info

```text
[Portfolio Website](https://www.jodadev.com/)
```

```text
[Twitter](https://www.twitter.jodadev2/)
```
