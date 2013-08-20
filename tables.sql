BEGIN;

CREATE TABLE notifications (
    id SERIAL NOT NULL,
    
    "user" INTEGER NOT NULL,
    
    posted TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    expires TIMESTAMP WITHOUT TIME ZONE,
    
    message VARCHAR NOT NULL,
    category VARCHAR NOT NULL,
    data VARCHAR NOT NULL,
    
    PRIMARY KEY (id),
    FOREIGN KEY("user") REFERENCES users (id)
);

COMMIT;
