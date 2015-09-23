Domain constraints

        CREATE TABLE A (
          a int,
          b text,
          c float         
        );
        INSERT INTO A(a,b,c) VALUES (1, '2', 3);
        INSERT INTO A(a,b,c) VALUES (1, 2, 3);
        INSERT INTO A(a,b,c) VALUES (1.5, 4, 5);
        INSERT INTO A(a,b) VALUES (1, '2');
        SELECT * FROM A;
        SELECT b+2 FROM A;
        SELECT b::int+2 FROM A;

        DROP TABLE A; --forget you!
        
        CREATE TABLE A (
          a int NOT NULL,
          b text NOT NULL,
          c float NOT NULL
        );
        INSERT INTO A(a,b) VALUES (1, '2');       

OK let's go through some candidate and primary key business

        CREATE TABLE A (
          a int,
          b text,
          PRIMARY KEY (a)
        );
        
        INSERT INTO A VALUES (1, 'a');
        INSERT INTO A VALUES (1, 'b');
        
There can only be one primary key!        

        CREATE TABLE A (
          a int,
          b text,
          PRIMARY KEY (a),
          PRIMARY KEY (b)
        );  
        
        CREATE TABLE A (
          a int,
          b text,
          PRIMARY KEY (a),
          UNIQUE (b)
        );      
        
        CREATE TABLE A (
          a int,
          b text,
          c int,
          PRIMARY KEY (a),
          UNIQUE (b, c)
        );                  

Let's move onto references

        CREATE TABLE A(
          a int
        );
        
        CREATE TABLE B(
          b int,
          a int,
          FOREIGN KEY (a) REFERENCES A(a)
        );
        -- doh.  why does this fail?
        
  
FINE!  We'll make A.a unique

        CREATE TABLE A(
          a int,
          UNIQUE (a) 
        );
        
        CREATE TABLE B(
          b int,
          a int,
          FOREIGN KEY (a) REFERENCES A(a)
        );
        -- hmm... this worked.  let's try using this
        
        INSERT INTO A VALUES(1);
        INSERT INTO B(a, b) VALUES(2, 2); -- fail!
        INSERT INTO B(a, b) VALUES(1, 1); -- good!
        
        DELETE FROM A;  -- fail!
        UPDATE A SET a = 2; -- fail!
        UPDATE B SET a = NULL; -- ok
        UPDATE A SET a = NULL;
        INSERT INTO A VALUES(null); -- uh.....
        
Let's try again with a primary key

        CREATE TABLE A(
          a int,
          PRIMARY KEY (a) 
        );
        
        CREATE TABLE B(
          b int,
          a int,
          FOREIGN KEY (a) REFERENCES A(a)
        );
        
        INSERT INTO A VALUES(1);
        INSERT INTO B(a, b) VALUES(2, 2); -- fail!
        INSERT INTO B(a, b) VALUES(1, 1); -- good!
        
        DELETE FROM A;  -- fail!
        UPDATE A SET a = 2; -- fail!
        UPDATE B SET a = NULL; -- ok
        UPDATE A SET a = NULL; -- fail!!!
        INSERT INTO A VALUES(null); -- fail!!!

OK, so we learned that PRIMARY KEY == UNIQUE + NOT NULL.  Typically also + index.

What if we want do be able to delete an A record and still maintain
referential integrity?

        CREATE TABLE A(
          a int,
          PRIMARY KEY (a) 
        );
        
        CREATE TABLE B(
          b int,
          a int,
          FOREIGN KEY (a) REFERENCES A(a) ON DELETE CASCADE
        );
        
        INSERT INTO A VALUES(1);
        INSERT INTO B(a, b) VALUES(1, 1); 
        -- look at the database

        DELETE FROM A;  
 

What if you want to do some crazy stuff with circular dependencies?

        CREATE TABLE A(
          a int,
          b int,
          PRIMARY KEY (a),
          FOREIGN KEY (b) REFERENCES B(b)
        );
        -- doh.  there's no B
        
        CREATE TABLE B(
          a int,
          b int,
          PRIMARY KEY (b),
          FOREIGN KEY (a) REFERENCES A(a)
        );
        -- doh. there's no A.
        
OK how do we get some circular business?        

        CREATE TABLE A(
          a int,
          b int,
          PRIMARY KEY (a)
        );
        
        CREATE TABLE B(
          a int,
          b int,
          PRIMARY KEY (b),
          FOREIGN KEY (a) REFERENCES A(a)
        );

        ALTER TABLE A ADD FOREIGN KEY (b) REFERENCES B(b);
        

        BEGIN;
        DROP TABLE A;
        COMMIT;
        
        BEGIN;
        DROP TABLE A cascade;
        DROP TABLE B;
        ABORT;
        \d
        
        BEGIN;
        DROP TABLE A cascade;
        DROP TABLE B;
        COMMIT;

Let's try adding some data

        INSERT INTO A VALUES(1, 1); -- doh

        BEGIN;
        SET CONSTRAINTS DEFERRED;
        INSERT INTO A VALUES(1, 1);
        ABORT;

        -- :(


Let's try again

        CREATE TABLE A(
          a int,
          b int,
          PRIMARY KEY (a)
        );
        
        CREATE TABLE B(
          a int,
          b int,
          PRIMARY KEY (b),
          FOREIGN KEY (a) REFERENCES A(a) DEFERRABLE
        );

        ALTER TABLE A ADD FOREIGN KEY (b) REFERENCES B(b) DEFERRABLE;

        BEGIN;
        SET CONSTRAINTS DEFERRED;
        INSERT INTO A VALUES(1, 1);
        INSERT INTO B VALUES(1, 1);
        COMMIT;


Check constraints


        CREATE TABLE A(
          a int,
          b int,
          grade char(1),
          CHECK (
            grade = 'A' or grade = 'B' or
            grade = 'C' or grade = 'D' or
            grade = 'F'
          )
        );

        INSERT INTO A VALUES(1, 2, 3);
        INSERT INTO A VALUES(1, 2, 'a');
        INSERT INTO A VALUES(1, 2, 'A');



OK, let's talk about ER --> Relational


        CREATE TABLE A(
          a int,
          PRIMARY KEY (a)
        );

        CREATE TABLE B(
          b int,
          PRIMARY KEY (b)
        ); 
        INSERT INTO A VALUES (1), (2);
        INSERT INTO B VALUES (3), (4);

        CREATE TABLE A_B(
          a int REFERENCES A(a),
          b int REFERENCES B(b),
          quantity int default 0
        );

        -- what if put NOT NULL on a or b?
        -- what if put PRIMARY KEY(a)?
        --    (each A record can have <= 1 entry in A_B)
        --    (each B record can have any # entries in A_B)

        INSERT INTO A_B VALUES(1, null, default);
        INSERT INTO A_B VALUES(2, 3, default);
        INSERT INTO A_B VALUES(2, 4, default);


        -- can I use A_B to ensure each B record has at least 1 A record?
        -- can we express participation?

OK so the above can do "at most one" e.g., Key constraints

What about the following?

        CREATE TABLE A(
          a int,
          PRIMARY KEY (a)
        );

        -- what does this say?
        CREATE TABLE B(
          b int,
          a int NOT NULL references A(a),
          PRIMARY KEY (b)
        ); 
        
        -- each B record MUST reference a valid A record

        -- what if removed PRIMARY KEY (b)?
        --    every B record MUST reference 
        
 
What about total participation AND key constraints?

        -- A ==> A_B <== B

        CREATE TABLE A(a int PRIMARY KEY);
        CREATE TABLE B(b int PRIMARY KEY);
        CREATE TABLE A_B(
          a int NOT NULL REFERENCES A(a),
          b int NOT NULL REFERENCES B(b),
          UNIQUE (a),
          UNIQUE (b)
        );
        -- does this work?
        --    (only one A record can exist.  BUG)
        -- what about UNIQUE (a, b)?
        -- how to enforce that a record for A1 exists in A_B?

        -- <insert code here>
        
What about total participation from both sides?

        -- A == A_B == B

        -- can't play the "merge B and A_B" trick on both sides
        -- why not?

What about IS_A relationships?

        -- User(uid int PRIMARY KEY, name text)
        -- Student(grade int) IS_A User
        -- Staff(rating int) IS_A User
        
        -- What if Employs wants to reference Users?
        -- What if Employs wants to reference Student and Staff?
        

