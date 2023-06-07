create database CSC_490_Schema

use CSC_490_Schema

--- CREATING THE ADMIN
create table Admins(
	admin_id bigint identity(1,1) primary key,
	admin_name varchar(200),
	admin_password varchar(200)
);

--insert into Admins(admin_name, admin_password) values ('administrator', 'dummypassword1')

--- creating admin read procedure:

create procedure spReadAdmins(
@admin_username varchar(200),
@admin_password varchar (200),
@statement_type varchar(200)
) as

begin 
	if @statement_type = 'SELECT'
	begin
		select admin_name, admin_password from Admins
	end
end


--- CREATING THE TABLES OF THE SCHEMA

create table Faculty(
	faculty_id bigint identity(1,1) primary key,
	faculty_name varchar(100),
	faculty_code varchar(5),
	faculty_description text,
	update_date date default(getdate()),
	update_time time default(getdate())
);


create table Department(
	department_id bigint identity(1,1) primary key,
	department_name varchar(100),
	department_code varchar(5),
	department_description text,
	update_date date default(getdate()),
	update_time time default(getdate())
);

create table departmental_courses(
	departmental_courses_id bigint identity(1,1) primary key,
);

create table Programme(
	programme_id bigint identity(1,1) primary key,
	programme_name varchar(200),
	programme_duration varchar(5)
);

create table Courses(
	course_id bigint identity(1,1) primary key,
	course_name varchar(200)
);

create table course_registration(
	course_registration_id bigint identity(1,1) primary key
);

create table Staff(
	staff_id bigint identity(1,1) primary key,
	staff_name varchar(200),
	staff_reg_number varchar(100) unique,
	tel_num varchar(11) unique,
	email varchar(100) unique
);

create table Sessionss(
	session_id bigint identity(1,1) primary key,
	session_start date default(getdate()),
	session_end date default(getdate())
);

create table Semester(
	semester_id bigint identity(1,1) primary key,
	semester_start date default(getdate()),
	semester_end date default(getdate())
);

create table Levels(
	level_id bigint identity(1,1) primary key,
	level_name varchar(50)
);

create table Student(
	student_id bigint identity(1,1) primary key,
	student_name varchar(200),
	matric_num varchar(100) unique,
	tel_num varchar(11) unique,
	email varchar(200) unique
);

create table Classes(
	class_id bigint identity(1,1) primary key,
	class_date date default(getdate()),
	class_in time default(getdate()),
	class_out time default(getdate())
);

create table Student_Attendance(
	student_attendance_id bigint identity(1,1) primary key,
	time_in time default(getdate())
);

create table Staff_Attendance(
	staff_attendance_id bigint identity(1,1) primary key,
	time_in time default(getdate())
);


--- CREATING THE CONNECTIONS BETWEEN THE TABLES

alter table Department
add faculty_id bigint foreign key(faculty_id) references Faculty(faculty_id)

alter table Departmental_courses
add course_id bigint foreign key (course_id) references Courses(course_id),
session_id bigint foreign key (session_id) references Sessionss(session_id)

alter table Programme
add department_id bigint foreign key(department_id) references Department(department_id)

alter table Courses
add department_id bigint foreign key(department_id) references Department(department_id),
level_id bigint foreign key(level_id) references Levels(level_id),
semester_id bigint foreign key (semester_id) references Semester(semester_id)

-- Adding Course Code
alter table Courses
add course_code varchar(15)

alter table course_registration
add course_id bigint foreign key (course_id) references Courses(course_id),
student_id bigint foreign key (student_id) references Student(student_id)

alter table Staff
add department_id bigint foreign key(department_id) references Department(department_id)

alter table Semester
add session_id bigint foreign key (session_id) references Sessionss(session_id)

alter table Student
add department_id bigint foreign key(department_id) references Department(department_id)

alter table Student
add student_password varchar(200) default('welcome'),
student_image varbinary(max)

alter table Student
drop column student_image

Alter table Student
add student_image varchar(max)

alter table Student
add level_id bigint foreign key (level_id) references Levels(level_id)

alter table Staff
add staff_password varchar(200) default('welcome'),
staff_image varbinary(max)

alter table Staff
drop column staff_image

Alter table Staff
add staff_image varchar(max)


--Adding Course_reg id
alter table Student_attendance
add course_registration_id bigint foreign key(course_registration_id) references course_registration(course_registration_id)

alter table student_attendance
drop column course_registration_id

alter table Classes
add course_id bigint foreign key (course_id) references Courses(course_id)

alter table Student_Attendance
add student_id bigint foreign key (student_id) references Student(student_id),
class_id bigint foreign key (class_id) references Classes(class_id)

alter table Staff_Attendance
add staff_id bigint foreign key (staff_id) references Staff(staff_id),
class_id bigint foreign key (class_id) references Classes(class_id)


--- CREATING PROCEDURES FOR INSERT AND UPDATE FOR THE TBALES
select * from Faculty
create procedure spCRUDFaculty(
@faculty_id varchar(200),
@faculty_name varchar(200),
@faculty_code varchar(200),
@faculty_Description varchar(max),
@StatementType varchar(200))  as 
begin
	if @StatementType = 'SELECT'
	begin
		select * from Faculty
	end
	if @StatementType='INSERT'
	begin
		insert into faculty(faculty_name, faculty_code, faculty_description) values 
		(@faculty_name, @faculty_code, @faculty_description) 
	end
	if @StatementType='UPDATE'
	begin
		update faculty set faculty_name=@faculty_name, faculty_code=@faculty_code, faculty_description=@faculty_Description
		where faculty_id=@faculty_id
	end
end

select * from Department

create procedure spCRUDDepartment(
@department_id varchar(200),
@department_name varchar(200),
@department_code varchar(200),
@department_description varchar(max),
@faculty_id varchar(200),
@StatementType varchar(200))  as 
begin
	if @StatementType = 'SELECT'
	begin
		select * from Department
	end
	if @StatementType='INSERT'
	begin
		insert into Department(department_name, department_code, department_description, faculty_id) values 
		(@department_name, @department_code, @department_description, @faculty_id) 
	end
	if @StatementType='UPDATE'
	begin
		update Department set department_name=@department_name, department_code=@department_code, department_description=@department_description, faculty_id=@faculty_id
		where department_id=@department_id
	end
end

select * from Programme
create procedure spCRUDProgramme(
@programme_id varchar(200),
@programme_name varchar(200),
@programme_duration varchar(200),
@department_id varchar(200),
@StatementType varchar(200)
) as 
begin
	if @StatementType = 'SELECT'
	begin
		select * from Programme
	end
	if @StatementType = 'INSERT'
	begin
		insert into Programme(programme_name, programme_duration, department_id) values
		(@programme_name, @programme_duration, @department_id)
	end
	if @StatementType = 'UPDATE'
	begin
		update Programme set programme_name=@programme_name, programme_duration=@programme_name, department_id=@department_id
		where programme_id=@programme_id
	end
end

select * from Courses
create procedure spCRUDCourses(
@course_id varchar(200),
@course_name varchar(200),
@department_id varchar(200),
@level_id varchar(200),
@semester_id varchar(200),
@course_code varchar(200),
@StatementType varchar(200)
) as
begin
	if @StatementType = 'SELECT'
	begin
		select * from Courses
	end
	if @StatementType = 'INSERT'
	begin
		insert into Courses(course_name, department_id, level_id, semester_id, course_code) values
		(@course_name, @department_id, @level_id, @semester_id, @course_code)
	end
	if @StatementType = 'UPDATE'
	begin
		update Courses set course_name=@course_name, department_id=@department_id, level_id=@level_id, semester_id=@semester_id, course_code=@course_code
		where course_id=@course_id
	end
end

select * from Staff

create procedure spCRUDStaff(
@staff_id varchar(200),
@staff_name varchar(200),
@staff_reg_number varchar(200),
@tel_num varchar(200),
@email varchar(200),
@department_id varchar(200),
@staff_image varchar(max),
@StatementType varchar(200)
) as 
begin
	if @StatementType = 'SELECT'
	begin
		select * from Staff
	end
	if @StatementType = 'INSERT'
	begin
		insert into Staff(staff_name, staff_reg_number, tel_num, email, department_id, staff_image) values
		(@staff_name, @staff_reg_number, @tel_num, @email, @department_id, @staff_image)
	end
	if @StatementType = 'UPDATE'
	begin
		update Staff set staff_name=@staff_name, staff_reg_number=@staff_reg_number, tel_num=@tel_num, email=@email, department_id=@department_id, staff_image=@staff_image
		where staff_id=@staff_id
	end
end

select * from Sessionss
create procedure spCRUDSession(
@session_id varchar(200),
@session_start varchar(200),
@session_end varchar(200),
@StatementType varchar(200)
) as 
begin
	if @StatementType = 'SELECT'
	begin
		select * from Sessionss
	end
	if @StatementType = 'INSERT'
	begin
		insert into Sessionss(session_start, session_end) values (@session_start, @session_end)
	end
	if @StatementType = 'UPDATE'
	begin 
		update Sessionss set session_start = @session_start, session_end=@session_end
		where session_id=@session_id
	end
end

select * from Semester
create procedure spCRUDSemester(
@semester_id varchar(200),
@semester_start varchar(200),
@semester_end varchar(200),
@session_id varchar(200),
@StatementType varchar(200)
) as
begin
	if @StatementType = 'SELECT'
	begin
		select * from Semester
	end
	if @StatementType = 'INSERT'
	begin
		insert into Semester(semester_start, semester_end, session_id) values (@semester_start, @semester_end, @session_id)
	end
	if @StatementType = 'UPDATE'
	begin
		update Semester set semester_start=@semester_start, semester_end=@semester_end, session_id=@session_id
		where semester_id=@semester_id
	end
end

select * from Levels
create procedure spCRUDLevel(
@level_id varchar(200),
@level_name varchar(200),
@StatementType varchar(200)
) as 
begin
	if @StatementType = 'SELECT'
	begin
		select * from Levels
	end
	if @StatementType = 'INSERT'
	begin 
		insert into Levels(level_name) values (@level_name)
	end
	if @StatementType = 'UPDATE'
	begin 
		update Levels set level_name=@level_name where level_id=@level_id
	end
end

delete from Student where student_id < 23


select * from Student
create procedure spCRUDStudent(
@student_id varchar(200),
@student_name varchar(200),
@matric_num varchar(200),
@tel_num varchar(200),
@email varchar(200),
@department_id varchar(200),
@student_image varchar(max),
@level_id varchar(200),
@StatementType varchar(200)
) as 
begin 
	if @StatementType = 'SELECT'
	begin
		select * from Student
	end
	if @StatementType = 'INSERT'
	begin 
		insert into Student(student_name, matric_num, tel_num, email, department_id, student_image, level_id) values
		(@student_name, @matric_num, @tel_num, @email, @department_id, @student_image, @level_id)
	end
	if @StatementType = 'UPDATE'
	begin
		update Student set student_name=@student_name, matric_num=@matric_num, tel_num=@tel_num, email=@email, department_id=@department_id, student_image=@student_image, level_id=@level_id
		where student_id=@student_name
	end
end

select * from Classes
create procedure spCRUDClasses(
@class_id varchar(200),
@class_date varchar(200),
@class_in varchar(200),
@class_out varchar(200),
@course_id varchar(200),
@StatementType varchar(200)
) as
begin
	if @StatementType = 'SELECT'
	begin
		select * from 
		(	select Classes.class_date, Classes.class_in, Classes.class_out, Courses.course_code
			from Classes inner join Courses on Classes.course_id = Courses.course_id
		) as qry
	end
	if @StatementType = 'INSERT'
	begin
		insert into Classes(class_date, class_in, class_out, course_id) values
		(@class_date, @class_in, @class_out, @course_id)
	end
	if @StatementType = 'UPDATE'
	begin
		update Classes set class_date=@class_date, class_in=@class_in, class_out=@class_out, course_id=@course_id
		where class_id=@class_id
	end
end

select * from Student_Attendance
create procedure spCRUDStudent_Attendance(
@student_attendance_id varchar(200),
@student_id varchar(200),
@course_registration_id varchar(200),
@class_id varchar(200),
@StatementType varchar(200)
) as
begin 
	if @StatementType = 'SELECT'
	begin
		select * from Student_Attendance
	end
	if @StatementType = 'INSERT'
	begin
		insert into Student_Attendance(student_id, course_registration_id, class_id) values
		(@student_id, @course_registration_id, @class_id)
	end
	if @StatementType = 'UPDATE'
	begin
		update Student_Attendance set student_id=@student_id, course_registration_id=@course_registration_id, class_id=@class_id
		where student_attendance_id=@student_attendance_id
	end
end

select * from Staff_Attendance
create procedure spCRUDStaff_Attendance(
@staff_attendance_id varchar(200),
@time_in varchar(200),
@staff_id varchar(200),
@class_id varchar(200),
@StatementType varchar(200)
) as
begin 
	if @StatementType = 'SELECT'
	begin
		select * from Staff_Attendance
	end
	if @StatementType = 'INSERT'
	begin
		insert into Staff_Attendance(time_in, staff_id, class_id) values
		(@time_in, @staff_id, @class_id)
	end
	if @StatementType = 'UPDATE'
	begin
		update Staff_Attendance set time_in=@time_in, staff_id=@staff_id, class_id=@class_id
		where staff_attendance_id=@staff_attendance_id
	end
end

select * from Course_Registration
create procedure spCRUDCourse_Registration(
	@course_registration_id varchar(200),
	@course_id varchar(200),
	@student_id varchar(200),
	@StatementType varchar(200)
) as
begin
	if @StatementType = 'SELECT'
	begin
		select * from Course_Registration
	end
	if @StatementType = 'INSERT'
	begin
		insert into Course_Registration(course_id, student_id) values (@course_id, @student_id)
	end
	if @StatementType = 'UPDATE'
	begin
		update Course_Registration set course_id=@course_id, student_id=@student_id
		where course_registration_id=@course_registration_id
	end
end

select * from Departmental_Courses
create procedure spCRUDDepartmental_courses(
	@departmental_course_id varchar(200),
	@session_id varchar(200),
	@course_id varchar(200),
	@StatementType varchar(200)
) as 
begin 
	if @StatementType = 'SELECT'
	begin
		select * from Departmental_Courses
	end
	if @StatementType = 'INSERT'
	begin
		insert into Departmental_Courses(session_id, course_id) values (@session_id, @course_id)
	end
	if @StatementType = 'UPDATE'
	begin
		update Departmental_Courses set session_id=@session_id, course_id=@course_id
		where departmental_courses_id=@departmental_course_id
	end
end

create procedure spAUTHStudent(
	@email varchar(200),
	@password varchar(200)
) as

begin
	select email, student_password, student_image, level_id, student_id, department_id from Student where email=@email and student_password=@password
end

select * from Student

delete from Student where student_id = 1 or student_id = 2

update Student set level_id = 4 where student_id = 23

select * from staff

delete from staff where staff_id = 5

create procedure spAUTHStaff(
	@staff_reg_number varchar(200),
	@staff_password varchar(200)
) as
begin 
	select staff_reg_number, staff_password, staff_image  from Staff where staff_reg_number=@staff_reg_number and staff_password=@staff_password
end

select student_id, matric_num, course_name
from Student inner join Courses on Student.level_id = Courses.level_id

create procedure getCourses(
	@level_id varchar(200),
	@department_id varchar(200)
) as
begin
	select Courses.course_id, course_code, course_name, course_registration.course_id from Courses inner join Student on Courses.level_id = Student.level_id 
	left join course_registration on Courses.course_id = course_registration.course_id 
	where course_registration.course_id is NULL and Student.level_id = @level_id and Courses.department_id = @department_id
	group by course_name, course_code, Courses.course_id, course_registration.course_id
end

Exec getCourses @level_id = '4', @department_id = '3'

select * from Courses left join course_registration on Courses.course_id = course_registration.course_id where course_registration.course_id is NULL

select Courses.course_id, course_code, course_name, course_registration.course_id as Reg_id from Courses inner join Student on Courses.level_id = Student.level_id left join course_registration
on Courses.course_id = course_registration.course_id where course_registration.course_id is NULL
group by course_name, course_code, Courses.course_id, course_registration.course_id


select * from Classes inner join Courses on Classes.course_id = Courses.course_id inner join Student on Courses.department_id = Student.department_id

create procedure getStudentClasses(
	@level_id varchar(200),
	@department_id varchar(200),
	@student_id varchar(200)
) as
begin 
	select * from Classes inner join Courses on Classes.course_id = Courses.course_id inner join Student on Courses.department_id = Student.department_id
	where Student.student_id = @student_id and Courses.level_id = @level_id and Student.department_id = @department_id
end

Exec getStudentClasses @level_id = '4', @department_id = '2', @student_id = '26'

select * from Courses

select * from course_registration

select * from Classes inner join Courses on Classes.course_id = Courses.course_id
inner join course_registration on course_registration.course_id = Classes.course_id inner join Student on course_registration.student_id
= Student.student_id

create procedure getStudentClasses(
	@level_id varchar(200),
	@department_id varchar(200),
	@student_id varchar(200)
) as
begin 
	select Classes.class_id, Classes.class_date, Classes.class_in, Classes.class_out, Courses.course_code, Courses.course_name , Classes.meet_id
	from Classes inner join Courses on Classes.course_id = Courses.course_id
	inner join course_registration on course_registration.course_id = Classes.course_id 
	inner join Student on course_registration.student_id = Student.student_id
	where Courses.level_id = @level_id and Courses.department_id = @department_id and course_registration.student_id = @student_id
end

Exec getStudentClasses @level_id = '4', @department_id = '2', @student_id = '26'

select * from Student_Attendance

	

select Courses.course_id, course_code, course_name, course_registration.course_id as Reg_id from Courses inner join Student on Courses.level_id = Student.level_id left join course_registration
on Courses.course_id = course_registration.course_id where course_registration.course_id is not NULL
group by course_name, course_code, Courses.course_id, course_registration.course_id

create procedure getRegisteredCourses(
	@level_id varchar(200),
	@department_id varchar(200),
	@student_id varchar(200)
) as
begin
	select Courses.course_id, course_code, course_name, course_registration.course_id from Courses inner join Student on Courses.level_id = Student.level_id 
	left join course_registration on Courses.course_id = course_registration.course_id 
	where course_registration.course_id is not NULL and Student.level_id = @level_id and Courses.department_id = @department_id
	and course_registration.student_id = @student_id
	group by course_name, course_code, Courses.course_id, course_registration.course_id
end

select * from course_registration

Exec getRegisteredCourses @level_id = '4', @department_id = '2', @student_id = '26'

select * from Faculty

create procedure spDeleteFaculty(
	@faculty_id varchar(200)
) as 
begin
	delete from Faculty where faculty_id=@faculty_id
end

create procedure spAssignStaffs(
	@course_id varchar(200),
	@staff_id varchar(200)
) as
begin 
	select * from Courses inner join Classes on Courses.course_id = Classes.course_id
end

select course_name, course_code, class_date, class_in, class_out, Classes.meet_id
from Courses inner join Classes on Courses.course_id = Classes.course_id where staff_id = '7'


select * from Classes
alter table Classes
add meet_id varchar(200)
select * from Courses
update Courses set staff_id = 7 where course_code = 'CSC 201'
select * from Staff
alter table Courses
add staff_id bigint foreign key (staff_id) references Staff(staff_id)
select * from course_registration

update ClassQry set meet_id = NEWID() from (
	select class_id, class_date, class_in, class_out, course_id, meet_id from Classes
) as ClassQry

select * from Classes

select * from Classes