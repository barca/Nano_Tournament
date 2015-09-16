\c tournament;
CREATE TABLE history (
	ID 				SERIAL,
	player1Id			int           NOT NULL,
	player2Id			int           NOT NULL CHECK (player2Id > player1Id)
);

