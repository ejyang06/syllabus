Python UDF	
	
	create function googleit(word text) returns text as $$
	
	import requests
	r = requests.get("http://www.google.com/search?q=%s" % (word,))
	return r.content.decode('unicode-escape')
	
	$$ language plpython2u;
	
	
	
	select left(googleit('columbia university'), 50);
	select googleit('columbia university') LIKE '%Columbia%';
	


copy record

	
	create function copyit() returns trigger as $$
	begin 
		insert into b values(NEW.a); 
		return NEW; 
	end;
	$$ language plpgsql;
	
	create trigger t_copyit after insert on a 
	for each row	 
		when (NEW.a > 10) 
		execute procedure copyit();

Disable inserts to a	
	
 
	
	create trigger t_disable before insert on a 
	for each row 
		execute procedure disable();
	
	
	CREATE FUNCTION checktotal() RETURNS trigger	AS $$		BEGIN	IF ((SELECT COUNT(*) FROM sailors) +	    (SELECT COUNT(*) FROM boats) < 100) THEN		RETURN NEW	ELSE		RETURN null;	END IF;	END;	$$ LANGUAGE plpgsql;Recursive Trigger
	create function addme() returns trigger as $$
	begin
		insert into a values(NEW.a);
		return NEW;
	end;
	$$ language plpgsql;
	
	create trigger t_recursive before insert on a
	for each row
		execute procedure addme();
		
	-- also recursive
	create trigger t_recursive after insert on a
	for each row
		execute procedure addme();		
		
Still inorrect trigger

	CREATE FUNCTION addme_stillwrong() RETURNS trigger	AS $$		BEGIN		IF (SELECT COUNT(*) FROM a) < 10 THEN			INSERT INTO a VALUES (NEW.a + 1);		END IF;	RETURN NEW;	END;	$$ LANGUAGE plpgsql;		CREATE TRIGGER t_addme_stillwrong BEFORE INSERT ON a		FOR EACH ROW			EXECUTE PROCEDURE addme_stillwrong();
			
Correct trigger
	CREATE FUNCTION addme_works() RETURNS trigger	AS $$		BEGIN		IF (SELECT COUNT(*) FROM a) < 10 THEN			INSERT INTO a VALUES (NEW.a + 1);		END IF;	RETURN NEW;	END;	$$ LANGUAGE plpgsql;			CREATE TRIGGER t_addme_works AFTER INSERT ON a		FOR EACH ROW			EXECUTE PROCEDURE addme_works();		
check for totals		
	create function checktotal() returns trigger as $$
	begin
	if ((select count(*) from a) + (select count(*) from b) < 20) then
	  return NEW;
	else
	 return null;
	end if;
	end;
	$$ language plpgsql;
	
	create trigger t_check before insert on a   for each row execute procedure checktotal();		
WITH clause
	
	with num(n) as (
		select count(*) from a
	), 
		 num2(n) as (
		 select count(*) from a
	) 

	select num.n+num2.n from num, num2;	
	
Views

	create view acopy as 
		select * from a;
	insert into acopy values (99);
	
	create view aacopy as 
		select a1.a as a1, a2.a as a2 
		from a as a1, a as a2 
		where a1.a = a2.a;
	insert into aacopy values (88, 99);
	
	create view adistinct as select distinct * from a;
	insert into adistinct values (9);
	
Create table and default column names

	Create table b as select 1;	Create table b as select 1, 2;	
				