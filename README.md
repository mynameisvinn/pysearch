# Anatomy of Search Engine
Bare bones implementation of search.

## Crawl
* the goal of crawling is to create an inverted index.
* at google, web crawling (downloading of web pages) is executed by several distributed crawlers.
* typical time for a single http request/response is ~500ms. this includes dns lookup, tcp connection, request over connection, wait for response, close the response. [math](https://www.quora.com/How-fast-should-network-request-response-normally-take-from-server-to-server). crawlers could maintain its own DNS cache so it does not need to do a DNS lookup before crawling each document.
* In order to speed things up and not wait for each request, you’ll need to make your crawler multi-threaded. This allows the CPU to stay busy working on one response or another, even when each request is taking several seconds to complete. each crawler keeps ~200 connections open at once. [threads](https://blog.hartleybrody.com/scrape-amazon/#code)
* there are 4.48 billion pages according to [w](http://www.worldwidewebsize.com/). 
* duplicates. duplicates are not a problem - they are easy to identify by standard checksumming techniques. a more difficult problem is the identification of near-duplicate documents (eg difer in advertisements, timestamps). eliminating of near-duplicates saves network bandwidth, reduces storage costs and improves search quality. [simhash](http://www.wwwconference.org/www2007/papers/paper215.pdf) is the best solution.
* limit to thread creation: a Python thread costs around 50k of memory, and starting tens of thousands of threads causes failures. If we scale up to tens of thousands of simultaneous operations on concurrent sockets, we run out of threads before we run out of sockets. Per-thread overhead or system limits on threads are the bottleneck. [source](http://aosabook.org/en/500L/a-web-crawler-with-asyncio-coroutines.html)

## Index
* disk seek requires ~5.5ms to complete. so keeping index in memory is important.

## Search

* The final step in building a search engine is creating a system to rank documents by their relevance to the query. This is the most challenging part, because it doesn’t have a direct technical solution: it requires some creativity, and examination of your own use case.
* usually combination of document similarity (tf idf) and pagerank [source](https://stackoverflow.com/questions/10692752/advantages-page-rank-has-over-tf-idf)

### tf-idf
* TF-IDF is used to give a document a score based upon some query. The score changes based upon the query, and without a query there is no score.

### pagerank
* once a set of results is returned for a given query, results must be sorted. we sorted the hits according to PageRank.
* PageRank assigns a score to a document based upon the documents it links to, and the documents which link to it. The score does not vary depending on the query used (i.e. it is a global ranking scheme).