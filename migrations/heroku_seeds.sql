DELETE FROM users;
DELETE FROM products;
DELETE FROM transactions;
DELETE FROM reviews;

INSERT INTO users (first_name, last_name, email, hashed_password)
VALUES
    ('demo', 'user', 'demouser@demouser.com', 'pbkdf2:sha256:150000$283iBvR6$1695a1277c460f12ee3cf544f64ce9aaa2bf9cc4e121ccb580c5335df845248f')
    ('CeeJay', 'Duhh', 'ceejayduhh@ceejayduhh.com', 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImNlZWpheWR1aGhAY2VlamF5ZHVoaC5jb20ifQ.MVe9oyWsTdk-k0s8RJ5fPz0JWH3_ieGEAvizW1BITm8')


INSERT INTO products (name, price, imgurl, color, size, description, category, new)
VALUES
    ('Supreme Takeshi Murakami COVID-19 Relief Box Logo Tee', 6000, 'https://www.supremecommunity.com/u/season/add/20200424b48cbe0f6cf943b7a95a34538f3de2c2_sqr.jpg', 'White', '')