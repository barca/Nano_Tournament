-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
CREATE DATABASE TOURNAMENT
\c tournament
CREATE TABLE matches (
	ID 			int PRIMARY KEY 	NOT NULL,
	name			text
	wins			int
	player_history		int[]
);

