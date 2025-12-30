-- Sample SQL queries for testing

select id,name,email from users where active=true;

select u.id,u.name,count(o.id) as order_count from users u left join orders o on u.id=o.user_id group by u.id,u.name;

select * from (select id,name from users where created_at>='2024-01-01') as recent_users;

insert into users(name,email,active) values('John Doe','john@example.com',true);

update users set active=false where last_login<'2023-01-01';