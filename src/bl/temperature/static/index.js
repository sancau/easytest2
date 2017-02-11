'use strict';

var data = {
    "target": "0",
    "logs": [
        {
            "file": "",
            "sensors_count": "8",
        }
    ],
    "sensors_total": "8",
    "slice_length": "10",
    "round_to": "1",
    "cp": [
        "0", "0", "0", "0", "0",
        "0", "0", "0", "0", "0"
    ],
    "md": [
        "0", "0", "0", "0", "0",
        "0", "0", "0", "0", "0"
    ],
    "max_deviation": "2"
}

function previewFile() {
  var file    = document.getElementById('file').files[0];
  var reader  = new FileReader();

  reader.addEventListener("load", function () {
    data.logs[0].file = reader.result.slice(23);
  }, false);

  if (file) {
      reader.readAsDataURL(file);
  }
}

function postData() {
    var url = 'http://127.0.0.1:5000/';
    axios.post(url, data).then(
        function(res) {
            console.log(res);
        }
    ).catch(function(e) { console.log(e); })
}