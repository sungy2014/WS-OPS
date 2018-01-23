INSERT INTO `process` (`id`, `step`, `step_id`) VALUES (1, '组内leader审批', 10);
INSERT INTO `process` (`id`, `step`, `step_id`) VALUES (2, 'QA审批', 20);
INSERT INTO `process` (`id`, `step`, `step_id`) VALUES (3, 'OPS审批/执行', 30);
INSERT INTO `process` (`id`, `step`, `step_id`) VALUES (4, 'Developer自验证', 40);
INSERT INTO `process` (`id`, `step`, `step_id`) VALUES (5, 'QA验证', 50);


INSERT INTO `process` (`id`, `step`, `step_id`) VALUES (1, '组内leader审批', 10);
INSERT INTO `process` (`id`, `step`, `step_id`) VALUES (2, 'QA审批', 20);
INSERT INTO `process` (`id`, `step`, `step_id`) VALUES (3, 'OPS审批/执行', 30);
INSERT INTO `process` (`id`, `step`, `step_id`) VALUES (4, 'Developer自验证', 40);
INSERT INTO `process` (`id`, `step`, `step_id`) VALUES (5, 'QA验证', 50);

insert into workform_type (`name`,`cn_name`,`process_step_id`) VALUES("publish","应用发布","10 -> 20 -> 30 -> 40 -> 50")

if(data['sql_file_url']){
		var files=data['sql_file_url'].split(';')
	        $.each(files,function(k,v){
		    $('#files_url_detail').append($("<p class='haha'/>").html(v.replace('/uploads/','')+"&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp").append($("<a target='_blank' class='hehe'/>").attr("href",v).text("预览")));
		});
            }else{
		$("#files_url_detail_div").attr('style','display:none')
            }
			
			fa-star-o
			<span class="fa fa-star-o fa-fw"></span>
			
			background-color: #2AEC27
			Qcs123!@#