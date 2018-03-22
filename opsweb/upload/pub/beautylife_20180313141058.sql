UPDATE beautylife.ba_article SET photos=REPLACE(photos,"http://","https://") WHERE id BETWEEN 1 AND 10000
UPDATE beautylife.ba_article SET photos=REPLACE(photos,"http://","https://") WHERE id BETWEEN 10000 AND 20000;
UPDATE beautylife.ba_article SET photos=REPLACE(photos,"http://","https://") WHERE id BETWEEN 20000 AND 30000;
UPDATE beautylife.ba_article SET photos=REPLACE(photos,"http://","https://") WHERE id BETWEEN 30000 AND 40000;
UPDATE beautylife.ba_article SET photos=REPLACE(photos,"http://","https://") WHERE id BETWEEN 40000 AND 50000;
UPDATE beautylife.ba_article SET photos=REPLACE(photos,"http://","https://") WHERE id BETWEEN 50000 AND 60000;
UPDATE beautylife.ba_article SET photos=REPLACE(photos,"http://","https://") WHERE id BETWEEN 60000 AND 70000;
UPDATE beautylife.ba_article SET photos=REPLACE(photos,"http://","https://") WHERE id BETWEEN 70000 AND 80000;
UPDATE beautylife.ba_article SET photos=REPLACE(photos,"http://","https://") WHERE id BETWEEN 80000 AND 90000;
UPDATE beautylife.ba_article SET photos=REPLACE(photos,"http://","https://") WHERE id BETWEEN 90000 AND 100000;
UPDATE beautylife.ba_article SET photos=REPLACE(photos,"http://","https://") WHERE id BETWEEN 100000 AND 110000;
UPDATE beautylife.ba_article SET photos=REPLACE(photos,"http://","https://") WHERE id BETWEEN 110000 AND 120000;
UPDATE beautylife.ba_article SET photos=REPLACE(photos,"http://","https://") WHERE id BETWEEN 120000 AND 130000;
UPDATE beautylife.ba_article SET photos=REPLACE(photos,"http://","https://") WHERE id BETWEEN 130000 AND 140000;

UPDATE beautylife.ba_article_resource SET url=REPLACE(url,"http://","https://") WHERE id BETWEEN 1 AND 10000;
UPDATE beautylife.ba_article_resource SET url=REPLACE(url,"http://","https://") WHERE id BETWEEN 10000 AND 20000;
UPDATE beautylife.ba_article_resource SET url=REPLACE(url,"http://","https://") WHERE id BETWEEN 20000 AND 30000;

UPDATE beautylife.ba_article_topic SET icon_url=REPLACE(icon_url,"http://","https://"),content_urls= REPLACE(content_urls,"http://","https://");
UPDATE beautylife.ba_question SET photos=REPLACE(photos,"http://","https://");
UPDATE beautylife.ba_user SET avatar=REPLACE(avatar,"http://","https://"),cover_img_url= REPLACE(cover_img_url,"http://","https://");
UPDATE beautylife.ba_user_photo SET file_name=REPLACE(file_name,"http://","https://");