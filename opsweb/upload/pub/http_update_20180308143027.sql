update item_group_rule 
set  
feature = REPLACE(feature,"http:","https:"),
gmt_modified = now();
where feature is not null;

update item_sku_image 
set  
image_url = REPLACE(image_url,"http:","https:"),
gmt_modified = now();
where image_url is not null;

update item_reviews 
set 
review_img_urls = REPLACE(review_img_urls,"http:","https:"),
sku_img_url = REPLACE(sku_img_url,"http:","https:"),
user_img_url = REPLACE(user_img_url,"http:","https:"), 
illegal_img_urls = REPLACE(illegal_img_urls,"http:","https:"),
gmt_modified = now();