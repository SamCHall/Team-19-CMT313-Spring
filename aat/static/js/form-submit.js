var submitFormative = document.querySelector('#submit-formative')

submitFormative.addEventListener("click", function(event) {
  event.preventDefault();

  var assessmentId = document.querySelector('input[name="assessment_id"]').value;

  var dropzones = document.querySelectorAll('.dropzone');
  var optionValues = [];
  for (var i = 0; i < dropzones.length; i++) {
    optionValues.push(dropzones[i].textContent);
  }

  var radio_answers = document.querySelectorAll(`input[id="type2_radio"]:checked`);
  var type2Values = [];
  for (var i = 0; i < radio_answers.length; i++){
    type2Values.push(radio_answers[i].value);
  }
  console.log(type2Values);
  

  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/submit-assessment/' + assessmentId);
  xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
  const csrfToken = document.querySelector('input[name="csrf_token"]').value;
  xhr.setRequestHeader('X-CSRF-Token', csrfToken);
  xhr.onerror = function() {
    console.log('Error occurred during the request.');
  };

  const requestData = {
    type2Values: type2Values,
    optionValues: optionValues
  };
  
  xhr.send(JSON.stringify(requestData))
});
