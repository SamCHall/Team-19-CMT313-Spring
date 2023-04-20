var submitFormative = document.querySelector('#submit-formative')
if (submitFormative) {
submitFormative.addEventListener("click", function(event) {
  event.preventDefault();

  var assessmentId = document.querySelector('input[name="assessment_id"]').value;

  var dropzones = document.querySelectorAll('.dropzone');
  var optionValues = [];
  for (var i = 0; i < dropzones.length; i++) {
    optionValues.push(dropzones[i].textContent);
  }

  var type2Values = [];
  var radio_questions = document.querySelectorAll(`.question_type2`);
  for (var i = 0; i < radio_questions.length; i++) {
    var radio_options = radio_questions[i].querySelectorAll(`input[type="radio"]`);
    var found_checked = false;
    for (var j = 0; j < radio_options.length; j++) {
      if (radio_options[j].checked) {
        type2Values.push(radio_options[j].value);
        found_checked = true;
        break;
      }
    }
    if (!found_checked) {
      type2Values.push("");
    }
  }

  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/submit-assessment/' + assessmentId);
  xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
  const csrfToken = document.querySelector('input[name="csrf_token"]').value;
  xhr.setRequestHeader('X-CSRF-Token', csrfToken);
  xhr.onerror = function() {
    console.log('Error occurred during the request.');
  };

  xhr.onload = function() {
    if (xhr.status === 200) {
      const responseData = JSON.parse(xhr.responseText);
      const redirectUrl = responseData.redirect_url;
  
      // Redirect to the submission results page
      window.location.href = redirectUrl;
    }
  };
  
  const requestData = {
    type2Values: type2Values,
    optionValues: optionValues
  };
  
  xhr.send(JSON.stringify(requestData))
});
}
