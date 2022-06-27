# configure replication user
grant replication slave on *.* to 'replication_user'@'%';
flush privileges;

# create objects
create table r1 (
    i1 int auto_increment primary key,
    c1 varchar(10),
    d1 datetime default current_timestamp()
);

insert into r1 (c1) values ('#1'),('#2'),('#3'),('#4'),('#5'),('#6'),('#7');

create table r2 (i2 int primary key, d2 datetime) ;
insert into r2 (i2, d2) values (1, now());
insert into r2 (i2, d2) values (2, now());
insert into r2 (i2, d2) values (3, now());
insert into r2 (i2, d2) values (4, now());

update r1 set c1=concat(c1, '-up');

select * from r2;

delete from r1 where i1 < 4;

drop table r2;

alter table r1 add column b1 bool default False;
insert into r1 (c1, b1) values ('#8', True);
