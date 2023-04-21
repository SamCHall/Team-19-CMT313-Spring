let origin = undefined

function onDragStart(event) {
  event.dataTransfer.setData('text/plain', event.target.value);
  origin = event.target.parentNode.parentNode;
}
  
function onDragOver(event) {
  event.preventDefault();
}

function onDrop(event) {
  if (event.target.parentNode.parentNode == origin){
    var dropzone = event.target;
    var optionValue = event.dataTransfer.getData('text/plain');
  
    dropzone.textContent = optionValue;
    document.getElementById('answer_' + dropzone.data.identifier).value = optionValue;
    event.dataTransfer.clearData();
  };
}

var dropzones = document.querySelectorAll('.dropzone');
for (var i = 0; i < dropzones.length; i++) {
  dropzones[i].addEventListener('dragover', onDragOver);
  dropzones[i].addEventListener('drop', onDrop);
}
