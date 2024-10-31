-- Insert data into the Cultura table
INSERT INTO Cultura (id, nombre) VALUES
(1, 'Quechua'),
(2, 'Aymara'),
(3, 'Guaraní');

-- Insert data into the Festividad table
INSERT INTO Festividad (id, nombre) VALUES
(1, 'Inti Raymi'),
(2, 'Pachamama Raymi'),
(3, 'Ch’illa Raymi'),
(4, 'Día de los Difuntos'),
(5, 'Killa Raymi'),
(6, 'Varía según la región'),
(7, 'Tarpuy'),
(8, 'Cocha Raymi'),
(9, 'Wilkakuti'),
(10, 'Sara Raymi'),
(11, 'Qocha K’uychi'),
(12, 'Ayapec Raymi'),
(13, 'Día de Ollantay (regional)'),
(14, 'Festival de Alasitas'),
(15, 'Mamani Raymi'),
(16, 'Wilka Raymi'),
(17, 'Festival de Aymuru'),
(18, 'Jach’a Raymi'),
(19, 'Festival de Tupã'),
(20, 'Festival de Kuarahy'),
(21, 'Jasy Raymi'),
(22, 'Yacy Raymi'),
(23, 'Festival de Karai');

-- Insert data into the Deidad table
INSERT INTO Deidad (id, nombre, simbolismo, festividad, cultura) VALUES
(1, 'Viracocha', 'Dios creador, dios del mar, lagos y toda la creación', 1, 1),
(2, 'Inti', 'Dios del sol, padre de los emperadores incas', 1, 1),
(3, 'Pachamama', 'Madre tierra, diosa de la fertilidad, la agricultura y la cosecha', 2, 1),
(4, 'Illapa', 'Dios de la lluvia, el trueno y la guerra', 3, 1),
(5, 'Supay', 'Dios de la muerte y del inframundo', 4, 1),
(6, 'Mama Killa', 'Diosa de la luna, controla los ciclos lunares y la fertilidad femenina', 5, 1),
(7, 'Mama Cocha', 'Diosa del mar, lagos, ríos y la fertilidad marina', NULL, 1),
(8, 'Apu', 'Espíritus de las montañas, protectores de regiones específicas', NULL, 1),
(9, 'Kon', 'Dios de la lluvia y el viento, asociado con la costa', NULL, 1),
(10, 'Sara Mama', 'Diosa del maíz, madre del maíz y protectora de los cultivos', 7, 1),
(11, 'Cochamama', 'Diosa de los lagos y fuentes de agua', 8, 1),
(12, 'Apu Illimani', 'Espíritu protector de la montaña Illimani, venerado en rituales locales', 9, 1),
(13, 'Mama Sara', 'Deidad de los granos, maíz y la cosecha', 10, 1),
(14, 'Quchamama', 'Madre del lago, diosa de agua dulce', 11, 1),
(15, 'Pacha Kamaq', 'Dios de los terremotos, deidad creadora en ciertas culturas costeras quechuas', NULL, 1),
(16, 'Catequil', 'Dios del trueno y los relámpagos, asociado con tormentas', 3, 1),
(17, 'Ayapec', 'Deidad de la muerte y protector de los huesos ancestrales', 12, 1),
(18, 'Ollantay', 'Deidad guerrera heroica, asociada con el amor y la rebelión', 13, 1),
(19, 'Tunupa', 'Dios creador, dios de los volcanes y origen del lago Titicaca', NULL, 1),
(20, 'Ekeko', 'Dios de la abundancia, la riqueza y la prosperidad', 14, 2),
(21, 'Wari', 'Dios protector, asociado con guerreros y la muerte', NULL, 2),
(22, 'Supaya', 'Dios de los muertos y los espíritus del inframundo', 15, 2),
(23, 'Mamani', 'Dios de la fertilidad, a menudo asociado con la agricultura y la cosecha', 16, 2),
(24, 'Wilka', 'Deidad del sol asociada con la protección y la sabiduría ancestral', NULL, 2),
(25, 'Antu', 'Deidad protectora de lagos, ríos y mares', 17, 2),
(26, 'Aymuru', 'Deidad de la música y el canto, protector de ceremonias', 18, 2),
(27, 'Jach’a Tata', 'Espíritu protector de montañas grandes y regiones altas', 4, 2),
(28, 'Awicha', 'Espíritu ancestral asociado con la sabiduría y la protección familiar', NULL, 2),
(29, 'Muru', 'Dios de la cosecha y el crecimiento de cultivos', 19, 2),
(30, 'Tupã', 'Dios supremo de la creación, asociado con el trueno y la fertilidad', NULL, 3),
(31, 'Ñamandú', 'Dios de la sabiduría y la creación, a menudo considerado el "Padre del pueblo"', 20, 3),
(32, 'Kuarahy', 'Dios del sol, controla el día y la noche, una fuerza prominente en la naturaleza', 21, 3),
(33, 'Jasy', 'Diosa de la luna, asociada con la feminidad y la protección', NULL, 3),
(34, 'Ñanderuvusu', 'Gran Espíritu, la energía cósmica que lo abarca todo', 22, 3),
(35, 'Yacy Yateré', 'Espíritu travieso del bosque, protector de la armonía natural', 23, 3),
(36, 'Karai', 'Dios del fuego, asociado con la fuerza y la purificación', NULL, 3),
(37, 'Pombero', 'Espíritu del bosque, protector de los animales y la naturaleza', NULL, 3),
(38, 'Angatupyry', 'Espíritu del bien, a menudo contrastado con Tau (espíritu del mal)', NULL, 3),
(39, 'Tau', 'Espíritu del mal, opuesto a Angatupyry, un equilibrio en la dualidad de la naturaleza', NULL, 3),
(40, 'Mbói Tu’i', 'Deidad serpiente, protector de ríos y vías navegables', NULL, 3);
