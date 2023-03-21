document.addEventListener("submit", function(event) {
  event.preventDefault();

  var assessmentId = document.querySelector('input[name="assessment_id"]').value;
  var dropzones = document.querySelectorAll('.dropzone');
  var optionValues = [];
  for (var i = 0; i < dropzones.length; i++) {
    optionValues.push(dropzones[i].textContent);
  }

  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/submit-assessment/' + assessmentId);
  xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
  const csrfToken = document.querySelector('input[name="csrf_token"]').value;
  xhr.setRequestHeader('X-CSRF-Token', csrfToken);
  xhr.onload = function() {
    console.log(xhr.responseText);
  };
  xhr.onerror = function() {
    console.log('Error occurred during the request.');
  };
  xhr.send(JSON.stringify({optionValues: optionValues}));
});
