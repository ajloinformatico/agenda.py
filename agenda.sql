create database agenda;
use agenda;
create table if not exists contactos(
	nombre varchar(50) UNIQUE NOT NULL,
    telefono varchar(20));

