const url = 'http://219.78.175.160:1111/file_uploader';

const data = {
  purpose: 'upload',
  files: './example_data/InnoLab_visit_developer_kids.pptx'
};

const headers = {
  'Content-Type': 'application/json'
};

fetch(url, {
  method: 'POST',
  body: JSON.stringify(data),
  headers: headers
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));