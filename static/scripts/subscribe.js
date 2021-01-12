$(document).ready(function(){
	const csrf = $("input[name=csrfmiddlewaretoken]").val()
	$("#subscribe").on("click", function(){
		$.ajax({
			url:"",
			method:"GET",
			success: function(response){
				if (response.followed == false){
					$.ajax({
						url:"",
						method:"POST",
						data:{
							sub: 't',
							csrfmiddlewaretoken: csrf
						},
						success: function(){
							$("#subscribe").text("Отписаться")
							console.log(response.followed)
						}
					})
				}
				else if (response.followed == true){
					$.ajax({
						url:"",
						method:"POST",
						data:{
							sub: 'f',
							csrfmiddlewaretoken: csrf
						},
						success: function(){
							$("#subscribe").text("Подписаться")
						}
					})
				}
			}
		})
	})
})

