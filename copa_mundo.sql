CREATE DATABASE copa_mundo;
USE copa_mundo;

CREATE TABLE selecoes (
    id_selecao    INT PRIMARY KEY AUTO_INCREMENT,
    nome_selecao  VARCHAR(50) NOT NULL,
    continente    VARCHAR(30),
    tecnico       VARCHAR(50),
    titulos       INT
);

CREATE TABLE estadios (
    id_estadio    INT PRIMARY KEY AUTO_INCREMENT,
    nome_estadio  VARCHAR(80) NOT NULL,
    cidade        VARCHAR(50),
    pais          VARCHAR(50),
    capacidade    INT
);

CREATE TABLE jogadores (
    id_jogador       INT PRIMARY KEY AUTO_INCREMENT,
    nome_jogador     VARCHAR(60) NOT NULL,
    posicao          VARCHAR(30),
    numero_camisa    INT,
    data_nascimento  DATE,
    id_selecao       INT NOT NULL,
    FOREIGN KEY (id_selecao)
        REFERENCES selecoes(id_selecao)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE partidas (
    id_partida              INT PRIMARY KEY AUTO_INCREMENT,
    data_partida            DATE NOT NULL,
    id_estadio              INT NOT NULL,
    id_selecao_1            INT NOT NULL,
    id_selecao_2            INT NOT NULL,
    quantidade_gols_selecao_1 INT DEFAULT 0,
    quantidade_gols_selecao_2 INT DEFAULT 0,
    vencedor                INT,
    FOREIGN KEY (id_estadio)
        REFERENCES estadios(id_estadio)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_selecao_1)
        REFERENCES selecoes(id_selecao)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_selecao_2)
        REFERENCES selecoes(id_selecao)
        ON DELETE CASCADE ON UPDATE CASCADE
);
INSERT INTO selecoes (nome_selecao, continente, tecnico, titulos) VALUES
('Brasil', 'América do Sul', 'Dorival Júnior', 5),
('Argentina', 'América do Sul', 'Lionel Scaloni', 3),
('França', 'Europa', 'Didier Deschamps', 2),
('Alemanha', 'Europa', 'Julian Nagelsmann', 4),
('Espanha', 'Europa', 'Luis de la Fuente', 1),
('Portugal', 'Europa', 'Roberto Martínez', 0),
('Inglaterra', 'Europa', 'Gareth Southgate', 1),
('Marrocos', 'África', 'Walid Regragui', 0);

INSERT INTO estadios (nome_estadio, cidade, pais, capacidade) VALUES
('Maracanã', 'Rio de Janeiro', 'Brasil', 78000),
('Lusail Stadium', 'Lusail', 'Catar', 89000),
('Wembley', 'Londres', 'Inglaterra', 90000),
('Allianz Arena', 'Munique', 'Alemanha', 75000),
('Camp Nou', 'Barcelona', 'Espanha', 99000);

INSERT INTO jogadores (nome_jogador, posicao, numero_camisa, data_nascimento, id_selecao) VALUES
('Vinicius Jr', 'Atacante', 7, '2000-07-12', 1),
('Rodrygo', 'Atacante', 11, '2001-01-09', 1),
('Marquinhos', 'Zagueiro', 4, '1994-05-14', 1),
('Lionel Messi', 'Atacante', 10, '1987-06-24', 2),
('Julián Álvarez', 'Atacante', 9, '2000-01-31', 2),
('Kylian Mbappé', 'Atacante', 10, '1998-12-20', 3),
('Antoine Griezmann', 'Meia', 7, '1991-03-21', 3),
('Manuel Neuer', 'Goleiro', 1, '1986-03-27', 4),
('Thomas Müller', 'Meia', 25, '1989-09-13', 4),
('Pedri', 'Meia', 8, '2002-11-25', 5),
('Lamine Yamal', 'Atacante', 19, '2007-07-13', 5),
('Cristiano Ronaldo', 'Atacante', 7, '1985-02-05', 6),
('Bruno Fernandes', 'Meia', 8, '1994-09-08', 6),
('Harry Kane', 'Atacante', 9, '1993-07-28', 7),
('Jude Bellingham', 'Meia', 10, '2003-06-29', 7),
('Achraf Hakimi', 'Lateral', 2, '1998-11-04', 8),
('Hakim Ziyech', 'Meia', 7, '1993-03-19', 8),
('Alisson', 'Goleiro', 1, '1992-10-02', 1),
('Raphinha', 'Atacante', 10, '1996-12-14', 1),
('Theo Hernández', 'Lateral', 22, '1997-10-06', 3);

INSERT INTO partidas (data_partida, id_estadio, id_selecao_1, id_selecao_2, quantidade_gols_selecao_1, quantidade_gols_selecao_2, vencedor) VALUES
('2026-06-15', 1, 1, 6, 3, 1, 1),
('2026-06-16', 2, 2, 7, 2, 0, 2),
('2026-06-17', 3, 3, 8, 4, 0, 3),
('2026-06-18', 4, 4, 5, 1, 2, 5),
('2026-06-19', 5, 6, 7, 1, 1, NULL),
('2026-06-20', 1, 8, 2, 0, 3, 2),
('2026-06-21', 2, 1, 3, 2, 2, NULL),
('2026-06-22', 3, 5, 6, 3, 0, 5),
('2026-06-23', 4, 7, 4, 1, 2, 4),
('2026-06-24', 5, 2, 3, 1, 2, 3);