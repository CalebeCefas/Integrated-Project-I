CREATE SCHEMA IF NOT EXISTS ru;

USE ru;

CREATE TABLE IF NOT EXISTS pratos (
    ID INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    prato ENUM('CVM', 'CB', 'VG') NOT NULL,
    avaliacao ENUM('RUIM', 'BOM', 'OTIMO') NOT NULL,
    PRIMARY KEY (ID),
    UNIQUE (prato, avaliacao) 
) ENGINE = InnoDB;

INSERT INTO ru.pratos (`prato`, `avaliacao`) VALUES 
('CVM', 'RUIM'),
('CVM', 'BOM'),
('CVM', 'OTIMO'),
('CB', 'RUIM'),
('CB', 'BOM'),
('CB', 'OTIMO'),
('VG', 'RUIM'),
('VG', 'BOM'),
('VG', 'OTIMO');

CREATE TABLE IF NOT EXISTS registro (
    ID INT(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    data DATE NOT NULL,
    hora TIME NOT NULL,
    ID_PRATO INT(11) UNSIGNED NOT NULL,
    PRIMARY KEY (ID),
    INDEX (data),
    INDEX (hora),
    INDEX (ID_PRATO),
    FOREIGN KEY (ID_PRATO) REFERENCES pratos(ID)
        ON DELETE RESTRICT 
        ON UPDATE RESTRICT
) ENGINE = InnoDB;

CREATE OR REPLACE VIEW ru.vw_resumo_diario AS
SELECT 
    r.data AS dia,
    CASE 
        WHEN r.hora BETWEEN '11:00:00' AND '14:00:00' THEN 'Almoço'
        ELSE 'Janta'
    END AS periodo,
    
    COUNT(CASE WHEN pa.prato = 'CVM' THEN 1 END) AS votos_cvm,
    COUNT(CASE WHEN pa.prato = 'CB' THEN 1 END) AS votos_cb,
    COUNT(CASE WHEN pa.prato = 'VG' THEN 1 END) AS votos_vg,
    COUNT(r.ID) AS total_votos

FROM 
    ru.registro AS r
JOIN 
    ru.pratos AS pa ON r.ID_PRATO = pa.ID
GROUP BY 
    dia, periodo;