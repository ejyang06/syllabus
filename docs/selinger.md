# Selinger optimizer walkthrough

R join S join T on the same key

Statistics

        C: 1000 pages
        D: 10 pages
        E: 10000 pages
        selectivity of E on join key: 1 / 10000
        primary index of E on join key
        fanout: 100
        fillfactor: 100%

Partial run through of Selinger algorithm, assuming nested loops only.
Cost in Disk IO


### Iteration 1


        S = { C }
        bestcost(S) = try each possible A, compute the cost, and pick the cheapest

            A = C

              cost of S-A join A:
                      {}  join C
              costs:   1 + 3 + 2
              
              1. bestjoin({}) = 0
              2. C has no indexes, so seq scan cost
                 1000 pages
              3. join is meaningless = 0

              1 + 2 + 3 =  1000 pages

            A = C is cheapest

        S = { D }
        bestcost(S) = 10 pages (same as S = {C})

        
        S = { E }
        bestcost(S) = 

            A = E

              cost of S-A join A:
                      {}  join E
              costs:   1 + 3 + 2
              
              1. bestjoin({}) = 0
              2. E has index on join key
                 fanout = 100
                 index height = log_100 (10,000) = 2
                 cost to access a value is 3 disk IOs  
              3. join is meaningless = 0

              1 + 2 + 3 =  3 pages

            A = E is cheapest



### Iteration 2

        S = { C, D }
        bestjoin(S) =  11010

          A = C

            cost of S-A join A:
                    {D} join C
            costs:   1 + 3 + 2
            
            1. bestjoin({D}) = 10 (precomputed)
            2. 1000
            3. nested loops is M + M*N.  
               1000 + 1000 * 10

            cost: 10 + 1000 + 1000 + 1000*10 = 12010


          A = D

            cost of S-A join A:
                    {C} join D
            costs:   1 + 3 + 2
            
            1. bestjoin({C}) = 1000 (precomputed)
            2. 10
            3. nested loops is M + M*N.  
               10 + 10 * 1000 

            cost: 10 + 1000 + 10 + 1000*10 = 11010

          A = D is cheapest

           



        S = { C, E }
        bestjoin(S) = 5003

          A = C

            cost of S-A join A:
                    {E} join C
            costs:   1 + 3 + 2
            
            1. bestjoin({C}) = 3 (precomputed)
            2. 1000
            3. index on outer doesn't really help
               10000 + 10000 * 1000

            cost: 1000 + 3 + 10000 + 10000 * 1000 = 10011003


          A = E

            cost of S-A join A:
                    {C} join E
            costs:   1 + 3 + 2
            
            1. bestjoin({C}) = 1000 (precomputed)
            2. 3
            3. primary key index, very low selectivity, can use index nested loops
               M + M * (index lookup cost)
               1000 + 1000 * 3

            cost: 1000 + 3 + 1000 + 1000*3 = 5003

          A = E is cheapest



### Iteration 3

        S = { C, D, E }
        bestjoin(S) = 

          A = D

            cost of S-A   join A:
                    {C,E} join D
            costs:   1 +   3 + 2
            
            1. bestjoin({C}) = 5003 (precomputed)
            2. 10
            3. nested loops
               5003 + 5003 * 10 = 55033

