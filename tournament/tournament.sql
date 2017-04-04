-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament; -- A database named tournament is created

\connect tournament;  
CREATE SEQUENCE serial1 START 200; --create a sequence which generates value greater than 200


CREATE TABLE players(         -- this table stores record of each player which includes his playerid, name, no of matches
    id INT4 DEFAULT nextval('serial1'),
    name varchar(50),
    
   PRIMARY KEY( id )
);

CREATE TABLE matches( -- this table records the matches. id1 -> winner id, id2 -> loser id
	id1 INT references players(id), -- here id1 is foreign key which references players id
	id2 INT references players(id) 
);





--CREATE or Replace Function updatePlayer() RETURNS TRIGGER AS $$ -- this function executes when trigger is executed
--BEGIN
--Update players set no_matches = 0 where id =OLD.id1 or id = OLD.id2;
--RETURN OLD;
--END;
--$$ LANGUAGE plpgsql;

--CREATE TRIGGER updateMatches AFTER DELETE on   -- this is a trigger which updates no_of_matches when matches are deleted
--matches 
--FOR EACH ROW 
--EXECUTE PROCEDURE updatePlayer();











