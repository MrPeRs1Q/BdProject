DROP DATABASE IF EXISTS gamedev;
CREATE DATABASE IF NOT EXISTS gamedev;
USE gamedev;
DROP TABLE IF EXISTS state;
CREATE TABLE IF NOT EXISTS state(
	state_id INT AUTO_INCREMENT,
    state VARCHAR(40) NOT NULL,
    PRIMARY KEY(state_id)
);
DROP TABLE IF EXISTS platform;
CREATE TABLE IF NOT EXISTS platform(
	platform_id INT AUTO_INCREMENT,
    platform VARCHAR(70) NOT NULL,
    PRIMARY KEY(platform_id)
);
DROP TABLE IF EXISTS specification;
CREATE TABLE IF NOT EXISTS specification(
	task_id INT AUTO_INCREMENT,
    task_name VARCHAR(150) NOT NULL,
    task_url VARCHAR(400),
    task VARCHAR(500),
    PRIMARY KEY(task_id)
);
DROP TABLE IF EXISTS project;
CREATE TABLE IF NOT EXISTS project(
	project_id INT AUTO_INCREMENT,
	project_name VARCHAR(40) NOT NULL,
	state_id INT,
    platform_id INT,
    project_version VARCHAR(15),
    github_url VARCHAR(100),
    PRIMARY KEY(project_id),
    FOREIGN KEY(platform_id) REFERENCES platform (platform_id),
    FOREIGN KEY(state_id) REFERENCES state (state_id)
);
DROP TABLE IF EXISTS department;
CREATE TABLE IF NOT EXISTS department(
	department_id INT AUTO_INCREMENT,
    department_name VARCHAR(255),
    project_id INT,
    PRIMARY KEY(department_id),
	FOREIGN KEY(project_id) REFERENCES project (project_id)
);
DROP TABLE IF EXISTS employee;
CREATE TABLE IF NOT EXISTS employee(
	employee_id INT AUTO_INCREMENT,
    employee_name VARCHAR(255) NOT NULL,
    employee_second_name VARCHAR(255) NOT NULL,
    position VARCHAR(100) NOT NULL,
    in_work BOOLEAN DEFAULT FALSE,
    department_id INT NOT NULL,
    PRIMARY KEY(employee_id),
    FOREIGN KEY(department_id) REFERENCES department (department_id)
);
DROP TABLE IF EXISTS dep_has_spec;
CREATE TABLE IF NOT EXISTS dep_has_spec(
	department_id INT NOT NULL,
    task_id INT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES department (department_id),
    FOREIGN KEY (task_id) REFERENCES specification (task_id)
);
-- Триггер для удаления состояний
DROP TRIGGER IF EXISTS state_BEFORE_DELETE;
CREATE DEFINER = CURRENT_USER TRIGGER state_BEFORE_DELETE BEFORE DELETE ON state FOR EACH ROW
BEGIN
	UPDATE project SET state_id = null WHERE state_id = OLD.state_id;
END
-- Триггер для удаления платформы
DROP TRIGGER IF EXISTS platform_BEFORE_DELETE;
CREATE DEFINER = CURRENT_USER TRIGGER platform_BEFORE_DELETE BEFORE DELETE ON platform FOR EACH ROW BEGIN
	DELETE FROM project where platform_id = old.platform_id;
END
