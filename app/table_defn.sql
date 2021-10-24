-- for aws redshift specifically

create table tx
(
    sig               varchar(256),
    err               varchar(256),
    fee               bigint,
    innerInstructions super,
    logMessages       super,
    postBalances      super,
    postTokenBalances super,
    preBalances       super,
    preTokenBalances  super,
    rewards           super,
    status            super,
    accountKeys       super,
    header            super,
    instructions      super,
    blockhash         varchar(256),

    primary key (sig),
    foreign key (blockhash) references blocks (blockhash)
);

create table blocks
(
    blockhash         varchar(256),
    blockTime         timestamp,
    blockHeight       bigint,
    parentSlot        bigint,
    previousBlockhash varchar(256),
    rewards           super,

    primary key (blockhash)
);
