# Intro

The following are examples of problems that you may want to practice with.  I'll supply answers to a subset of the problems at a later date, so you can work out the rest.

These problems are not graded.  Working with others on this is encouraged.


# Indexing Problems

Let's say we have 10,000 records and we create a secondary B+ tree index on the age attribute.  A pointer is 8 bytes, the age takes 4 bytes, a page has size 1k bytes, we enforce a fill factor of 2/3, and ignoring other storage overheads, how many leaf nodes are in the tree?

Let's say my main memory has the following number of pages.  What is the expected number of disk accesses to access a given record?

* 10
* 100
* 1000

Let's say age has 80 distinct values, and no index pages are cached in memory.  How many disk IOs (one per page) would I expect for a predicate of the form `age = CONSTANT`?




# Query Optimization Problems


## Simple Operator Case

Let's say we have the following statistics about the database with table R

        NCARD(R) = 1000
        ICARD(R) = 100
        # pages  = 100
        minmax(a1) = [0, 100]
        default selectivity = 0.1

Assuming no indexes, what is the cost in the number of pages to

1. Read all records in R?
1. Read all records where a1 = 10
1. Read all records where a2 = 10

Again, assuming no indexes, what is the estimated number of tuples where

1. TRUE
1. a1 = 10
1. a2 = 10
1. a1 = 10 AND a2 = 10

Now, assuming we have a b+tree primary index on a1, what is the cost in number of pages to

1. Read all records in R?
1. Read all records where a1 = 10?
1. Read all records where a1 > 50?
1. Read all records where a2 = 10?

Now assuming the b+tree was a secondary index on a1, what is the cost in number of pages to

1. Read all records in R?
1. Read all records where a1 = 10?
1. Read all records where a1 > 50?
1. Read all records where a2 = 10?


# Single Join query case

Let's say you have the following query

        SELECT *
        FROM  R, S
        WHERE R.sid = S.sid 

Where

        NCARD(R) = 1000
        NCARD(S) = 100
        ICARD(R) = 1000
        ICARD(S) = 10
        NPAGES(R) = 100
        NPAGES(S) = 10
        Primary B+Tree on R.bid
        Secondary B+Tree on R.sid


What is the cost, in number of pages read, for executing the following joins, where the left relation is the outer, and the right relation is the inner?


1. R nested loops join S
1. R index nested loops join S
1. S index nested loops join R
1. R merge sort join S


What is

* the selectivity of the query?
* the expected number of results of the above join?  

Now let's take memory into account.  Let's say we have `11` pages of memory, what is the cost, in number of pages _read from disk_ for the following?

1. R nested loops join S
1. R index nested loops join S
1. S index nested loops join R
1. R merge sort join S


Let's say you have the following query, but with the same statistics and indexes as above

        SELECT *
        FROM R, S
        WHERE R.sid = S.sid AND R.bid = 10

What would the Selinger optimizer pick as the best plan?


# Multi Join optimization

Suppose I run the following query

        SELECT *
        FROM R, S, T
        WHERE R.sid = S.sid AND S.sid = T.sid

And I have the following statistics about the relatons

        NCARD(R) = 100
        ICARD(R) = 100
        NCARD(S) = 1000
        ICARD(S) = 1000
        NCARD(T) = 10
        ICARD(T) = 10

Suppose we have no other information, and we have not built any indices, and we only use nested loops join, work through the Selinger optimizer algorithm to

1. report the join orders the algorithm considers (the arguments to bestjoin())
1. compute the selectivity of the query
1. estimate the cardinality of the query result 
1. What is the minimum cost plan?