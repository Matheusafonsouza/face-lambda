
$.ajax({
  url: 'https://s3.amazonaws.com/fa-afonso-website/data.json',
  dataType: 'json',
  crossDomain: true,
  success: function (data) {
    console.log(data);
    mountTable(data);
  }
})


function mountTable(data) {


  for (var d of data) {
    var trTable = document.createElement("tr");

    var tdInfoPhoto = document.createElement("td");
    var tdInfoName = document.createElement("td");
    var tdInfoFaceMatch = document.createElement("td");


    tdInfoName.textContent = d.name;
    tdInfoFaceMatch.textContent = d.similarity;
    tdInfoPhoto = document.createElement("img");
    tdInfoPhoto.height = 100;
    tdInfoPhoto.width = 68;
    tdInfoPhoto.src = 'https://s3.amazonaws.com/fa-afonso-images/' + d.name + '.jpg';

    trTable.appendChild(tdInfoPhoto);
    trTable.appendChild(tdInfoName);
    trTable.appendChild(tdInfoFaceMatch);

    var table = document.querySelector("#tabela-site");

    table.appendChild(trTable);
  }
}
