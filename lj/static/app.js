+$(document).ready(function(){
 +    var form_submit = $("#create");
 +    form_submit.on("click", function(){
 +        $.ajax({
 +            url: "/create",
 +            data: {
 +                "title": $("[name='title']").val(),
 +                "body": $("[name='body']").val(),
 +            },
 +            success: function(){
 +                console.log("updated");
 +            }
 +        });        
 +
 +    });
