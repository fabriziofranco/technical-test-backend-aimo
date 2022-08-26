let localStorage = {};

function login(){
    let username = $('#username').val();
    let password = $('#password').val();
    let message = JSON.stringify({
            "username": username,
            "password": password
    });
    let errors = [];
    $.ajax({
        url:'http://localhost:8000/login',
        type:'POST',
        data : message,
        dataType: "json",
        contentType: 'application/json',
        success: function(response){
          $('#username-logged').text("Bienvenido " + username); 
          $("#username-logged").css("display", "inline");
          $("#error-message").css("display", "none");
          $("#container-xl").css("display", "block");
          $("#login-page").css("display", "none");
          localStorage['token'] = response['result']['token'];
        },
        error: function(response){
          let result_errors = response['responseJSON']['result'];
          for (let key in result_errors){
              errors.push(result_errors[key]);
          }
          $("#error-message").css("display", "inline");
          $('#error-message').text(errors); 
        }
      }      
    );
}

function signup(){
    let username = $('#username').val();
    let password = $('#password').val();
    let message = JSON.stringify({
            "username": username,
            "password": password
    });
    let errors = [];

    $.ajax({
        url:'http://localhost:8000/signup',
        type:'POST',
        data : message,
        dataType: "json",
        contentType: 'application/json',
        success: function(){
          $("#error-message").css("display", "none");
          $('#username').val("");
          $('#password').val("");
        },
        error: function(response){
          let result_errors = response['responseJSON']['result'];
          for (let key in result_errors){
              errors.push(result_errors[key]);
          }
          $("#error-message").css("display", "inline");
          $('#error-message').text(errors); 
        }
      }      
    );
}


$(document).ready(function(){
	// Activate tooltip
	$('[data-toggle="tooltip"]').tooltip();
	
	// Select/Deselect checkboxes
	let checkbox = $('table tbody input[type="checkbox"]');
	$("#selectAll").click(function(){
		if(this.checked){
			checkbox.each(function(){
				this.checked = true;                        
			});
		} else{
			checkbox.each(function(){
				this.checked = false;                        
			});
		} 
	});
	checkbox.click(function(){
		if(!this.checked){
			$("#selectAll").prop("checked", false);
		}
	});
});