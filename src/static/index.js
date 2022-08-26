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
          load_notes();
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

function load_notes(){
  $.ajax({
    url:'http://localhost:8000/notes',
    type:'GET',
    dataType: "json",
    contentType: 'application/json',
    beforeSend: function(request) {
      request.setRequestHeader("Authorization", localStorage['token']);
    },
    success: function(response){
      let notes = response['notes'];
      for (let note in notes){
        let note_content = notes[note];
        let codeBlock = '<tr>' + 
                '<td>' + note_content['title'] + '</td>' +
                '<td>' + note_content['creation_date'] + '</td>' +
      '         </tr>';
            document.getElementById("list-notes").innerHTML += codeBlock;
      }
    },
    error: function(){
      alert("Wrong token detected");
    }
  }      
);  
}

function add_note(){
  let title = $('#title-add-note').val();
  if (title.length > 0){
    let note = JSON.stringify({
      "title": title,
    });
  
    $.ajax({
      url:'http://localhost:8000/notes',
      type:'POST',
      'data': note,
      dataType: "json",
      contentType: 'application/json',
      beforeSend: function(request) {
        request.setRequestHeader("Authorization", localStorage['token']);
      },
      success: function(response){
        let codeBlock = '<tr>' + 
        '<td>' + title + '</td>' +
        '<td>' + response['creation_date'] + '</td>' +
  '         </tr>';
        document.getElementById("list-notes").innerHTML += codeBlock; 
        $("#error-insert-message").css("display", "none");
        $('#title-add-note').val("");
        $('#addNoteModal').modal('hide');
      },
      error: function(response){
        let result_errors = response['responseJSON']['result'];
        let errors = [];
        for (let key in result_errors){
            errors.push(result_errors[key]);
        }
        $("#error-insert-message").css("display", "inline");
        $("#error-insert-message").css("margin-top", "20px");
        $('#error-insert-message').text(errors); 
        }
    }      
  );  
  }
  else{
    $("#error-insert-message").css("display", "inline");
    $("#error-insert-message").css("margin-top", "20px");
    $('#error-insert-message').text("Insert title");     
  }
}
